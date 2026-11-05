# send_lunch_message.py: .env에 적은 학교의 중식 알림(9단계부터 그날의 학사일정 포함)을 Slack 급식 알림 채널로 보내는 파일
# 매일 아침 자동으로 보내는 일은 main.py가 한다. 이 파일은 원하는 날짜로 직접 한 번 보내 볼 때 쓴다.
# 실행 방법(가상환경을 켠 상태에서): python send_lunch_message.py
# 먼저 setup_slack_token.py를 한 번 실행해 토큰 파일을 만들어 두어야 한다.
#
# 실패하면 관리자 채널로 오류 알림이 가고, 자세한 기록은 logs/bot.log에 남는다. (5단계)

from app.notifier import send_lunch_notification

meal_date = input("날짜를 YYYYMMDD 형식으로 입력하세요 (예: 20261105): ")
if send_lunch_notification(meal_date):
    print("급식 알림을 보냈습니다.")
else:
    print("급식 알림을 보내지 못했습니다. 관리자 채널과 logs/bot.log를 확인하세요.")
