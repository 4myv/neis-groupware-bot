# sender.py: Slack 채널로 메시지를 보내는 파일
#
# 정기 알림, 명령어 답장, 오류 알림이 모두 이 파일을 거쳐 Slack으로 나간다.
# 메신저를 바꾸게 되면 이 파일과 auth.py만 바꾸면 되도록, Slack에 보내는 코드는 여기에 모은다.
# 요청 방식은 Slack 공식 문서(chat.postMessage, Web API)를 따랐다. (docs/step04-devlog.md 참고)

import requests

from app.auth import get_access_token

SLACK_POST_MESSAGE_URL: str = "https://slack.com/api/chat.postMessage"
REQUEST_TIMEOUT_SECONDS: int = 10


def post_message(channel_id: str, text: str) -> dict:
    # Slack은 토큰을 Authorization 헤더에 "Bearer 토큰" 모양으로 받는다.
    # JSON 본문 안에는 토큰을 넣을 수 없다. (Slack 공식 문서)
    headers = {
        "Authorization": f"Bearer {get_access_token()}",
        "Content-Type": "application/json; charset=utf-8",
    }
    payload = {
        "channel": channel_id,
        "text": text,
    }
    response = requests.post(
        SLACK_POST_MESSAGE_URL,
        headers=headers,
        json=payload,
        timeout=REQUEST_TIMEOUT_SECONDS,
    )
    return response.json()
