# test_formatter.py: app/formatter.py의 변환 함수가 규칙대로 동작하는지 확인하는 테스트
# 실행 방법(가상환경을 켠 상태에서, 프로젝트 최상위 폴더에서): python -m pytest
#
# 테스트 데이터는 공개된 예시 학교(서울고등학교)의 실제 NEIS 응답(2026-11-05)을 줄여서 썼다.
# 응답 원본은 docs/step02-devlog.md 4번 [B], [C]에 있다.

from app.formatter import (
    extract_allergy_numbers,
    find_lunch_row,
    format_daily_message,
    format_date,
    format_lunch_message,
    format_today_schedule,
    format_week_schedule_message,
    parse_dishes,
    remove_allergy_numbers,
    split_dishes,
)

REAL_LUNCH_DDISH = (
    "흑미밥 <br/>부대찌개 (1.2.5.6.9.10.12.13.15.16)<br/>호박볶음 (5.6)"
    "<br/>오지치즈스틱 (1.2.5.6.10.12.13)<br/>고등어구이 (1.5.6.7.13)<br/>백김치 (9)"
)

MEAL_RESULT_WITH_LUNCH = {
    "mealServiceDietInfo": [
        {"head": [{"list_total_count": 2}, {"RESULT": {"CODE": "INFO-000", "MESSAGE": "정상 처리되었습니다."}}]},
        {
            "row": [
                {"MMEAL_SC_CODE": "2", "MMEAL_SC_NM": "중식", "MLSV_YMD": "20261105", "DDISH_NM": REAL_LUNCH_DDISH},
                {"MMEAL_SC_CODE": "3", "MMEAL_SC_NM": "석식", "MLSV_YMD": "20261105", "DDISH_NM": "배추김치 (9)"},
            ]
        },
    ]
}

MEAL_RESULT_DINNER_ONLY = {
    "mealServiceDietInfo": [
        {"head": [{"list_total_count": 1}, {"RESULT": {"CODE": "INFO-000", "MESSAGE": "정상 처리되었습니다."}}]},
        {"row": [{"MMEAL_SC_CODE": "3", "MMEAL_SC_NM": "석식", "MLSV_YMD": "20261105", "DDISH_NM": "배추김치 (9)"}]},
    ]
}

MEAL_RESULT_NO_DATA = {"RESULT": {"CODE": "INFO-200", "MESSAGE": "해당하는 데이터가 없습니다."}}


# ---- 줄바꿈 태그를 구분자로 ----

def test_split_dishes_claude_md_example():
    assert split_dishes("쌀밥<br/>된장찌개") == ["쌀밥", "된장찌개"]


def test_split_dishes_removes_spaces_around_tag():
    assert split_dishes("흑미밥 <br/>백김치 (9)") == ["흑미밥", "백김치 (9)"]


# ---- 알레르기 번호 지우기 ----

def test_remove_allergy_numbers_claude_md_example():
    assert remove_allergy_numbers("된장찌개(5.6.9.)") == "된장찌개"


def test_remove_allergy_numbers_real_format():
    assert remove_allergy_numbers("부대찌개 (1.2.5.6.9.10.12.13.15.16)") == "부대찌개"


def test_remove_allergy_numbers_without_numbers():
    assert remove_allergy_numbers("흑미밥") == "흑미밥"


def test_remove_allergy_numbers_keeps_parentheses_in_name():
    assert remove_allergy_numbers("떡볶이(국물)") == "떡볶이(국물)"


# 아래 두 메뉴 이름은 다른 지역 공개 학교의 실제 응답에서 찾은 모양이다. (step03 개발 기록 4번)
def test_remove_allergy_numbers_keeps_amount_in_parentheses():
    assert remove_allergy_numbers("사과(1/2)") == "사과(1/2)"


def test_allergy_numbers_after_name_with_parentheses():
    assert remove_allergy_numbers("혼합잡곡밥(연) (5)") == "혼합잡곡밥(연)"
    assert extract_allergy_numbers("혼합잡곡밥(연) (5)") == ["5"]


# ---- 알레르기 번호는 따로 보관 ----

def test_extract_allergy_numbers_claude_md_example():
    assert extract_allergy_numbers("된장찌개(5.6.9.)") == ["5", "6", "9"]


def test_extract_allergy_numbers_real_format():
    assert extract_allergy_numbers("고등어구이 (1.5.6.7.13)") == ["1", "5", "6", "7", "13"]


def test_extract_allergy_numbers_without_numbers():
    assert extract_allergy_numbers("흑미밥") == []


def test_parse_dishes_keeps_name_and_allergy_numbers():
    assert parse_dishes("흑미밥 <br/>호박볶음 (5.6)") == [
        {"name": "흑미밥", "allergy_numbers": []},
        {"name": "호박볶음", "allergy_numbers": ["5", "6"]},
    ]


# ---- 날짜를 읽기 쉬운 형식으로 ----

def test_format_date_claude_md_example():
    assert format_date("20261105") == "11월 5일(목)"


def test_format_date_sunday():
    assert format_date("20261108") == "11월 8일(일)"


def test_format_date_new_year():
    assert format_date("20270101") == "1월 1일(금)"


