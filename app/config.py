# config.py: .env 파일에 적어 둔 설정값을 읽어 오는 파일
#
# 인증키를 코드에 직접 쓰면 코드를 GitHub에 올릴 때 키도 같이 올라간다.
# 그래서 비밀 정보는 .env 파일에만 두고, 다른 코드는 모두 이 파일을 거쳐서 값을 읽는다.
# 읽는 곳을 한 군데로 모아 두면 항목 이름이 바뀌어도 이 파일만 고치면 된다.

import os
from pathlib import Path

from dotenv import load_dotenv

# .env 파일의 내용을 환경 변수로 등록한다.
# .env 파일이 없어도 오류를 내지 않으므로, 값이 비었는지는 쓰는 쪽에서 확인해야 한다.
load_dotenv()

# 값이 없을 때 None 대신 빈 문자열("")을 넣는다.
# 그래야 이 값을 쓰는 코드가 "문자열인가?"를 따로 따지지 않고 바로 비교할 수 있다.
NEIS_API_KEY: str = os.getenv("NEIS_API_KEY", "")

# 급식을 조회할 학교의 코드.
# 비밀값은 아니지만, 개발자가 다니는 학교를 저장소에 남기지 않으려고 코드 대신 .env에 둔다.
NEIS_OFFICE_CODE: str = os.getenv("NEIS_OFFICE_CODE", "")
NEIS_SCHOOL_CODE: str = os.getenv("NEIS_SCHOOL_CODE", "")

# Slack 앱 정보. 토큰 교환과 재발급(app/auth.py), 메시지 전송(app/sender.py)에 쓴다.
SLACK_BOT_TOKEN: str = os.getenv("SLACK_BOT_TOKEN", "")
SLACK_CLIENT_ID: str = os.getenv("SLACK_CLIENT_ID", "")
SLACK_CLIENT_SECRET: str = os.getenv("SLACK_CLIENT_SECRET", "")
SLACK_CHANNEL_ID: str = os.getenv("SLACK_CHANNEL_ID", "")

# 토큰 자동 교체를 켜서 토큰이 12시간마다 바뀐다.
# 프로그램이 스스로 고쳐 써야 하는 값이라 .env가 아니라 따로 파일에 저장한다.
# secrets 폴더는 .gitignore에 들어 있어서 GitHub에 올라가지 않는다.
# 어느 폴더에서 실행하든 같은 파일을 찾도록, 이 파일(config.py)의 위치를 기준으로 경로를 만든다.
PROJECT_ROOT: Path = Path(__file__).resolve().parent.parent
SLACK_TOKEN_FILE: Path = PROJECT_ROOT / "secrets" / "slack_tokens.json"
