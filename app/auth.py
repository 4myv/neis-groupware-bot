# auth.py: Slack 토큰을 발급받고, 만료되기 전에 새로 발급받는 파일
#
# 이 앱은 토큰 자동 교체(token rotation)를 켰다. 그래서 봇 토큰이 12시간마다 만료된다.
# 만료가 가까우면 refresh token으로 새 토큰을 받아 파일에 저장하고, 메시지를 보낼 때는 늘 파일의 토큰을 쓴다.
# 요청 주소와 인자는 Slack 공식 문서 "Using token rotation"을 따랐다. (docs/step04-devlog.md 참고)

import json
import time
from urllib.parse import parse_qs, urlencode, urlparse

import requests

from app.config import SLACK_CLIENT_ID, SLACK_CLIENT_SECRET, SLACK_TOKEN_FILE
from app.log import logger

SLACK_API_URL: str = "https://slack.com/api/"
REQUEST_TIMEOUT_SECONDS: int = 10

# 만료되기 이만큼(초) 전에 미리 새 토큰을 받는다. 메시지를 보내는 도중에 만료되는 일을 막으려고 여유를 둔다.
REFRESH_MARGIN_SECONDS: int = 300

# 앱을 다시 설치할 때 쓰는 값들 (Slack 공식 문서 "Installing with OAuth")
SLACK_AUTHORIZE_URL: str = "https://slack.com/oauth/v2/authorize"
# 4단계에서 등록한 Redirect URL. 허락하면 Slack이 이 주소에 일회용 code를 붙여 돌려보낸다.
SLACK_REDIRECT_URI: str = "https://localhost/slack/oauth/callback"
# 이 앱이 쓰는 봇 권한 전체. 권한을 늘리면 여기에도 적고 reinstall_slack_app.py로 다시 설치한다.
# chat:write: 메시지 보내기(4단계), im:history: 봇에게 온 1:1 메시지 받기(6단계)
SLACK_BOT_SCOPES: list[str] = ["chat:write", "im:history"]


class SlackAuthError(Exception):
    # Slack 토큰을 새로 발급받지 못했을 때 일으키는 오류
    pass


def save_tokens(access_token: str, refresh_token: str, expires_in: int) -> None:
    # Slack은 "몇 초 뒤에 만료되는지"(expires_in)를 알려 준다.
    # 나중에 지금 시각과 바로 비교할 수 있게 "만료되는 시각"(expires_at)으로 바꿔 저장한다.
    tokens = {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "expires_at": time.time() + expires_in,
    }
    SLACK_TOKEN_FILE.parent.mkdir(exist_ok=True)
    with open(SLACK_TOKEN_FILE, "w", encoding="utf-8") as file:
        json.dump(tokens, file, indent=2)


def save_token_response(response_body: dict) -> None:
    save_tokens(
        response_body["access_token"],
        response_body["refresh_token"],
        response_body["expires_in"],
    )


def load_tokens() -> dict:
    with open(SLACK_TOKEN_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def needs_refresh(expires_at: float, now: float) -> bool:
    return now >= expires_at - REFRESH_MARGIN_SECONDS


def exchange_long_lived_token(long_lived_token: str) -> dict:
    # 토큰 자동 교체를 켜기 전에 받은 xoxb- 토큰을 "만료되는 토큰 + refresh token"으로 바꾼다.
    # 같은 토큰은 한 번만 바꿀 수 있다. (Slack 공식 문서)
    response = requests.post(
        SLACK_API_URL + "oauth.v2.exchange",
        data={
            "client_id": SLACK_CLIENT_ID,
            "client_secret": SLACK_CLIENT_SECRET,
            "token": long_lived_token,
        },
        timeout=REQUEST_TIMEOUT_SECONDS,
    )
    return response.json()


def refresh_access_token(refresh_token: str) -> dict:
    # refresh token은 한 번 쓰면 버려진다. 응답에 새 refresh token이 오므로 반드시 다시 저장해야 한다.
    response = requests.post(
        SLACK_API_URL + "oauth.v2.access",
        data={
            "client_id": SLACK_CLIENT_ID,
            "client_secret": SLACK_CLIENT_SECRET,
            "grant_type": "refresh_token",
            "refresh_token": refresh_token,
        },
        timeout=REQUEST_TIMEOUT_SECONDS,
    )
    return response.json()


def build_authorize_url(state: str) -> str:
    # 다시 설치할 때 브라우저로 여는 Slack 허락 화면 주소를 만든다.
    # state는 이번 설치에서만 쓰는 무작위 값이다. 돌아온 값과 비교해 위조를 막는다.
    params = {
        "client_id": SLACK_CLIENT_ID,
        "scope": ",".join(SLACK_BOT_SCOPES),
        "redirect_uri": SLACK_REDIRECT_URI,
        "state": state,
    }
    return SLACK_AUTHORIZE_URL + "?" + urlencode(params)


def read_code_from_redirect(redirected_url: str, expected_state: str) -> str:
    # Slack이 돌려보낸 주소에서 일회용 code를 꺼낸다. 쓸 수 없으면 빈 문자열을 돌려준다.
    # state가 우리가 보낸 값과 다르면 위조로 보라는 것이 Slack 공식 문서의 안내다.
    query = parse_qs(urlparse(redirected_url.strip()).query)
    if query.get("state") != [expected_state]:
        return ""
    if "code" not in query:
        return ""
    return query["code"][0]


def exchange_code(code: str) -> dict:
    # 일회용 code를 토큰으로 바꾼다. code는 10분 뒤 만료된다. (Slack 공식 문서)
    # 허락 화면 주소에 redirect_uri를 넣었으므로, 여기에도 같은 값을 넣어야 한다.
    response = requests.post(
        SLACK_API_URL + "oauth.v2.access",
        data={
            "client_id": SLACK_CLIENT_ID,
            "client_secret": SLACK_CLIENT_SECRET,
            "code": code,
            "redirect_uri": SLACK_REDIRECT_URI,
        },
        timeout=REQUEST_TIMEOUT_SECONDS,
    )
    return response.json()


def refresh_and_save() -> str:
    # 저장된 refresh token으로 새 토큰을 받아 바로 저장하고, 새 access token을 돌려준다.
    # 만료가 가까울 때(get_access_token)와, 보내다가 토큰 오류가 났을 때(app/sender.py) 함께 쓴다.
    tokens = load_tokens()
    response_body = refresh_access_token(tokens["refresh_token"])
    if not response_body["ok"]:
        logger.error(f"Slack 토큰 재발급 실패: 오류 코드 {response_body['error']}")
        raise SlackAuthError("Slack 토큰을 새로 발급받지 못했습니다.")
    save_token_response(response_body)
    logger.info("Slack 토큰을 새로 발급받아 저장했습니다.")
    return response_body["access_token"]


def get_access_token() -> str:
    # 메시지를 보낼 때마다 이 함수로 토큰을 받는다.
    # 만료가 가까우면 새로 발급받아 저장한 뒤, 새 토큰을 돌려준다.
    tokens = load_tokens()
    if needs_refresh(tokens["expires_at"], time.time()):
        return refresh_and_save()
    return tokens["access_token"]
