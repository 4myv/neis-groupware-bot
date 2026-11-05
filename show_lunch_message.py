# show_lunch_message.py: .env에 적은 학교의 중식을 알림 메시지 모양으로 바꿔 보여 주는 파일
# 실행 방법(가상환경을 켠 상태에서): python show_lunch_message.py

from app.config import NEIS_OFFICE_CODE, NEIS_SCHOOL_CODE
from app.formatter import format_lunch_message
from app.neis import fetch_meals

meal_date = input("날짜를 YYYYMMDD 형식으로 입력하세요 (예: 20261105): ")
result = fetch_meals(NEIS_OFFICE_CODE, NEIS_SCHOOL_CODE, meal_date)
print(format_lunch_message(result, meal_date))
