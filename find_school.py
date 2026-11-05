# find_school.py: 학교 이름으로 NEIS 학교 코드를 찾는 파일
# 실행 방법(가상환경을 켠 상태에서): python find_school.py
#
# 화면에 나온 결과에서 ATPT_OFCDC_SC_CODE(시도교육청코드)와 SD_SCHUL_CODE(행정표준코드)를 찾아
# .env의 NEIS_OFFICE_CODE, NEIS_SCHOOL_CODE에 적는다.

import json

from app.neis import fetch_schools

school_name = input("학교 이름을 입력하세요: ")
result = fetch_schools(school_name)

# NEIS가 돌려준 응답을 손대지 않고 그대로 보여 준다.
# ensure_ascii=False는 한글을 서 같은 기호 대신 글자 그대로 보여 주려고 넣는다.
print(json.dumps(result, ensure_ascii=False, indent=2))
