# auth.py: Slack 토큰을 발급받고, 만료되기 전에 새로 발급받는 파일
#
# 이 앱은 토큰 자동 교체(token rotation)를 켰다. 그래서 봇 토큰이 12시간마다 만료된다.
# 만료가 가까우면 refresh token으로 새 토큰을 받아 파일에 저장하고, 메시지를 보낼 때는 늘 파일의 토큰을 쓴다.
# 요청 주소와 인자는 Slack 공식 문서 "Using token rotation"을 따랐다. (docs/step04-devlog.md 참고)

import json
import time

import requests

from app.config import SLACK_CLIENT_ID, SLACK_CLIENT_SECRET, SLACK_TOKEN_FILE

SLACK_API_URL: str = "https://slack.com/api/"
REQUEST_TIMEOUT_SECONDS: int = 10

# 만료되기 이만큼(초) 전에 미리 새 토큰을 받는다. 메시지를 보내는 도중에 만료되는 일을 막으려고 여유를 둔다.
REFRESH_MARGIN_SECONDS: int = 300


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


def get_access_token() -> str:
    # 메시지를 보낼 때마다 이 함수로 토큰을 받는다.
    # 만료가 가까우면 새로 발급받아 저장한 뒤, 새 토큰을 돌려준다.
    tokens = load_tokens()
    if needs_refresh(tokens["expires_at"], time.time()):
        response_body = refresh_access_token(tokens["refresh_token"])
        save_token_response(response_body)
        return response_body["access_token"]
    return tokens["access_token"]
