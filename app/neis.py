# neis.py: NEIS 교육정보 개방 포털의 Open API를 호출하는 파일
#
# 정기 알림과 명령어 응답이 모두 이 파일을 거쳐 NEIS 데이터를 가져온다.
# 그래서 NEIS 주소나 요청 방식이 바뀌어도 이 파일만 고치면 된다.
# 요청 주소, 요청 인자 이름은 NEIS 포털의 Open API 명세에서 확인했다. (docs/step02-devlog.md 참고)

import requests

from app.config import NEIS_API_KEY

# 모든 NEIS Open API 주소의 공통 앞부분. 뒤에 서비스 이름을 붙여 쓴다.
NEIS_BASE_URL: str = "https://open.neis.go.kr/hub/"

# 응답을 기다릴 최대 시간(초).
# 정해 두지 않으면 서버가 답하지 않을 때 프로그램이 끝없이 기다린다.
REQUEST_TIMEOUT_SECONDS: int = 10


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

    response = requests.get(
        NEIS_BASE_URL + service_name,
        params=params,
        timeout=REQUEST_TIMEOUT_SECONDS,
    )
    return response.json()


def fetch_schools(school_name: str) -> dict:
    # 학교 이름의 일부만 넣어도 여러 학교가 함께 나올 수 있다. (예: "서울고" → 9곳)
    search_conditions = {"SCHUL_NM": school_name}
    return call_neis_api("schoolInfo", search_conditions)


def fetch_meals(office_code: str, school_code: str, meal_date: str) -> dict:
    # 중식·석식을 가리지 않고 그날의 급식을 모두 가져온다.
    # 중식만 고르는 일은 3단계(데이터 변환)에서 한다.
    search_conditions = {
        "ATPT_OFCDC_SC_CODE": office_code,
        "SD_SCHUL_CODE": school_code,
        "MLSV_YMD": meal_date,
    }
    return call_neis_api("mealServiceDietInfo", search_conditions)
