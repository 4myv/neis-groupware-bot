# setup_slack_token.py: 토큰 자동 교체를 켠 뒤 처음 한 번만 실행하는 파일
# 실행 방법(가상환경을 켠 상태에서): python setup_slack_token.py
#
# .env의 xoxb- 토큰을 "12시간마다 만료되는 토큰 + refresh token"으로 바꿔 secrets/slack_tokens.json에 저장한다.
# 같은 토큰은 한 번만 바꿀 수 있으므로, 저장 파일이 이미 있으면 아무것도 하지 않는다.

from app.auth import exchange_long_lived_token, save_token_response
from app.config import SLACK_BOT_TOKEN, SLACK_TOKEN_FILE

if SLACK_TOKEN_FILE.exists():
    print("토큰 파일이 이미 있어서 다시 바꾸지 않습니다:", SLACK_TOKEN_FILE)
else:
    # 교환은 되돌릴 수 없으므로, 저장할 폴더를 먼저 만들어 두고 교환을 요청한다.
    SLACK_TOKEN_FILE.parent.mkdir(exist_ok=True)
    response_body = exchange_long_lived_token(SLACK_BOT_TOKEN)
    if response_body["ok"]:
        save_token_response(response_body)
        print("토큰을 바꿔 저장했습니다:", SLACK_TOKEN_FILE)
        print("새 토큰은", response_body["expires_in"], "초 뒤에 만료됩니다. 그 전에 프로그램이 알아서 새로 발급받습니다.")
    else:
        print("토큰을 바꾸지 못했습니다. Slack 오류 코드:", response_body["error"])
