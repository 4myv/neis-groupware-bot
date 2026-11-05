# server.py: Slack이 보내는 이벤트(봇에게 온 메시지 등)를 받는 콜백 서버 (FastAPI)
#
# 실행 방법(가상환경을 켠 상태에서): python -m uvicorn app.server:app --port 8000
# Slack 앱 설정의 Request URL에는 "터널 주소 + /slack/events"를 적는다. (docs/step06-devlog.md)
#
# 6단계: 받은 메시지를 화면과 로그에 남기기만 한다.
# 서명 검증(가짜 요청 거부)은 7단계, 답장은 8단계에서 더한다.
# 요청 모양과 규칙은 Slack 공식 문서(Events API, url_verification, message.im)를 따랐다.

from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse

from app.log import logger

# 터널로 인터넷에 열리는 서버라서, FastAPI가 자동으로 만드는 문서 페이지(/docs 등)는 끈다.
app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)


@app.post("/slack/events")
async def receive_slack_event(request: Request) -> PlainTextResponse:
    payload = await request.json()

    # Slack이 Request URL을 등록할 때 한 번 보내는 확인 요청이다.
    # 받은 challenge 값을 글자 그대로 돌려줘야 등록이 끝난다. (Slack 공식 문서: url_verification)
    if payload["type"] == "url_verification":
        logger.info("Slack Request URL 확인 요청을 받아 challenge를 돌려줬습니다.")
        return PlainTextResponse(payload["challenge"])

    # 3초 안에 응답하지 않으면 Slack이 같은 이벤트를 다시 보낸다. 다시 보낸 것이면 몇 번째인지 헤더에 적혀 온다.
    retry_number = request.headers.get("x-slack-retry-num", "")

    if payload["type"] == "event_callback":
        event = payload["event"]
        # 이벤트마다 들어 있는 항목이 달라서, 없을 수도 있는 항목은 get으로 꺼낸다.
        print(
            "[받은 이벤트]",
            "종류:", event.get("type"),
            "| 채널 종류:", event.get("channel_type"),
            "| 보낸 사람:", event.get("user"),
            "| 내용:", event.get("text"),
        )
        # 로그에는 메시지 내용 대신 어떤 이벤트가 왔는지만 남긴다.
        logger.info(
            f"Slack 이벤트 수신: event_id={payload.get('event_id')}, 종류={event.get('type')}, "
            f"채널 종류={event.get('channel_type')}, 재전송 번호={retry_number}"
        )

    # 받았다는 뜻으로 바로 200(정상)을 돌려준다.
    return PlainTextResponse("ok")