# ---- 중식 고르기 ----

def test_find_lunch_row_picks_lunch():
    assert find_lunch_row(MEAL_RESULT_WITH_LUNCH)["MMEAL_SC_NM"] == "중식"


def test_find_lunch_row_when_no_data():
    assert find_lunch_row(MEAL_RESULT_NO_DATA) == {}


def test_find_lunch_row_when_only_dinner():
    assert find_lunch_row(MEAL_RESULT_DINNER_ONLY) == {}


# ---- 메시지 전체 ----

def test_format_lunch_message_real_data():
    assert format_lunch_message(MEAL_RESULT_WITH_LUNCH, "20261105") == (
        "[11월 5일(목) 중식]\n"
        "흑미밥 / 부대찌개 / 호박볶음 / 오지치즈스틱 / 고등어구이 / 백김치"
    )


def test_format_lunch_message_no_data_is_normal():
    assert format_lunch_message(MEAL_RESULT_NO_DATA, "20261108") == (
        "[11월 8일(일) 중식]\n"
        "오늘은 급식이 없습니다."
    )


def test_format_lunch_message_with_tomorrow_wording():
    assert format_lunch_message(MEAL_RESULT_NO_DATA, "20261108", "내일은 급식이 없습니다.") == (
        "[11월 8일(일) 중식]\n"
        "내일은 급식이 없습니다."
    )


# ---- 학사일정 (8단계) ----
# 공개된 예시 학교(서울고등학교)의 실제 응답(2026-11-02 ~ 11-08)을 필요한 키만 남겨 줄였다.
# 같은 날 같은 행사가 두 번 오는 경우(부산고 실제 응답)도 넣었다.

def schedule_row(aa_ymd, event_nm):
    return {"AA_YMD": aa_ymd, "EVENT_NM": event_nm, "SBTR_DD_SC_NM": "해당없음"}


SCHEDULE_RESULT_THIS_WEEK = {
    "SchoolSchedule": [
        {"head": [{"list_total_count": 8}, {"RESULT": {"CODE": "INFO-000", "MESSAGE": "정상 처리되었습니다."}}]},
        {
            "row": [
                schedule_row("20261102", "수학 하이챌린지(1,2)"),
                schedule_row("20261103", "정보 하이챌린지"),
                schedule_row("20261104", "수업공개의 날"),
                schedule_row("20261104", "독서골든벨"),
                schedule_row("20261105", "과학 하이챌린지(1,2)"),
                schedule_row("20261106", "학교폭력예방교육"),
                schedule_row("20261106", "학교폭력예방교육"),
                schedule_row("20261107", "토요휴업일"),
            ]
        },
    ]
}

SCHEDULE_RESULT_NO_DATA = {"RESULT": {"CODE": "INFO-200", "MESSAGE": "해당하는 데이터가 없습니다."}}


def test_week_schedule_groups_by_date_and_hides_saturday_holiday():
    assert format_week_schedule_message(SCHEDULE_RESULT_THIS_WEEK, "20261102", "20261108") == (
        "[11월 2일(월) ~ 11월 8일(일) 학사일정]\n"
        "11월 2일(월) 수학 하이챌린지(1,2)\n"
        "11월 3일(화) 정보 하이챌린지\n"
        "11월 4일(수) 수업공개의 날, 독서골든벨\n"
        "11월 5일(목) 과학 하이챌린지(1,2)\n"
        "11월 6일(금) 학교폭력예방교육"
    )


def test_week_schedule_without_events():
    assert format_week_schedule_message(SCHEDULE_RESULT_NO_DATA, "20261228", "20270103") == (
        "[12월 28일(월) ~ 1월 3일(일) 학사일정]\n"
        "없음"
    )


# ---- 정기 알림의 오늘의 학사일정 (9단계) ----

def test_today_schedule_with_two_events():
    assert format_today_schedule(SCHEDULE_RESULT_THIS_WEEK, "20261104") == (
        "[오늘의 학사일정]\n"
        "수업공개의 날, 독서골든벨"
    )


def test_today_schedule_on_saturday_holiday_is_none():
    # 토요휴업일만 있는 날은 숨기고 나면 일정이 없다.
    assert format_today_schedule(SCHEDULE_RESULT_THIS_WEEK, "20261107") == (
        "[오늘의 학사일정]\n"
        "없음"
    )


def test_today_schedule_without_data():
    assert format_today_schedule(SCHEDULE_RESULT_NO_DATA, "20261108") == (
        "[오늘의 학사일정]\n"
        "없음"
    )


def test_daily_message_has_blank_line_between_parts():
    lunch_message = format_lunch_message(MEAL_RESULT_WITH_LUNCH, "20261105")
    schedule_section = format_today_schedule(SCHEDULE_RESULT_THIS_WEEK, "20261105")
    assert format_daily_message(lunch_message, schedule_section) == (
        "[11월 5일(목) 중식]\n"
        "흑미밥 / 부대찌개 / 호박볶음 / 오지치즈스틱 / 고등어구이 / 백김치\n"
        "\n"
        "[오늘의 학사일정]\n"
        "과학 하이챌린지(1,2)"
    )
