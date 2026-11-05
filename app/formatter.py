# formatter.py: NEIS 급식 응답을 사람이 읽기 좋은 메시지로 바꾸는 파일
#
# 정기 알림과 명령어 응답이 같은 메시지 모양을 쓰도록, 변환은 모두 이 파일에서 한다.
# 실제 NEIS 응답의 모양은 docs/step02-devlog.md 4번 [B], [C]에 있다.

from datetime import datetime

# MMEAL_SC_CODE 값 중 중식. 실제 응답에서 "2"가 중식, "3"이 석식이었다. (step02 개발 기록 6번)
LUNCH_CODE: str = "2"

# 급식 데이터가 없는 날(주말, 방학, 공휴일)에 보낼 문구. 오류가 아니라 정상 상황이다.
NO_MEAL_TEXT: str = "오늘은 급식이 없습니다."

# datetime의 weekday()는 월요일을 0, 일요일을 6으로 돌려준다. 그 번호 순서대로 적었다.
WEEKDAY_NAMES: list[str] = ["월", "화", "수", "목", "금", "토", "일"]

# 메시지에서 메뉴와 메뉴 사이에 넣을 구분자
DISH_SEPARATOR: str = " / "

# 학사일정이 없을 때 쓸 문구 (CLAUDE.md 메시지 예시)
NO_SCHEDULE_TEXT: str = "없음"

# 학사일정 메시지에서 뺄 행사 이름.
# 확인한 학교 세 곳의 실제 응답에 매주 토요일마다 들어 있어서, 그대로 두면 매번 같은 줄이 붙는다. (step08 개발 기록)
HIDDEN_EVENT_NAMES: list[str] = ["토요휴업일"]

# 같은 날의 행사 이름 사이에 넣을 구분자
EVENT_SEPARATOR: str = ", "


def split_dishes(ddish_text: str) -> list[str]:
    # NEIS는 메뉴 사이를 줄바꿈 태그 <br/>로 이어 보낸다. 예: "흑미밥 <br/>부대찌개 (1.2.5.6)"
    dishes = []
    for part in ddish_text.split("<br/>"):
        # 태그 앞뒤에 빈칸이 붙어 오는 경우가 있어서 양쪽 빈칸을 지운다.
        dish = part.strip()
        if dish != "":
            dishes.append(dish)
    return dishes


def find_allergy_start(dish: str) -> int:
    # 메뉴 이름 맨 끝의 알레르기 번호 괄호가 시작하는 위치를 돌려준다. 없으면 -1을 돌려준다.
    # 실제 응답은 "부대찌개 (1.2.5.6)", CLAUDE.md 예시는 "된장찌개(5.6.9.)" 모양이라 둘 다 다룬다.
    if not dish.endswith(")"):
        return -1
    start = dish.rfind("(")
    if start == -1:
        return -1
    inside = dish[start + 1:-1]
    # "떡볶이(국물)"처럼 메뉴 이름의 일부인 괄호는 지우면 안 되므로,
    # 괄호 안이 숫자와 점으로만 되어 있을 때만 알레르기 번호로 본다.
    if inside.replace(".", "").isdigit():
        return start
    return -1


def remove_allergy_numbers(dish: str) -> str:
    start = find_allergy_start(dish)
    if start == -1:
        return dish.strip()
    return dish[:start].strip()


def extract_allergy_numbers(dish: str) -> list[str]:
    # 알레르기 번호는 버리지 않고 따로 보관한다. 나중에 "알레르기" 명령어로 확장할 수 있다.
    start = find_allergy_start(dish)
    if start == -1:
        return []
    inside = dish[start + 1:-1]
    numbers = []
    for part in inside.split("."):
        # "5.6.9."처럼 끝에 점이 있으면 마지막 조각이 빈 문자열이 되므로 건너뛴다.
        if part != "":
            numbers.append(part)
    return numbers


