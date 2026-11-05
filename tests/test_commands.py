# test_commands.py: 사용자가 보낸 말을 명령어로 해석하는 규칙과, 서버가 이벤트를 걸러내는 규칙을 확인하는 테스트
# 실행 방법(가상환경을 켠 상태에서, 프로젝트 최상위 폴더에서): python -m pytest

from datetime import date

from app.commands import (
    HELP,
    HELP_TEXT,
    THIS_WEEK_SCHEDULE,
    TODAY_LUNCH,
    TOMORROW_LUNCH,
    build_reply,
    parse_command,
    to_yyyymmdd,
    week_end,
    week_start,
)
from app.server import is_duplicate_event, is_user_message


# ---- 명령어 해석 (CLAUDE.md 명령어 표) ----

def test_today_lunch():
    assert parse_command("오늘 급식") == TODAY_LUNCH


def test_spaces_are_ignored():
    assert parse_command("내일급식") == TOMORROW_LUNCH
    assert parse_command("  내일   급식 \n") == TOMORROW_LUNCH


def test_this_week_schedule():
    assert parse_command("이번 주 일정") == THIS_WEEK_SCHEDULE
    assert parse_command("이번주일정") == THIS_WEEK_SCHEDULE


def test_help_command():
    assert parse_command("도움말") == HELP


def test_other_words_get_help():
    assert parse_command("안녕") == HELP
    assert parse_command("") == HELP


# ---- 사람이 보낸 새 메시지만 명령어로 본다 (Slack 공식 문서의 message 이벤트 모양) ----

def test_plain_user_message():
    assert is_user_message({"type": "message", "user": "U123", "text": "오늘 급식", "channel_type": "im"})


def test_bot_message_is_ignored():
    assert not is_user_message({"type": "message", "bot_id": "B123", "text": "[11월 5일(목) 중식]"})


def test_edited_message_is_ignored():
    assert not is_user_message({"type": "message", "subtype": "message_changed", "hidden": True})


# ---- 같은 이벤트는 한 번만 ----

def test_same_event_id_is_duplicate_the_second_time():
    assert not is_duplicate_event("Ev-test-only-0001")
    assert is_duplicate_event("Ev-test-only-0001")


# ---- 답장에 쓰는 날짜 계산 (8단계) ----

def test_date_to_neis_format():
    assert to_yyyymmdd(date(2026, 11, 5)) == "20261105"


def test_this_week_from_thursday():
    assert week_start(date(2026, 11, 5)) == date(2026, 11, 2)
    assert week_end(date(2026, 11, 5)) == date(2026, 11, 8)


def test_this_week_from_monday_and_sunday():
    assert week_start(date(2026, 11, 2)) == date(2026, 11, 2)
    assert week_start(date(2026, 11, 8)) == date(2026, 11, 2)


def test_this_week_across_new_year():
    assert week_start(date(2027, 1, 1)) == date(2026, 12, 28)
    assert week_end(date(2027, 1, 1)) == date(2027, 1, 3)


def test_help_reply_does_not_need_neis():
    assert build_reply(HELP, date(2026, 11, 5)) == HELP_TEXT
