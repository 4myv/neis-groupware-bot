# notifier.py: 급식 알림 한 번을 처음부터 끝까지 처리하고, 실패하면 관리자에게 알리는 파일
#
# NEIS 조회 → 메시지 만들기 → Slack 전송을 차례로 하고, 어느 단계에서든 실패하면 관리자 채널로 알린다.
# 9단계의 정기 알림(스케줄러)과, 손으로 실행하는 send_lunch_message.py가 이 함수를 함께 쓴다.

from app.config import NEIS_OFFICE_CODE, NEIS_SCHOOL_CODE, SLACK_ADMIN_CHANNEL_ID, SLACK_CHANNEL_ID
from app.formatter import format_lunch_message
from app.log import logger
from app.neis import NeisError, fetch_meals
from app.sender import post_message

ADMIN_ALERT_TITLE: str = "[급식 봇 오류 알림]"


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