def parse_dishes(ddish_text: str) -> list[dict]:
    # 메뉴마다 이름과 알레르기 번호를 짝지어 담는다.
    dishes = []
    for raw_dish in split_dishes(ddish_text):
        dish = {
            "name": remove_allergy_numbers(raw_dish),
            "allergy_numbers": extract_allergy_numbers(raw_dish),
        }
        dishes.append(dish)
    return dishes


def format_date(yyyymmdd: str) -> str:
    # "20261105" → "11월 5일(목)"
    meal_day = datetime.strptime(yyyymmdd, "%Y%m%d")
    weekday_name = WEEKDAY_NAMES[meal_day.weekday()]
    return f"{meal_day.month}월 {meal_day.day}일({weekday_name})"


def find_lunch_row(meal_result: dict) -> dict:
    # 급식이 없는 날은 "mealServiceDietInfo" 키 없이 RESULT만 온다. (step02 개발 기록 4번 [C])
    # 그런 날과, 석식만 있고 중식이 없는 날은 빈 딕셔너리를 돌려준다.
    if "mealServiceDietInfo" not in meal_result:
        return {}
    rows = meal_result["mealServiceDietInfo"][1]["row"]
    for row in rows:
        if row["MMEAL_SC_CODE"] == LUNCH_CODE:
            return row
    return {}


def join_dish_names(dishes: list[dict]) -> str:
    names = []
    for dish in dishes:
        names.append(dish["name"])
    return DISH_SEPARATOR.join(names)


def format_lunch_message(meal_result: dict, meal_date: str, no_meal_text: str = NO_MEAL_TEXT) -> str:
    # 메시지 모양 (CLAUDE.md 예시):
    # [11월 5일(목) 중식]
    # 쌀밥 / 된장찌개 / 제육볶음 / 배추김치 / 요구르트
    # no_meal_text: 급식이 없을 때 쓸 문구. "내일 급식" 답장에서는 "내일은 급식이 없습니다."를 넘긴다.
    title = f"[{format_date(meal_date)} 중식]"
    lunch_row = find_lunch_row(meal_result)
    if lunch_row == {}:
        return title + "\n" + no_meal_text
    dishes = parse_dishes(lunch_row["DDISH_NM"])
    return title + "\n" + join_dish_names(dishes)


def group_events_by_date(schedule_result: dict) -> dict[str, list[str]]:
    # 학사일정 응답을 {"20261104": ["수업공개의 날", "독서골든벨"], ...} 모양으로 묶는다.
    # 일정이 없는 기간은 "SchoolSchedule" 키 없이 RESULT만 온다. (급식과 같은 모양)
    events_by_date = {}
    if "SchoolSchedule" not in schedule_result:
        return events_by_date
    for row in schedule_result["SchoolSchedule"][1]["row"]:
        event_date = row["AA_YMD"]
        event_name = row["EVENT_NM"].strip()
        if event_name in HIDDEN_EVENT_NAMES:
            continue
        if event_date not in events_by_date:
            events_by_date[event_date] = []
        # 같은 날 같은 행사가 두 번 들어 있는 경우가 있어서 한 번만 넣는다.
        if event_name not in events_by_date[event_date]:
            events_by_date[event_date].append(event_name)
    return events_by_date


def format_schedule_lines(schedule_result: dict) -> list[str]:
    # 날짜마다 한 줄: "11월 4일(수) 수업공개의 날, 독서골든벨"
    lines = []
    events_by_date = group_events_by_date(schedule_result)
    for event_date in sorted(events_by_date):
        lines.append(format_date(event_date) + " " + EVENT_SEPARATOR.join(events_by_date[event_date]))
    return lines


def format_week_schedule_message(schedule_result: dict, start_date: str, end_date: str) -> str:
    # 메시지 모양:
    # [11월 2일(월) ~ 11월 8일(일) 학사일정]
    # 11월 2일(월) 수학 하이챌린지(1,2)
    title = f"[{format_date(start_date)} ~ {format_date(end_date)} 학사일정]"
    lines = format_schedule_lines(schedule_result)
    if lines == []:
        return title + "\n" + NO_SCHEDULE_TEXT
    return title + "\n" + "\n".join(lines)
