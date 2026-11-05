# python practice step01\p6 - from...import, 패키지, 비밀값을 출력하지 않기

from app.config import NEIS_API_KEY, NEIS_SCHOOL_CODE

if NEIS_API_KEY == "":
    print("NEIS_API_KEY:", "비어 있음")
else:
    print("NEIS_API_KEY:", "입력됨")

if NEIS_SCHOOL_CODE == "":
    print("NEIS_SCHOOL_CODE:", "비어 있음")
else:
    print("NEIS_SCHOOL_CODE:", "입력됨")

# 이 파일은 app 패키지를 가져오므로, 아래처럼 -m으로 실행 
# (.py를 붙이지 않고 \ 대신 .을 사용)
# python -m practice.step01.p6_config_check

# 왜 -m으로 실행하나?
# python practice\step01\파일.py로 실행하면, 
# python은 그 파일이 있는 폴더(practice\step01)에서 app을 찾는다.
# 거기엔 app이 없어서 ModuleNotFoundError: No module name 'app'이 발생함.
# python -m practice.step01.파일로 실행하면 지금 폴더(프로젝트 맨 위)에서 찾음.
# 그래서 app을 찾을 수 있음

# 실행 결과
# NEIS_API_KEY: 입력됨
# NEIS_SCHOOL_CODE: 입력됨