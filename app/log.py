# log.py: 프로그램이 한 일과 오류를 시각과 함께 로그 파일에 남기는 설정
#
# CLAUDE.md 규칙: 모든 요청과 오류는 시각과 함께 로그 파일에 남긴다.
# 다른 파일은 from app.log import logger 로 가져와 logger.info(...), logger.error(...)처럼 쓴다.
# 로그에는 인증키와 토큰을 절대 쓰지 않는다. logs 폴더는 .gitignore에 들어 있다.

import logging
from pathlib import Path

from app.config import PROJECT_ROOT

LOG_FILE: Path = PROJECT_ROOT / "logs" / "bot.log"
LOG_FILE.parent.mkdir(exist_ok=True)

logger = logging.getLogger("lunch_bot")
logger.setLevel(logging.INFO)

# 한 줄 예: 2026-11-05 09:00:00,123 [INFO] NEIS mealServiceDietInfo 호출 성공: 결과 코드 INFO-000
file_handler = logging.FileHandler(LOG_FILE, encoding="utf-8")
file_handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s"))
logger.addHandler(file_handler)
