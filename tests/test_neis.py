# test_neis.py: NEIS 응답에서 결과(코드와 설명)를 꺼내고, 쓸 수 있는 응답인지 판단하는 규칙을 확인하는 테스트
# 실행 방법(가상환경을 켠 상태에서, 프로젝트 최상위 폴더에서): python -m pytest
#
# NEIS에 실제로 요청하지 않는다. 응답 모양은 docs/step02-devlog.md 4번의 실제 응답을 줄여서 썼다.

from app.neis import USABLE_RESULT_CODES, get_result

SUCCESS = {
    "mealServiceDietInfo": [
        {"head": [{"list_total_count": 1}, {"RESULT": {"CODE": "INFO-000", "MESSAGE": "정상 처리되었습니다."}}]},
        {"row": []},
    ]
}
NO_DATA = {"RESULT": {"CODE": "INFO-200", "MESSAGE": "해당하는 데이터가 없습니다."}}
WRONG_KEY = {"RESULT": {"CODE": "ERROR-290", "MESSAGE": "인증키가 유효하지 않습니다."}}


def test_result_of_success():
    assert get_result(SUCCESS, "mealServiceDietInfo")["CODE"] == "INFO-000"


def test_result_of_no_data():
    assert get_result(NO_DATA, "mealServiceDietInfo")["CODE"] == "INFO-200"


def test_result_of_error_keeps_official_message():
    assert get_result(WRONG_KEY, "mealServiceDietInfo") == {"CODE": "ERROR-290", "MESSAGE": "인증키가 유효하지 않습니다."}


def test_no_data_is_usable_because_weekends_are_normal():
    assert "INFO-200" in USABLE_RESULT_CODES


def test_wrong_key_is_not_usable():
    assert "ERROR-290" not in USABLE_RESULT_CODES
