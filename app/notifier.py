# notifier.py: 메시지 하나를 처음부터 끝까지 보내고, 실패하면 관리자에게 알리는 파일
#
# NEIS 조회 → 메시지 만들기 → Slack 전송을 차례로 하고, 어느 단계에서든 실패하면 관리자 채널로 알린다.
# - send_lunch_notification: 급식 알림 (9단계 정기 알림, send_lunch_message.py)
# - send_command_reply: 명령어 답장 (8단계 콜백 서버)

from datetime import date

from app.commands import build_reply
from app.config import NEIS_OFFICE_CODE, NEIS_SCHOOL_CODE, SLACK_ADMIN_CHANNEL_ID, SLACK_CHANNEL_ID
from app.formatter import format_lunch_message
from app.log import logger
from app.neis import NeisError, fetch_meals
from app.sender import post_message

ADMIN_ALERT_TITLE: str = "[급식 봇 오류 알림]"

# 명령어 답장을 만들다가 NEIS에서 정보를 받지 못했을 때, 사용자에게 보내는 답장
COMMAND_FAILED_TEXT: str = "지금은 정보를 가져오지 못했습니다. 잠시 뒤에 다시 보내 주세요."


def notify_admin(problem: str) -> None:
    response_body = post_message(SLACK_ADMIN_CHANNEL_ID, ADMIN_ALERT_TITLE + "\n" + problem)
    if not response_body["ok"]:
        # 관리자 채널로도 보내지 못하면 로그 파일이 유일한 기록이다.
        logger.error("관리자 오류 알림도 보내지 못했습니다. 로그 파일을 확인하세요.")


def send_lunch_notification(meal_date: str) -> bool:
    # 성공하면 True, 실패하면 관리자에게 알린 뒤 False를 돌려준다.
    try:
        meal_result = fetch_meals(NEIS_OFFICE_CODE, NEIS_SCHOOL_CODE, meal_date)
    except NeisError as error:
        logger.error(f"{meal_date} 급식 알림 실패: {error}")
        notify_admin(f"{meal_date} 급식 정보를 NEIS에서 받지 못했습니다.\n{error}")
        return False

    message = format_lunch_message(meal_result, meal_date)
    response_body = post_message(SLACK_CHANNEL_ID, message)
    if not response_body["ok"]:
        notify_admin(f"{meal_date} 급식 알림을 Slack으로 보내지 못했습니다. (오류 코드: {response_body['error']})")
        return False

    logger.info(f"{meal_date} 급식 알림 완료")
    return True


def send_command_reply(channel_id: str, command: str) -> None:
    # 콜백 서버가 Slack에 먼저 응답한 뒤, 뒤에서(백그라운드로) 부르는 함수다. (3초 규칙)
    # 사용자가 명령어를 보낸 1:1 대화방(channel_id)으로 답장한다.
    try:
        reply = build_reply(command, date.today())
    except NeisError as error:
        logger.error(f"명령어 답장 실패({command}): {error}")
        notify_admin(f"명령어 답장({command})에 필요한 정보를 NEIS에서 받지 못했습니다.\n{error}")
        # 사용자에게는 아무 답도 없는 것보다, 지금은 안 된다고 알려 주는 편이 낫다.
        reply = COMMAND_FAILED_TEXT

    response_body = post_message(channel_id, reply)
    if response_body["ok"]:
        logger.info(f"명령어 답장 완료: {command}")
    else:
        notify_admin(f"명령어 답장({command})을 Slack으로 보내지 못했습니다. (오류 코드: {response_body['error']})")
