# send_lunch_message.py: .env에 적은 학교의 중식 메시지를 Slack 급식 알림 채널로 보내는 파일
# 실행 방법(가상환경을 켠 상태에서): python send_lunch_message.py
# 먼저 setup_slack_token.py를 한 번 실행해 토큰 파일을 만들어 두어야 한다.

from app.config import NEIS_OFFICE_CODE, NEIS_SCHOOL_CODE, SLACK_CHANNEL_ID
from app.formatter import format_lunch_message
from app.neis import fetch_meals
from app.sender import post_message

meal_date = input("날짜를 YYYYMMDD 형식으로 입력하세요 (예: 20261105): ")
result = fetch_meals(NEIS_OFFICE_CODE, NEIS_SCHOOL_CODE, meal_date)
message = format_lunch_message(result, meal_date)
print(message)

slack_response = post_message(SLACK_CHANNEL_ID, message)
if slack_response["ok"]:
    print("Slack으로 보냈습니다.")
else:
    print("Slack으로 보내지 못했습니다. 오류 코드:", slack_response["error"])
