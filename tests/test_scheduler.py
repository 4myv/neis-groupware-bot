# test_scheduler.py: 정기 알림 예약과 숫자 설정 읽기를 확인하는 테스트
# 실행 방법(가상환경을 켠 상태에서, 프로젝트 최상위 폴더에서): python -m pytest
#
# 스케줄러를 start() 하지 않고 예약 내용만 확인한다. 테스트하다가 실제 알림이 나가지 않게 하기 위해서다.

from app.config import NOTIFY_HOUR, NOTIFY_MINUTE, read_int_setting
from app.scheduler import DAILY_JOB_ID, MISFIRE_GRACE_SECONDS, create_scheduler, send_today_notification


def test_daily_job_runs_every_day_at_notify_time():
    job = create_scheduler().get_job(DAILY_JOB_ID)
    assert str(job.trigger) == f"cron[hour='{NOTIFY_HOUR}', minute='{NOTIFY_MINUTE}']"


def test_daily_job_calls_today_notification():
    job = create_scheduler().get_job(DAILY_JOB_ID)
    assert job.func == send_today_notification


def test_daily_job_allows_one_hour_late():
    job = create_scheduler().get_job(DAILY_JOB_ID)
    assert job.misfire_grace_time == MISFIRE_GRACE_SECONDS
    assert job.coalesce


def test_missing_number_setting_uses_default():
    assert read_int_setting("NO_SUCH_SETTING_FOR_TEST", 7) == 7
