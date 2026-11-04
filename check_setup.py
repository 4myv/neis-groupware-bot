# check_setup.py: 1단계 환경 준비가 잘 되었는지 확인하는 파일
# 실행 방법(가상환경을 켠 상태에서): python check_setup.py

import sys

from app.config import NEIS_API_KEY

# 가상환경의 Python으로 실행되었는지 눈으로 확인하려고 Python의 위치를 보여 준다.
# 위치가 .venv 폴더 안이면 가상환경이 켜진 상태다.
print("Python 버전:", sys.version)
print("Python 위치:", sys.executable)

# 인증키 값 자체는 화면에 보여 주지 않는다. 화면 캡처나 기록을 통해 새어 나갈 수 있어서다.
if NEIS_API_KEY == "":
    print("NEIS_API_KEY: 비어 있음 (.env 파일을 확인하세요)")
else:
    print("NEIS_API_KEY: 입력됨")
