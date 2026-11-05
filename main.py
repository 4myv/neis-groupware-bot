# main.py: 콜백 서버와 정기 알림 스케줄러를 한 프로그램으로 실행하는 파일 (9단계)
# 실행 방법(가상환경을 켠 상태에서, 프로젝트 최상위 폴더에서): python main.py
# 끄는 방법: 이 프로그램을 실행한 창에서 Ctrl+C
#
# 스케줄러는 따로 일하는 줄(스레드)에서 시계를 보고, 서버는 이 파일이 실행되는 원래 줄에서 요청을 기다린다.
# 그래서 프로그램 하나로 "매일 아침 알림"과 "명령어 답장"을 함께 한다.

import uvicorn

from app.log import logger
from app.scheduler import DAILY_JOB_ID, create_scheduler
from app.server import app

# 6단계부터 써 온 주소와 포트. 터널도 이 주소로 연결한다.
HOST: str = "127.0.0.1"
PORT: int = 8000

scheduler = create_scheduler()
# start()는 스케줄러를 따로 일하는 줄에서 돌려 놓고 바로 돌아온다. (공식 문서)
scheduler.start()
next_run_time = scheduler.get_job(DAILY_JOB_ID).next_run_time
print("정기 알림 다음 실행 시각:", next_run_time)
logger.info(f"프로그램 시작: 정기 알림 다음 실행 시각 {next_run_time}")

try:
    # 서버를 켠다. Ctrl+C로 끌 때까지 이 줄에서 기다린다.
    uvicorn.run(app, host=HOST, port=PORT)
except KeyboardInterrupt:
    # uvicorn은 Ctrl+C를 받으면 서버를 정리한 뒤, 받은 Ctrl+C 신호를 다시 보낸다. (uvicorn 코드에서 확인)
    # 그래서 여기서 KeyboardInterrupt가 생길 수 있다. 정상적으로 끄는 것이므로 오류로 보지 않고 넘어간다.
    pass

# 서버가 꺼진 뒤에 실행된다. 스케줄러도 정리하고 끝낸다.
scheduler.shutdown()
logger.info("프로그램 종료")
print("프로그램을 종료했습니다.")
