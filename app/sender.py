# sender.py: Slack 채널로 메시지를 보내는 파일
#
# 정기 알림, 명령어 답장, 오류 알림이 모두 이 파일을 거쳐 Slack으로 나간다.
# 메신저를 바꾸게 되면 이 파일과 auth.py만 바꾸면 되도록, Slack에 보내는 코드는 여기에 모은다.
# 요청 방식은 Slack 공식 문서(chat.postMessage, Web API)를 따랐다. (docs/step04-devlog.md 참고)

import requests

from app.auth import SlackAuthError, get_access_token, refresh_and_save
from app.log import logger

SLACK_POST_MESSAGE_URL: str = "https://slack.com/api/chat.postMessage"
REQUEST_TIMEOUT_SECONDS: int = 10

# 이 오류 코드가 오면 토큰 문제로 보고, 새 토큰을 받아 한 번 다시 보낸다.
# token_expired: 토큰이 만료됨, invalid_auth: 토큰이 맞지 않음 (Slack 공식 문서의 오류 설명)
TOKEN_ERROR_CODES: list[str] = ["token_expired", "invalid_auth"]


def send_once(channel_id: str, text: str, access_token: str) -> dict:
    # Slack은 토큰을 Authorization 헤더에 "Bearer 토큰" 모양으로 받는다.
    # JSON 본문 안에는 토큰을 넣을 수 없다. (Slack 공식 문서)
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json; charset=utf-8",
    }
    payload = {
        "channel": channel_id,
        "text": text,
    }
    try:
        response = requests.post(
            SLACK_POST_MESSAGE_URL,
            headers=headers,
            json=payload,
            timeout=REQUEST_TIMEOUT_SECONDS,
        )
        return response.json()
    except (requests.RequestException, ValueError) as error:
        # 인터넷이 끊겼거나 응답이 JSON이 아닐 때도 Slack 응답과 같은 모양으로 돌려준다.
        logger.warning(f"Slack 전송 요청 실패: {type(error).__name__}")
        return {"ok": False, "error": "request_failed"}


def needs_new_token(response_body: dict) -> bool:
    return not response_body["ok"] and response_body["error"] in TOKEN_ERROR_CODES


def post_message(channel_id: str, text: str) -> dict:
    # 실패해도 오류를 일으키지 않고 늘 {"ok": ..., "error": ...} 모양을 돌려준다.
    # 그래서 부르는 쪽은 ok만 확인하면 된다.
    try:
        response_body = send_once(channel_id, text, get_access_token())
        if needs_new_token(response_body):
            # 토큰이 만료되었거나 맞지 않으면 새로 발급받아 한 번 다시 보낸다. (CLAUDE.md 예외 처리 규칙)
            logger.warning(f"Slack 토큰 오류({response_body['error']}): 새 토큰으로 다시 보냅니다.")
            response_body = send_once(channel_id, text, refresh_and_save())
    except (SlackAuthError, OSError, requests.RequestException, ValueError, KeyError) as error:
        # 토큰 파일이 없거나(OSError), 재발급에 실패하면 여기로 온다.
        logger.error(f"Slack 토큰을 준비하지 못했습니다: {type(error).__name__}")
        return {"ok": False, "error": "token_unavailable"}

    if response_body["ok"]:
        logger.info(f"Slack 전송 성공: 채널 {channel_id}")
    else:
        logger.error(f"Slack 전송 실패: 채널 {channel_id}, 오류 코드 {response_body['error']}")
    return response_body
