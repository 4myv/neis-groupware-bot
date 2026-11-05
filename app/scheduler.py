# scheduler.py: 매일 정해진 시각에 정기 알림(급식 + 오늘의 학사일정)을 보내는 파일
#
# APScheduler의 BackgroundScheduler를 쓴다. 이 스케줄러는 따로 일하는 줄(스레드)에서 시계를 보다가,
# 정해진 시각이 되면 함수를 실행한다. 그래서 콜백 서버와 한 프로그램 안에서 함께 돌아갈 수 있다. (main.py)
# 설정 방법은 APScheduler 3.x 공식 문서를 따랐다. (docs/step09-devlog.md)

from datetime import date

from apscheduler.schedulers.background import BackgroundScheduler

from app.commands import to_yyyymmdd
from app.config import NOTIFY_HOUR, NOTIFY_MINUTE
from app.log import logger
from app.notifier import notify_admin, send_lunch_notification

# 예약한 일을 나중에 찾을 때 쓰는 이름
DAILY_JOB_ID: str = "daily_lunch_notification"

# 정해진 시각을 놓쳤을 때(예: 7시 30분에 PC가 잠자기 상태) 몇 초 늦게까지는 보낼지.
# APScheduler의 기본값은 1초라서, 잠깐만 늦어도 그날 알림을 건너뛴다. 1시간까지는 늦게라도 보낸다.
MISFIRE_GRACE_SECONDS: int = 60 * 60


def send_today_notification() -> None:
    # 스케줄러가 매일 부르는 함수. 부를 때마다 '그날'의 날짜를 새로 구한다.
    today = to_yyyymmdd(date.today())
    logger.info(f"정기 알림 시작: {today}")
    try:
        send_lunch_notification(today)
    except Exception as error:
        # NEIS·Slack 오류는 send_lunch_notification 안에서 이미 처리한다.
        # 여기서는 미처 생각하지 못한 오류까지 잡아서 로그와 관리자 알림으로 남긴다.
        # 잡지 않으면 스케줄러가 오류를 화면에만 출력하고 넘어가서, 로그 파일과 관리자에게는 남지 않는다.
        logger.error(f"정기 알림 중 예상하지 못한 오류: {type(error).__name__}")
        notify_admin(f"{today} 정기 알림 중 예상하지 못한 오류가 났습니다. ({type(error).__name__}) logs/bot.log를 확인하세요.")


def create_scheduler() -> BackgroundScheduler:
    # 시간대를 따로 정하지 않으면 PC의 시간대(한국이면 Asia/Seoul)를 쓴다. date.today()와 같은 기준이다.
    scheduler = BackgroundScheduler()
    # "cron" 방식: 시와 분만 정하면 매일 그 시각에 실행한다.
    scheduler.add_job(
        send_today_notification,
        "cron",
        hour=NOTIFY_HOUR,
        minute=NOTIFY_MINUTE,
        id=DAILY_JOB_ID,
        misfire_grace_time=MISFIRE_GRACE_SECONDS,
        # 여러 번을 놓쳤다가 한꺼번에 실행할 차례가 되어도 한 번만 보낸다.
        coalesce=True,
    )
    return scheduler
