# commands.py: 사용자가 봇에게 보낸 말을 명령어로 해석하고, 명령어마다 답장 글을 만드는 파일
#
# CLAUDE.md 규칙: 앞뒤 공백과 띄어쓰기 차이는 무시한다. (내일급식 = 내일 급식)
# 7단계: 명령어 해석 / 8단계: 명령어별 답장 만들기
# 급식·일정 조회와 메시지 모양은 정기 알림과 같은 neis.py, formatter.py를 함께 쓴다. (CLAUDE.md: 모듈 중복 금지)

from datetime import date, timedelta

from app.config import NEIS_OFFICE_CODE, NEIS_SCHOOL_CODE
from app.formatter import NO_MEAL_TEXT, format_lunch_message, format_week_schedule_message
from app.neis import fetch_meals, fetch_schedules

# 명령어의 이름. 글자를 여러 곳에 직접 쓰면 오타가 나기 쉬워서 이름을 붙여 둔다.
TODAY_LUNCH: str = "today_lunch"
TOMORROW_LUNCH: str = "tomorrow_lunch"
THIS_WEEK_SCHEDULE: str = "this_week_schedule"
HELP: str = "help"

# 사용자가 보내는 말 → 명령어 이름. 띄어쓰기를 모두 지운 모양으로 적어 둔다.
COMMANDS: dict[str, str] = {
    "오늘급식": TODAY_LUNCH,
    "내일급식": TOMORROW_LUNCH,
    "이번주일정": THIS_WEEK_SCHEDULE,
    "도움말": HELP,
}

# 도움말과, 목록에 없는 말에 보내는 답장 (CLAUDE.md 명령어 표)
HELP_TEXT: str = (
    "사용할 수 있는 명령어입니다.\n"
    "• 오늘 급식: 오늘 중식 메뉴\n"
    "• 내일 급식: 내일 중식 메뉴\n"
    "• 이번 주 일정: 이번 주 학사일정\n"
    "• 도움말: 이 안내"
)

# "내일 급식"에 급식이 없을 때의 문구.
# "오늘 급식"은 정기 알림과 같은 formatter.py의 NO_MEAL_TEXT("오늘은 급식이 없습니다.")를 쓴다.
NO_LUNCH_TOMORROW_TEXT: str = "내일은 급식이 없습니다."


def remove_spaces(text: str) -> str:
    # split()은 빈칸·줄바꿈·탭을 모두 기준으로 자른다. 잘린 조각을 다시 이어 붙이면 띄어쓰기가 모두 사라진다.
    return "".join(text.split())


def parse_command(text: str) -> str:
    key = remove_spaces(text)
    if key in COMMANDS:
        return COMMANDS[key]
    # 목록에 없는 말은 도움말로 답한다. (CLAUDE.md: "도움말 또는 그 밖의 말")
    return HELP


def to_yyyymmdd(day: date) -> str:
    # NEIS가 받는 날짜 모양(예: "20261105")으로 바꾼다.
    return day.strftime("%Y%m%d")


def week_start(today: date) -> date:
    # 이번 주 월요일. weekday()는 월요일이 0이라서, 그만큼 날짜를 빼면 월요일이 된다.
    return today - timedelta(days=today.weekday())


def week_end(today: date) -> date:
    # 이번 주 일요일 (월요일 + 6일)
    return week_start(today) + timedelta(days=6)


def make_lunch_reply(meal_day: date, no_meal_text: str) -> str:
    meal_date = to_yyyymmdd(meal_day)
    meal_result = fetch_meals(NEIS_OFFICE_CODE, NEIS_SCHOOL_CODE, meal_date)
    return format_lunch_message(meal_result, meal_date, no_meal_text)


def make_week_schedule_reply(today: date) -> str:
    start_date = to_yyyymmdd(week_start(today))
    end_date = to_yyyymmdd(week_end(today))
    schedule_result = fetch_schedules(NEIS_OFFICE_CODE, NEIS_SCHOOL_CODE, start_date, end_date)
    return format_week_schedule_message(schedule_result, start_date, end_date)


def build_reply(command: str, today: date) -> str:
    # 오늘 날짜(today)를 밖에서 받아야 테스트에서 원하는 날짜를 넣어 볼 수 있다.
    # NEIS 조회에 실패하면 NeisError가 그대로 올라간다. 부르는 쪽(app/notifier.py)이 처리한다.
    if command == TODAY_LUNCH:
        return make_lunch_reply(today, NO_MEAL_TEXT)
    if command == TOMORROW_LUNCH:
        return make_lunch_reply(today + timedelta(days=1), NO_LUNCH_TOMORROW_TEXT)
    if command == THIS_WEEK_SCHEDULE:
        return make_week_schedule_reply(today)
    return HELP_TEXT
