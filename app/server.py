# server.py: Slack이 보내는 이벤트(봇에게 온 메시지 등)를 받는 콜백 서버 (FastAPI)
#
# 실행 방법(가상환경을 켠 상태에서): python -m uvicorn app.server:app --port 8000
# Slack 앱 설정의 Request URL에는 "터널 주소 + /slack/events"를 적는다. (docs/step06-devlog.md)
#
# 6단계: 받은 이벤트를 출력한다.
# 7단계: 서명이 맞지 않는 요청은 거부하고, 같은 이벤트는 한 번만 처리하고, 명령어를 해석한다.
# 8단계: Slack에 먼저 응답한 뒤, 뒤에서 명령어 답장을 보낸다.
# 요청 모양과 규칙은 Slack 공식 문서(Events API, url_verification, message, 요청 서명)를 따랐다.

import json
import time

from fastapi import BackgroundTasks, FastAPI, Request
from fastapi.responses import PlainTextResponse

from app.auth import is_valid_slack_request
from app.commands import parse_command
from app.config import SLACK_SIGNING_SECRET
from app.log import logger
from app.notifier import send_command_reply

# 터널로 인터넷에 열리는 서버라서, FastAPI가 자동으로 만드는 문서 페이지(/docs 등)는 끈다.
app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)

# 이미 처리한 이벤트 ID. Slack이 같은 이벤트를 다시 보내도 한 번만 처리하려고 기억해 둔다.
# 서버를 다시 켜면 비워진다.
processed_event_ids: set[str] = set()


def is_duplicate_event(event_id: str) -> bool:
    if event_id in processed_event_ids:
        return True
    processed_event_ids.add(event_id)
    return False


def is_user_message(event: dict) -> bool:
    # 봇이 보낸 메시지에는 bot_id가 붙는다. (Slack 공식 문서: message 이벤트의 bot_message)
    # 수정·삭제 같은 메시지에는 subtype이 붙는다. 사람이 직접 보낸 새 메시지만 명령어로 본다.
    # 봇이 자기 답장을 다시 명령어로 읽어 끝없이 답하는 일을 막는다.
    return event.get("type") == "message" and "bot_id" not in event and "subtype" not in event


@app.post("/slack/events")
async def receive_slack_event(request: Request, background_tasks: BackgroundTasks) -> PlainTextResponse:
    # 서명은 받은 그대로의 본문으로 계산해야 한다. 그래서 JSON으로 바꾸기 전에 원래 본문(바이트)을 먼저 읽는다.
    body = await request.body()
    timestamp = request.headers.get("x-slack-request-timestamp", "")
    signature = request.headers.get("x-slack-signature", "")
    if not is_valid_slack_request(SLACK_SIGNING_SECRET, timestamp, signature, body, time.time()):
        # CLAUDE.md 규칙: 서명이 맞지 않는 콜백은 거부하고 로그에 기록한다.
        logger.warning("서명이 맞지 않는 요청을 거부했습니다.")
        return PlainTextResponse("invalid signature", status_code=401)

    payload = json.loads(body)

    # Slack이 Request URL을 등록할 때 한 번 보내는 확인 요청이다.
    # 받은 challenge 값을 글자 그대로 돌려줘야 등록이 끝난다. (Slack 공식 문서: url_verification)
    if payload["type"] == "url_verification":
        logger.info("Slack Request URL 확인 요청을 받아 challenge를 돌려줬습니다.")
        return PlainTextResponse(payload["challenge"])

    # 3초 안에 응답하지 않으면 Slack이 같은 이벤트를 다시 보낸다. 다시 보낸 것이면 몇 번째인지 헤더에 적혀 온다.
    retry_number = request.headers.get("x-slack-retry-num", "")

    if payload["type"] == "event_callback":
        event = payload["event"]
        event_id = payload.get("event_id", "")
        if is_duplicate_event(event_id):
            # CLAUDE.md 규칙: 콜백 중복 수신 → 응답을 바로 돌려주고, 같은 메시지는 한 번만 처리한다.
            logger.info(f"이미 처리한 이벤트라 건너뜁니다: event_id={event_id}, 재전송 번호={retry_number}")
            return PlainTextResponse("ok")

        if is_user_message(event):
            command = parse_command(event.get("text", ""))
            print("[명령어]", command, "| 보낸 글:", event.get("text"))
            # 로그에는 보낸 글 대신 어떤 명령어로 해석했는지만 남긴다.
            logger.info(f"명령어 해석: event_id={event_id}, 명령어={command}")
            # NEIS 조회와 Slack 전송은 3초를 넘길 수 있다.
            # 그래서 답장은 뒤에서(응답을 돌려준 다음에) 보내도록 맡겨 두고, Slack에는 바로 200을 돌려준다.
            background_tasks.add_task(send_command_reply, event["channel"], command)
        else:
            logger.info(f"사람이 보낸 새 메시지가 아니라 건너뜁니다: event_id={event_id}, subtype={event.get('subtype')}")

    # 받았다는 뜻으로 바로 200(정상)을 돌려준다.
    return PlainTextResponse("ok")
