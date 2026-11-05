# show_meal_json.py: .env에 적은 학교의 급식 정보를 NEIS에서 받아 원본 그대로 보여 주는 파일
# 실행 방법(가상환경을 켠 상태에서): python show_meal_json.py

import json

from app.config import NEIS_OFFICE_CODE, NEIS_SCHOOL_CODE
from app.neis import fetch_meals

meal_date = input("날짜를 YYYYMMDD 형식으로 입력하세요 (예: 20261105): ")
result = fetch_meals(NEIS_OFFICE_CODE, NEIS_SCHOOL_CODE, meal_date)

# 3단계에서 이 응답을 보기 좋은 메시지로 바꾼다. 지금은 원본의 모양을 그대로 확인한다.
print(json.dumps(result, ensure_ascii=False, indent=2))
