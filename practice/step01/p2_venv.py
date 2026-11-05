# python practice step01\p2 - 가상환경, pip, requirements.txt

# .venv 가상환경을 켜는 명령어
# .venv\Scripts\activate
# .venv 가상환경을 끄는 명령어
# deactivate

# python check_setup.py 명령어로 가상환경이 켜져있는지 확인 가능
# python 위치: 줄에 .venv가 포함되어 있는지 확인

# python -m pip show requests ->
# 결과 Version: 2.34.2
# reqirements.txt 파일의 requests==2.34.2 버전이 설치되어 있는지 확인 가능

# deactivate 명령어로 가상환경을 끄고, python -m pip show requests 명령어를 실행하면
# 결과가 나오지 않음.
# 가상환경이 꺼져있는 상태에서 python check_setup.py 명령어를 실행하면, 
# python 위치에 .venv가 포함되어 있지 않음. 
# (가상환경이 꺼져있기 때문에)
