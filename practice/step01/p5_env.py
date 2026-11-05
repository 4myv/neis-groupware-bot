# python practice step01\p5 - .env, 환경 변수, import, None

import os

PRACTICE_NAME: str = os.getenv("PRACTICE_NAME", "")

if PRACTICE_NAME == "":
    print("PRACTICE_NAME이 비어 있습니다.")
else:
    print("PRACTICE_NAME:", PRACTICE_NAME)

print("기본값 없이 읽으면:", os.getenv("PRACTICE_NAME"))

# 실행 결과
# PRACTICE_NAME이 비어 있습니다
# 기본값 없이 읽으면: None

# $env:PRACTICE_NAME = "급식봇" 실행 후

# PRACTICE_NAME: 급식봇
# 기본값 없이 읽으면: 급식봇