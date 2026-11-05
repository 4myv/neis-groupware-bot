# neis.py: NEIS 교육정보 개방 포털의 Open API를 호출하는 파일
#
# 정기 알림과 명령어 응답이 모두 이 파일을 거쳐 NEIS 데이터를 가져온다.
# 그래서 NEIS 주소나 요청 방식이 바뀌어도 이 파일만 고치면 된다.
# 요청 주소, 요청 인자 이름은 NEIS 포털의 Open API 명세에서 확인했다. (docs/step02-devlog.md 참고)

import time

import requests

from app.config import NEIS_API_KEY
from app.log import logger

# 모든 NEIS Open API 주소의 공통 앞부분. 뒤에 서비스 이름을 붙여 쓴다.
NEIS_BASE_URL: str = "https://open.neis.go.kr/hub/"

# 응답을 기다릴 최대 시간(초).
# 정해 두지 않으면 서버가 답하지 않을 때 프로그램이 끝없이 기다린다.
REQUEST_TIMEOUT_SECONDS: int = 10

# 실패했을 때 다시 시도하기 전에 기다릴 시간(초). CLAUDE.md 규칙: "잠시 후 한 번 재시도"
RETRY_WAIT_SECONDS: int = 3

# 이 결과 코드만 쓸 수 있는 응답으로 본다. (NEIS 공식 명세, docs/step02-devlog.md 6번)
# INFO-000은 정상 처리, INFO-200은 데이터 없음이다. 주말·방학에 급식이 없는 것은 오류가 아니다.
USABLE_RESULT_CODES: list[str] = ["INFO-000", "INFO-200"]


class NeisError(Exception):
    # NEIS에서 쓸 수 있는 응답을 받지 못했을 때 일으키는 오류. 메시지에 실패 원인을 담는다.
    pass


def get_result(response_body: dict, service_name: str) -> dict:
    # 결과 코드와 설명이 든 RESULT 딕셔너리를 꺼낸다. 예: {"CODE": "INFO-000", "MESSAGE": "정상 처리되었습니다."}
    # 데이터가 없거나 오류일 때: {"RESULT": {...}}
    # 정상일 때: {"서비스이름": [{"head": [{"list_total_count": 2}, {"RESULT": {...}}]}, {"row": [...]}]}
    if "RESULT" in response_body:
        return response_body["RESULT"]
    return response_body[service_name][0]["head"][1]["RESULT"]


def try_neis_once(service_name: str, params: dict) -> dict:
    # NEIS를 한 번 불러 본다. 쓸 수 있는 응답이면 돌려주고, 아니면 원인을 담아 NeisError를 일으킨다.
    try:
        response = requests.get(
            NEIS_BASE_URL + service_name,
            params=params,
            timeout=REQUEST_TIMEOUT_SECONDS,
        )
        response_body = response.json()
        result = get_result(response_body, service_name)
    except (requests.RequestException, ValueError, KeyError, IndexError) as error:
        # requests의 오류 메시지에는 인증키(KEY)가 붙은 요청 주소가 섞여 있다. (5단계에서 실제로 확인)
        # 그래서 메시지는 쓰지 않고 오류의 종류 이름만 원인으로 남긴다.
        # from None: 원래 오류(인증키가 든 메시지)를 화면에 함께 보여 주지 않게 한다.
        raise NeisError(f"응답을 받지 못함({type(error).__name__})") from None
    if result["CODE"] not in USABLE_RESULT_CODES:
        # NEIS가 보낸 결과 코드와 공식 설명을 원인으로 남긴다. 예: ERROR-290 인증키가 유효하지 않습니다.
        raise NeisError(f"{result['CODE']} {result['MESSAGE']}")
    logger.info(f"NEIS {service_name} 호출 성공: 결과 코드 {result['CODE']}")
    return response_body


def call_neis_api(service_name: str, search_conditions: dict) -> dict:
    # 모든 NEIS API에 똑같이 붙는 기본 인자.
    # Type을 json으로 정하지 않으면 NEIS는 기본값인 xml로 답한다.
    params = {
        "KEY": NEIS_API_KEY,
        "Type": "json",
        "pIndex": 1,
        "pSize": 100,
    }

    # 서비스마다 다른 조건(학교 이름, 날짜 등)을 기본 인자에 덧붙인다.
    for name in search_conditions:
        params[name] = search_conditions[name]

    try:
        return try_neis_once(service_name, params)
    except NeisError as error:
        # 잠시 기다렸다가 한 번만 다시 시도한다. (CLAUDE.md 예외 처리 규칙)
        logger.warning(f"NEIS {service_name} 호출 실패: {error} → {RETRY_WAIT_SECONDS}초 뒤 다시 시도")
        time.sleep(RETRY_WAIT_SECONDS)

    try:
        return try_neis_once(service_name, params)
    except NeisError as error:
        logger.warning(f"NEIS {service_name} 다시 시도도 실패: {error}")
        raise NeisError(f"NEIS {service_name} 호출이 두 번 모두 실패했습니다. 원인: {error}") from None


def fetch_schools(school_name: str) -> dict:
    # 학교 이름의 일부만 넣어도 여러 학교가 함께 나올 수 있다. (예: "서울고" → 9곳)
    search_conditions = {"SCHUL_NM": school_name}
    return call_neis_api("schoolInfo", search_conditions)


def fetch_meals(office_code: str, school_code: str, meal_date: str) -> dict:
    # 중식·석식을 가리지 않고 그날의 급식을 모두 가져온다.
    # 중식만 고르는 일은 app/formatter.py가 한다.
    search_conditions = {
        "ATPT_OFCDC_SC_CODE": office_code,
        "SD_SCHUL_CODE": school_code,
        "MLSV_YMD": meal_date,
    }
    return call_neis_api("mealServiceDietInfo", search_conditions)
