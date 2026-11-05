# reinstall_slack_app.py: Slack 앱의 권한을 바꾼 뒤, 앱을 다시 설치하고 새 토큰을 저장하는 파일
# 실행 방법(가상환경을 켠 상태에서): python reinstall_slack_app.py
#
# 앱 설정 화면에 다시 설치 버튼이 없어서, 공식 문서 "Installing with OAuth"의 설치 과정을 직접 밟는다.
# 1) 화면에 나온 주소를 Slack에 로그인된 브라우저에서 열고 Allow를 누른다.
# 2) 브라우저가 https://localhost/... 로 이동하며 "연결할 수 없음" 화면이 나온다. 정상이다.
# 3) 그 화면의 주소창 주소 전체를 복사해 이 프로그램에 붙여 넣는다. (채팅에는 붙여 넣지 않는다)

import secrets

from app.auth import build_authorize_url, exchange_code, read_code_from_redirect, save_token_response

# 이번 설치에서만 쓰는 무작위 값. 돌아온 주소의 state와 같아야 우리가 시작한 설치로 믿는다.
state = secrets.token_urlsafe(16)

print("1) 아래 주소를 Slack에 로그인된 브라우저에서 열고 Allow를 누르세요.")
print(build_authorize_url(state))
print()
redirected_url = input("2) 이동한 화면의 주소창 주소 전체를 붙여 넣고 Enter를 누르세요: ")

code = read_code_from_redirect(redirected_url, state)
if code == "":
    print("이 주소에서 쓸 수 있는 code를 찾지 못했습니다. state가 다르거나, Allow를 누르지 않았거나, 주소가 잘렸습니다.")
else:
    response_body = exchange_code(code)
    if response_body["ok"] and "refresh_token" in response_body:
        save_token_response(response_body)
        print("다시 설치를 마치고 새 토큰을 저장했습니다. 이 앱의 권한:", response_body["scope"])
    elif response_body["ok"]:
        # 자동 교체를 켠 앱은 refresh_token이 함께 와야 한다. 없으면 저장하지 않아 지금 토큰 파일을 지킨다.
        print("토큰은 받았지만 refresh_token이 없어 저장하지 않았습니다. 에이전트에게 알려 주세요.")
    else:
        print("토큰을 받지 못했습니다. Slack 오류 코드:", response_body["error"])
