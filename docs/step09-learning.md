# 9단계 학습 정리: 통합 (정기 알림 스케줄러 + 콜백 서버)

## 이 문서를 다 읽으면 할 수 있게 되는 것

1. "매일 아침 7시 30분에 이 함수를 실행해라"를 APScheduler로 예약하는 코드를 읽고 설명할 수 있다.
2. 프로그램 하나가 "정해진 시각에 알림 보내기"와 "요청 기다리기"를 동시에 하는 원리(스레드)를 설명할 수 있다.
3. `except Exception`과 `KeyboardInterrupt`(Ctrl+C)가 어떻게 다른지 설명할 수 있다.

## 읽기 전에

- 코드 예시는 모두 실제로 실행한 결과를 붙였습니다. 긴 파일 경로는 `예시.py`처럼 줄여 적었습니다.
- 시각이 들어간 결과는 이 문서를 쓴 날(2026-11-05)에 실행한 것입니다. 실행하는 때에 따라 다르게 나옵니다.
- 앞 단계에서 설명한 것은 "step05 참고"처럼 적었습니다.

---

## 1. 이번 단계에서 새로 나온 것

**개념**

1. 스케줄러와 "cron" 방식
2. 스레드: 한 프로그램 안에서 두 가지 일을 함께 하기

**Python 문법과 라이브러리**

3. APScheduler `BackgroundScheduler`: 예약하고, 시작하고, 끝내기
4. 다음 실행 시각 `next_run_time`과 `+09:00`
5. 늦어도 실행하기: `misfire_grace_time`, `coalesce`
6. `except Exception`: 어떤 오류든 잡기
7. `KeyboardInterrupt`: Ctrl+C로 생기는 예외
8. `uvicorn.run`: 코드 안에서 서버 켜기
9. 숫자 설정 읽기: `read_int_setting`

**앞 단계에서 설명한 것**

- step01: `os.getenv`, `.env`, `python 파일명.py`로 실행하기
- step05: `try` / `except`, `type(error).__name__`, `pass`, `logger`
- step06: Uvicorn, `127.0.0.1`, 포트 8000
- step07: `int()`
- step08: `date.today()`, `to_yyyymmdd`, 함수를 값으로 넘기기, `group_events_by_date`

---

## 2. 하나씩 설명

### 2-1. 스케줄러와 "cron" 방식

**설명**

**스케줄러**는 "정해진 시각이 되면 이 일을 해라"를 기억해 두었다가, 그 시각에 일을 실행해 주는 프로그램입니다.

지금까지 급식 알림은 `python send_lunch_message.py`를 사람이 직접 실행해야 나갔습니다. 9단계부터는 스케줄러가 매일 아침 알아서 보냅니다.

**cron**(크론)은 "몇 시 몇 분에"처럼 달력과 시계로 때를 정하는 방식입니다. 이름은 오래된 리눅스 예약 프로그램에서 왔습니다.

`hour=7, minute=30`처럼 시와 분만 정하면 **매일** 7시 30분입니다. 정하지 않은 날짜와 요일은 "아무 날이나"라는 뜻이 됩니다. (APScheduler 공식 문서)

**비유**

휴대폰의 "매일 반복" 알람입니다. 한 번 맞춰 두면 매일 그 시각에 울립니다.

**Java 비교**

Spring의 `@Scheduled(cron = "0 30 7 * * *")`와 같은 역할입니다. Spring은 cron을 글자 한 줄로 쓰고, APScheduler는 `hour=7, minute=30`처럼 이름을 붙여 씁니다.

**자주 하는 실수: 프로그램을 꺼 둔다**

스케줄러는 프로그램이 **켜져 있는 동안에만** 시계를 봅니다. 7시 30분에 프로그램이 꺼져 있거나 PC가 꺼져 있으면 알림이 나가지 않습니다.

---

### 2-2. 스레드: 한 프로그램 안에서 두 가지 일을 함께 하기

**설명**

프로그램은 보통 코드를 위에서 아래로 **한 줄씩 차례로** 실행합니다. 이 실행 흐름을 **스레드**(thread, "실")라고 부릅니다.

그런데 서버(`uvicorn.run`)는 요청을 기다리느라 그 줄에서 멈춰 있습니다. 같은 흐름에서는 7시 30분이 됐는지 볼 수가 없습니다.

그래서 `BackgroundScheduler`는 **새 스레드**를 하나 더 만들어, 그 스레드에서 시계를 봅니다. 원래 스레드는 서버 일을 하고, 새 스레드는 스케줄러 일을 합니다.

**비유**

가게에 점원이 두 명 있는 것입니다. 한 명(원래 스레드)은 계산대에서 손님(요청)을 기다리고, 다른 한 명(새 스레드)은 시계를 보다가 7시 30분에 안내 방송(알림)을 합니다.

**작은 예시** (`예시.py`)

```python
import time

from apscheduler.schedulers.background import BackgroundScheduler


def tick() -> None:
    print("스케줄러:", time.strftime("%H:%M:%S"))


scheduler = BackgroundScheduler()
scheduler.add_job(tick, "cron", second="*")
scheduler.start()
print("start()가 바로 돌아왔습니다")
time.sleep(3)
print("원래 코드: 3초 기다리는 동안 스케줄러가 따로 일했습니다")
scheduler.shutdown()
```

결과:

```
start()가 바로 돌아왔습니다
스케줄러: 18:28:49
스케줄러: 18:28:50
스케줄러: 18:28:51
원래 코드: 3초 기다리는 동안 스케줄러가 따로 일했습니다
```

- `second="*"`는 "매초"라는 뜻입니다. 결과를 빨리 보려고 이 예시에서만 썼습니다.
- 원래 코드가 `time.sleep(3)`으로 멈춰 있는 동안에도, 스케줄러는 다른 스레드에서 매초 `tick`을 실행했습니다.

**이 프로젝트에서는**: `main.py`가 스케줄러를 시작한 뒤 `uvicorn.run`으로 서버를 켭니다. 서버가 요청을 기다리는 동안, 스케줄러는 다른 스레드에서 7시 30분을 기다립니다.

**Java 비교**

Java의 `new Thread(...).start()`와 같은 생각입니다. Spring의 `@Scheduled`도 따로 스레드를 만들어 실행합니다.

**자주 하는 실수: 서버를 먼저 켜고, 그 아래에 스케줄러를 시작한다**

```python
uvicorn.run(app, host=HOST, port=PORT)   # 여기서 서버가 꺼질 때까지 멈춘다
scheduler.start()                        # 서버가 꺼진 뒤에야 실행된다
```

`uvicorn.run`은 서버가 꺼질 때까지 돌아오지 않습니다. 그래서 스케줄러는 **반드시 먼저** 시작해야 합니다.

---

### 2-3. APScheduler `BackgroundScheduler`: 예약하고, 시작하고, 끝내기

**설명**

APScheduler는 함수를 정해진 때에 실행해 주는 라이브러리입니다. 이번에 쓴 기능은 네 가지입니다.

| 코드 | 하는 일 |
| --- | --- |
| `BackgroundScheduler()` | 새 스레드에서 도는 스케줄러를 만든다 |
| `scheduler.add_job(함수, "cron", hour=..., minute=..., id=...)` | 함수를 예약한다. `id`는 나중에 찾을 때 쓰는 이름 |
| `scheduler.start()` | 스케줄러를 켠다. 켜 놓고 **바로 돌아온다** |
| `scheduler.shutdown()` | 스케줄러를 끈다 |

`add_job`에 함수를 넘길 때는 괄호를 붙이지 않습니다. 스케줄러가 나중에 실행해야 하기 때문입니다. (step08 2-9 참고)

**이 프로젝트 코드** (`app/scheduler.py` 38~52줄)

```python
def create_scheduler() -> BackgroundScheduler:
    scheduler = BackgroundScheduler()
    scheduler.add_job(
        send_today_notification,
        "cron",
        hour=NOTIFY_HOUR,
        minute=NOTIFY_MINUTE,
        id=DAILY_JOB_ID,
        misfire_grace_time=MISFIRE_GRACE_SECONDS,
        coalesce=True,
    )
    return scheduler
```

(주석은 줄였습니다.) `misfire_grace_time`, `coalesce`는 2-5에서 설명합니다.

**Java 비교**

```java
ScheduledExecutorService scheduler = Executors.newSingleThreadScheduledExecutor();
scheduler.scheduleAtFixedRate(this::sendTodayNotification, initialDelay, 24, TimeUnit.HOURS);
scheduler.shutdown();
```

Java의 이 방법은 "몇 시간마다"로 정합니다. APScheduler의 cron은 "몇 시 몇 분에"로 정합니다.

**자주 하는 실수: `start()`를 두 번 부른다**

```python
from apscheduler.schedulers.background import BackgroundScheduler

scheduler = BackgroundScheduler()
scheduler.start()
scheduler.start()
```

결과:

```
apscheduler.schedulers.SchedulerAlreadyRunningError: Scheduler is already running
```

이미 켜진 스케줄러는 다시 켤 수 없습니다. "이미 돌고 있다"는 뜻의 오류가 납니다.

---

### 2-4. 다음 실행 시각 `next_run_time`과 `+09:00`

**설명**

`scheduler.get_job(이름)`은 `add_job`에서 `id`로 붙인 이름으로 예약을 찾아 줍니다.

찾은 예약의 `.next_run_time`은 **다음에 실행할 시각**입니다. 스케줄러를 `start()`한 뒤에 계산됩니다. (공식 문서)

**작은 예시** (`예시.py`)

```python
from apscheduler.schedulers.background import BackgroundScheduler


def hello() -> None:
    print("안녕")


scheduler = BackgroundScheduler()
job = scheduler.add_job(hello, "cron", hour=7, minute=30, id="morning")
print(job.trigger)
scheduler.start()
print(scheduler.get_job("morning").next_run_time)
scheduler.shutdown()
```

결과 (2026-11-05 저녁에 실행):

```
cron[hour='7', minute='30']
2026-11-06 07:30:00+09:00
```

- `job.trigger`는 "언제 실행하는가"라는 규칙입니다. `cron[hour='7', minute='30']`으로 보입니다.
- 오늘 7시 30분은 이미 지나서, 다음 실행은 **내일** 7시 30분입니다.
- `+09:00`은 시간대 표시입니다. 세계 기준 시각(UTC)보다 9시간 빠른, **한국 시간**이라는 뜻입니다.

시간대를 따로 정하지 않으면 스케줄러는 PC의 시간대를 씁니다. (공식 문서) 이 PC는 `Asia/Seoul`(한국)로 확인했습니다. (개발 기록 2번)

**이 프로젝트 코드** (`main.py` 21~23줄)

```python
next_run_time = scheduler.get_job(DAILY_JOB_ID).next_run_time
print("정기 알림 다음 실행 시각:", next_run_time)
logger.info(f"프로그램 시작: 정기 알림 다음 실행 시각 {next_run_time}")
```

프로그램을 켜자마자 "다음 알림이 언제 나가는지"를 화면과 로그에 남깁니다. 시각을 잘못 설정했다면 여기서 바로 알 수 있습니다.

**Java 비교**

`ZonedDateTime`을 출력하면 `2026-11-06T07:30+09:00[Asia/Seoul]`처럼 시간대가 붙는 것과 같습니다.

**자주 하는 실수: 시와 분에 범위를 벗어난 숫자를 넣는다**

```python
scheduler.add_job(hello, "cron", hour=25, minute=30)
```

결과:

```
ValueError: Error validating expression '25': the last value (25) is higher than the maximum value (23)
```

시는 0~23, 분은 0~59만 됩니다. `.env`의 `NOTIFY_HOUR`에 25를 적으면 프로그램이 켜질 때 이 오류가 납니다.

---

### 2-5. 늦어도 실행하기: `misfire_grace_time`, `coalesce`

**설명**

정해진 시각에 실행하지 못하는 경우가 있습니다. 예를 들어 7시 30분에 PC가 잠자기 상태였다가 7시 40분에 깨어나는 경우입니다.

`misfire_grace_time`은 "정해진 시각보다 **몇 초 늦게까지는** 그래도 실행한다"는 값입니다.

APScheduler의 기본값은 **1초**입니다. (설치된 APScheduler 코드에서 확인. 공식 문서에는 숫자가 적혀 있지 않았습니다) 1초만 늦어도 그날 알림을 건너뛰게 됩니다.

그래서 이 프로젝트는 **1시간**(3600초)으로 정했습니다. 8시 30분 전에만 깨어나면 늦게라도 알림이 나갑니다.

`coalesce=True`는 "실행을 여러 번 놓쳤어도, 한꺼번에 몰아서 하지 말고 **한 번만** 실행한다"는 뜻입니다. 같은 알림이 여러 번 나가는 일을 막습니다.

**비유**

학원 버스가 7시 30분에 출발하기로 했습니다. `misfire_grace_time`은 "늦은 학생을 몇 분까지 기다려 줄까"입니다. 기본값 1초는 거의 기다려 주지 않는 것입니다.

**이 프로젝트 코드** (`app/scheduler.py` 19~21줄)

```python
# 정해진 시각을 놓쳤을 때(예: 7시 30분에 PC가 잠자기 상태) 몇 초 늦게까지는 보낼지.
# APScheduler의 기본값은 1초라서, 잠깐만 늦어도 그날 알림을 건너뛴다. 1시간까지는 늦게라도 보낸다.
MISFIRE_GRACE_SECONDS: int = 60 * 60
```

테스트 `test_daily_job_allows_one_hour_late`가 이 두 값이 예약에 들어갔는지 확인합니다.

```
tests/test_scheduler.py::test_daily_job_allows_one_hour_late PASSED
```

**Java 비교**

Spring의 `@Scheduled`에는 이런 설정이 없습니다. 놓친 실행은 그냥 건너뜁니다. Quartz 같은 라이브러리의 "misfire" 설정과 같은 개념입니다.

**자주 하는 실수: 기본값을 믿고 그냥 둔다**

기본값 1초로 두면, 컴퓨터가 잠깐 바빠서 2초 늦어도 그날 알림이 나가지 않습니다. 오류도 나지 않아서 알아채기 어렵습니다.

---

### 2-6. `except Exception`: 어떤 오류든 잡기

**설명**

step05에서는 `except NeisError`처럼 **잡을 오류를 정해서** 잡았습니다.

`except Exception`은 **거의 모든 오류**를 잡습니다. `Exception`은 보통의 오류들을 모두 묶은 큰 이름이기 때문입니다.

**작은 예시**

```python
def risky(number: int) -> int:
    return 10 // number


try:
    print(risky(0))
except Exception as error:
    print("예상하지 못한 오류:", type(error).__name__)
print("프로그램은 계속 실행됩니다")
```

결과:

```
예상하지 못한 오류: ZeroDivisionError
프로그램은 계속 실행됩니다
```

0으로 나누는 오류(`ZeroDivisionError`)를 따로 적지 않았는데도 잡혔습니다.

**이 프로젝트 코드** (`app/scheduler.py` 24~35줄)

```python
def send_today_notification() -> None:
    today = to_yyyymmdd(date.today())
    logger.info(f"정기 알림 시작: {today}")
    try:
        send_lunch_notification(today)
    except Exception as error:
        logger.error(f"정기 알림 중 예상하지 못한 오류: {type(error).__name__}")
        notify_admin(f"{today} 정기 알림 중 예상하지 못한 오류가 났습니다. ({type(error).__name__}) logs/bot.log를 확인하세요.")
```

(주석은 줄였습니다.)

- NEIS 오류와 Slack 오류는 `send_lunch_notification` 안에서 이미 처리합니다. (step05)
- 여기서 `Exception`으로 넓게 잡는 이유는 **미처 생각하지 못한 오류**에 대비하기 위해서입니다.
- 아침 알림은 사람이 지켜보지 않는 시각에 돕니다. 잡지 않으면 스케줄러가 오류를 **화면에만** 출력하고 넘어갑니다. 로그 파일(`logs/bot.log`)에도 남지 않고 관리자도 모릅니다.

일부러 오류를 내는 예약으로 확인한 결과입니다. (`예시.py`, 매초 `10 // 0`을 실행)

```python
def broken() -> None:
    print(10 // 0)


scheduler = BackgroundScheduler()
scheduler.add_job(broken, "cron", second="*")
scheduler.start()
time.sleep(1.5)
scheduler.shutdown()
print("프로그램은 계속 실행되었습니다")
```

결과 (화면의 오류 출력 부분은 줄였습니다):

```
Job "broken (trigger: cron[second='*'], next run at: 2026-11-05 19:57:50 KST)" raised an exception
Traceback (most recent call last):
  ...
ZeroDivisionError: integer division or modulo by zero
프로그램은 계속 실행되었습니다
```

오류는 화면에 한 번 나오고 끝입니다. 아무도 화면을 보고 있지 않으면 모르고 지나갑니다.

**Java 비교**

```java
try {
    sendLunchNotification(today);
} catch (Exception e) {
    log.error("정기 알림 중 예상하지 못한 오류: " + e.getClass().getSimpleName());
}
```

**자주 하는 실수: 잡고 아무것도 하지 않는다**

```python
try:
    print(risky(0))
except Exception:
    pass
print("끝")
```

결과:

```
끝
```

오류가 났다는 흔적이 하나도 없습니다. 넓게 잡을수록, 잡은 뒤에 **반드시 기록**(로그, 알림)을 남겨야 합니다.

---

### 2-7. `KeyboardInterrupt`: Ctrl+C로 생기는 예외

**설명**

실행 중인 프로그램 창에서 **Ctrl+C**를 누르면, Python은 `KeyboardInterrupt`라는 예외를 일으킵니다. "사용자가 키보드로 멈추라고 했다"는 뜻입니다.

`KeyboardInterrupt`는 **`Exception`에 들어 있지 않습니다.** 그래서 `except Exception`으로는 잡히지 않습니다. 오류가 아니라 사용자가 일부러 멈춘 것이기 때문입니다.

```python
print(issubclass(ZeroDivisionError, Exception))
print(issubclass(KeyboardInterrupt, Exception))
```

결과:

```
True
False
```

`issubclass(A, B)`는 "A가 B 묶음에 들어 있는가?"를 확인하는 내장 함수입니다. 이 예시에서만 씁니다.

**작은 예시** (Ctrl+C 대신 `raise`로 같은 예외를 일으켰습니다)

```python
try:
    raise KeyboardInterrupt
except KeyboardInterrupt:
    print("Ctrl+C로 끝냈습니다")
print("정리하고 끝냅니다")
```

결과:

```
Ctrl+C로 끝냈습니다
정리하고 끝냅니다
```

**이 프로젝트 코드** (`main.py` 25~36줄)

```python
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
```

Ctrl+C로 서버를 끈 뒤에도 아래 세 줄(스케줄러 끄기, 로그, 안내)이 실행되게 하려고 `KeyboardInterrupt`를 잡습니다.

**Java 비교**

Java에는 Ctrl+C용 예외가 없습니다. 대신 `Runtime.getRuntime().addShutdownHook(...)`으로 "끝날 때 할 일"을 등록합니다.

**자주 하는 실수: `except Exception`으로 Ctrl+C를 잡으려 한다**

```python
try:
    raise KeyboardInterrupt
except Exception:
    print("잡았습니다")
print("정리하고 끝냅니다")
```

결과:

```
Traceback (most recent call last):
  File "예시.py", line 2, in <module>
    raise KeyboardInterrupt
KeyboardInterrupt
```

`KeyboardInterrupt`는 `Exception` 묶음에 없어서 잡히지 않았습니다. 아래의 "정리하고 끝냅니다"도 실행되지 않았습니다.

---

### 2-8. `uvicorn.run`: 코드 안에서 서버 켜기

**설명**

6~8단계에서는 명령어로 서버를 켰습니다.

```powershell
python -m uvicorn app.server:app --port 8000
```

`uvicorn.run(앱, host=주소, port=번호)`는 **같은 일을 Python 코드 안에서** 합니다. 서버를 켜기 **전에** 스케줄러를 시작하는 코드를 함께 쓸 수 있어서, 이 방법을 골랐습니다.

`uvicorn.run`은 서버가 꺼질 때까지 **돌아오지 않습니다.** (2-2)

**이 프로젝트 코드** (`main.py` 15~27줄 요약)

```python
HOST: str = "127.0.0.1"
PORT: int = 8000

scheduler = create_scheduler()
scheduler.start()
...
uvicorn.run(app, host=HOST, port=PORT)
```

**실제 실행 결과** (정기 알림 시각을 18시 29분으로 바꿔 시험한 것. 개발 기록 4번 결과 4)

```
정기 알림 다음 실행 시각: 2026-11-05 18:29:00+09:00
INFO:     Started server process [9464]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
[명령어] help | 보낸 글: 도움말
INFO:     127.0.0.1:*** - "POST /slack/events HTTP/1.1" 200 OK
INFO:     Shutting down
INFO:     Waiting for application shutdown.
INFO:     Application shutdown complete.
INFO:     Finished server process [9464]
프로그램을 종료했습니다.
```

같은 시간에 로그에는 18시 29분 정기 알림이 남았습니다. 서버와 스케줄러가 한 프로그램 안에서 함께 일했습니다.

**Java 비교**

Spring Boot의 `SpringApplication.run(App.class, args)`처럼, `main`에서 서버를 켜는 것과 같습니다.

**자주 하는 실수: `--reload`처럼 쓰려고 한다**

8단계에서 겪었듯 `--reload`는 Windows에서 멈출 수 있습니다. `main.py`는 `--reload` 없이 켭니다. 코드를 고쳤다면 Ctrl+C로 끄고 `python main.py`로 다시 켭니다.

---

### 2-9. 숫자 설정 읽기: `read_int_setting`

**설명**

`.env`의 값은 언제나 **글자**로 읽힙니다. (step01) 시각은 숫자여야 하므로 `int()`로 바꿉니다. (step07)

`.env`에 적지 않았거나 비워 두면 기본값을 씁니다. 그래서 `.env`를 고치지 않아도 아침 7시 30분에 알림이 나갑니다.

**작은 예시** (프로젝트 함수를 줄여, 글자를 직접 넘기게 했습니다)

```python
def read_int_setting(value: str, default: int) -> int:
    if value == "":
        return default
    return int(value)


print(read_int_setting("", 7))
print(read_int_setting("8", 7))
print(read_int_setting("8시", 7))
```

결과:

```
7
8
Traceback (most recent call last):
  ...
ValueError: invalid literal for int() with base 10: '8시'
```

**이 프로젝트 코드** (`app/config.py` 17~23줄, 47~48줄)

```python
def read_int_setting(name: str, default: int) -> int:
    value = os.getenv(name, "")
    if value == "":
        return default
    return int(value)
```

```python
NOTIFY_HOUR: int = read_int_setting("NOTIFY_HOUR", 7)
NOTIFY_MINUTE: int = read_int_setting("NOTIFY_MINUTE", 30)
```

숫자가 아닌 값(`8시`)을 적으면 프로그램이 켜질 때 바로 오류가 납니다. 이상한 값을 몰래 기본값으로 바꾸지 않고 바로 알리려고, 일부러 오류를 잡지 않았습니다.

**Java 비교**

```java
String value = System.getenv().getOrDefault("NOTIFY_HOUR", "");
int hour = value.isEmpty() ? 7 : Integer.parseInt(value);   // 숫자가 아니면 NumberFormatException
```

**자주 하는 실수: `.env`에 단위나 따옴표를 붙인다**

`NOTIFY_HOUR=8시`나 `NOTIFY_HOUR="8 "`처럼 적으면 `int()`가 숫자로 바꾸지 못합니다. `NOTIFY_HOUR=8`처럼 숫자만 적습니다.

---

## 3. 코드 줄 단위 해설

### 3-1. `app/scheduler.py` (새 파일)

| 줄 | 설명 |
| --- | --- |
| 7 | 오늘 날짜를 구할 `date`를 가져옵니다. (step08) |
| 9 | APScheduler의 `BackgroundScheduler`를 가져옵니다. (2-3) |
| 11~14 | 날짜 모양 바꾸기, 알림 시각, 로그, 알림 함수들을 가져옵니다. 모두 앞 단계에서 만든 것입니다. |
| 17 | 예약의 이름입니다. `main.py`가 이 이름으로 다음 실행 시각을 찾습니다. (2-4) |
| 21 | 늦어도 실행하는 한도, 1시간입니다. (2-5) |
| 24~35 | `send_today_notification`: 스케줄러가 매일 부르는 함수입니다. |
| 26 | 부를 때마다 **그날의** 날짜를 새로 구합니다. 날짜를 미리 구해 두면 매일 같은 날짜로 보내게 됩니다. |
| 27 | 알림을 시작했다고 로그에 남깁니다. |
| 28~35 | 알림을 보내고, 생각하지 못한 오류는 로그와 관리자 알림으로 남깁니다. (2-6) |
| 38~52 | `create_scheduler`: 스케줄러를 만들고 매일 알림을 예약해서 돌려줍니다. 아직 `start()`는 하지 않습니다. |

`create_scheduler`가 `start()`까지 하지 않는 이유가 있습니다. 테스트에서 예약 내용만 확인하고, 실제 알림은 나가지 않게 하기 위해서입니다.

### 3-2. `main.py` (새 파일)

| 줄 | 설명 |
| --- | --- |
| 8~12 | uvicorn, 로그, 스케줄러 만들기, 콜백 서버 앱을 가져옵니다. |
| 15~16 | 서버 주소와 포트입니다. 6단계부터 같은 값이라, 터널 설정을 바꾸지 않아도 됩니다. |
| 18~20 | 스케줄러를 만들고 **먼저** 시작합니다. (2-2) |
| 21~23 | 다음 알림 시각을 화면과 로그에 남깁니다. (2-4) |
| 25~31 | 서버를 켜고, Ctrl+C로 끌 때 생길 수 있는 `KeyboardInterrupt`는 넘어갑니다. (2-7, 2-8) |
| 34~36 | 서버가 꺼지면 스케줄러를 끄고, 로그와 안내를 남깁니다. |

`main.py`는 `app` 폴더가 아니라 프로젝트 맨 위 폴더에 있습니다. `python main.py`로 바로 실행하는 파일이라, `send_lunch_message.py` 같은 다른 실행 파일과 같은 곳에 두었습니다.

### 3-3. `app/formatter.py` (추가된 부분)

| 줄 | 설명 |
| --- | --- |
| 31 | 정기 알림의 학사일정 제목 `[오늘의 학사일정]`입니다. (CLAUDE.md 메시지 예시) |
| 34 | 학사일정을 가져오지 못했을 때 제목 아래에 쓸 문구입니다. |
| 175~182 | `format_today_schedule`: 8단계의 `group_events_by_date`로 묶은 뒤, 오늘 날짜의 행사만 꺼냅니다. 없으면 `없음`입니다. 토요휴업일은 묶을 때 이미 빠지므로, 토요일은 `없음`이 됩니다. |
| 185~187 | `format_daily_message`: 급식 부분과 학사일정 부분 사이에 빈 줄을 둡니다. `"\n\n"`은 줄바꿈 두 번, 곧 빈 줄 하나입니다. (`\n`은 step03 참고) |

### 3-4. `app/notifier.py` (바뀐 부분)

| 줄 | 설명 |
| --- | --- |
| 35~43 | `make_today_schedule_section`: 오늘 하루(시작일 = 끝일)의 학사일정을 가져와 학사일정 부분을 만듭니다. |
| 37~42 | 가져오지 못하면 로그와 관리자 알림을 남기고, "학사일정을 가져오지 못했습니다."를 돌려줍니다. 오류를 위로 올려 보내지 않습니다. |
| 55~57 | 급식 부분과 학사일정 부분을 만들어 하나의 메시지로 합칩니다. |

학사일정은 CLAUDE.md에서 "선택" 기능입니다. 급식("필수")은 학사일정이 실패해도 보내야 합니다. 그래서 학사일정 오류는 이 함수 안에서 처리하고 끝냅니다.

반대로 **급식** 조회가 실패하면 5단계와 같이 관리자에게 알리고 메시지를 보내지 않습니다.

### 3-5. `app/config.py`, `.env.example`, `requirements.txt` (바뀐 부분)

- `app/config.py`: `read_int_setting`(2-9)과 `NOTIFY_HOUR`, `NOTIFY_MINUTE`를 추가했습니다.
- `.env.example`: `NOTIFY_HOUR=`, `NOTIFY_MINUTE=` 항목 이름을 추가했습니다. 비워 두면 7시 30분입니다.
- `requirements.txt`: `apscheduler==3.11.3`을 추가했습니다.

### 3-6. 테스트 (8개 추가, 전체 68개)

- `tests/test_formatter.py` (4개)
  - 행사가 두 개인 날, 토요휴업일만 있는 날, 자료가 없는 날의 `[오늘의 학사일정]`을 확인합니다.
  - 급식과 학사일정 사이에 빈 줄이 들어간 전체 메시지를 확인합니다.
- `tests/test_scheduler.py` (새 파일, 4개)
  - 예약이 `NOTIFY_HOUR`시 `NOTIFY_MINUTE`분에 매일 실행되는지, 실행할 함수가 맞는지 확인합니다.
  - 1시간 늦어도 실행하고(`misfire_grace_time`), 몰아서 실행하지 않는지(`coalesce`) 확인합니다.
  - `.env`에 없는 숫자 설정은 기본값이 되는지 확인합니다.

```python
def test_daily_job_runs_every_day_at_notify_time():
    job = create_scheduler().get_job(DAILY_JOB_ID)
    assert str(job.trigger) == f"cron[hour='{NOTIFY_HOUR}', minute='{NOTIFY_MINUTE}']"
```

`str(값)`은 값을 글자로 바꿉니다. 2-4에서 본 `cron[hour='7', minute='30']` 모양과 비교합니다. `.env`에서 시각을 바꿔도 테스트가 맞도록, 7과 30을 직접 쓰지 않고 설정값을 넣었습니다.

---

## 4. 사용한 라이브러리

| 라이브러리 | 종류 | 이번에 쓴 것 | 뜻 |
| --- | --- | --- | --- |
| APScheduler | 따로 설치 | `BackgroundScheduler()`, `add_job(함수, "cron", hour=, minute=, id=, misfire_grace_time=, coalesce=)`, `start()`, `get_job(id).next_run_time`, `shutdown()` | 정해진 시각에 함수를 실행합니다. |
| tzlocal, tzdata | 따로 설치 (APScheduler가 함께 설치) | 직접 쓰지 않음 | PC의 시간대를 알아내고, 시간대 정보를 제공합니다. |
| uvicorn | 따로 설치 | `uvicorn.run(app, host=, port=)` | 코드 안에서 서버를 켭니다. |
| os | 표준 | `os.getenv(이름, "")` | `.env`에서 읽은 설정값 |
| (기본 기능) | 내장 | `Exception`, `KeyboardInterrupt`, `str()`, `issubclass()` | 보통 오류의 묶음, Ctrl+C 예외, 글자로 바꾸기, 묶음 확인(예시에서만) |

---

## 5. 용어 정리

| 용어 | 쉬운 뜻 | 예시 |
| --- | --- | --- |
| 스케줄러 | 정해진 시각에 일을 실행해 주는 프로그램 | `BackgroundScheduler` |
| cron | 시·분·요일 같은 달력 칸으로 때를 정하는 방식 | `"cron", hour=7, minute=30` |
| 예약(job) | 스케줄러에 맡긴 일 하나 | `add_job(...)`이 돌려주는 것 |
| 스레드 | 프로그램 안에서 코드가 차례로 실행되는 흐름 하나 | 서버 스레드, 스케줄러 스레드 |
| 시간대 | 나라·지역마다 다른 시각 기준 | `Asia/Seoul`, `+09:00` |
| UTC | 세계 기준 시각. 한국은 이보다 9시간 빠르다 | `08:32Z` = 한국 `17:32` |
| misfire | 정해진 시각에 실행하지 못한 것 | PC가 잠자기 상태였던 7시 30분 |
| 통합 | 따로 있던 기능을 한 프로그램으로 합치는 것 | 스케줄러 + 콜백 서버 = `main.py` |

---

## 6. 확인 문제

### 문제 1. 코드 읽기: 출력은?

```python
def read_int_setting(value: str, default: int) -> int:
    if value == "":
        return default
    return int(value)


print(read_int_setting("", 30))
print(read_int_setting("07", 30))
print(read_int_setting("0", 30))
```

<details><summary>정답</summary>

```
30
7
0
```

- 빈 글자면 기본값 `30`입니다.
- `int("07")`은 앞의 0을 무시하고 `7`이 됩니다.
- `"0"`은 빈 글자가 아니라서 기본값이 아니라 `0`이 됩니다. `NOTIFY_MINUTE=0`이면 정각(예: 7시 0분)에 보냅니다. (2-9)

</details>

### 문제 2. 빈칸 채우기

매일 아침 8시 정각에 `send_today_notification`을 실행하고, 스케줄러를 켜려고 합니다.

```python
scheduler = BackgroundScheduler()
scheduler.add_job(send_today_notification, "____", hour=8, minute=0)
scheduler._____()
```

<details><summary>정답</summary>

- `cron`: 시와 분으로 때를 정하는 방식입니다. 정하지 않은 날짜·요일은 "아무 날이나"라서 매일 실행됩니다. (2-1)
- `start`: 스케줄러를 켭니다. 켜 놓고 바로 돌아옵니다. (2-3)
- `send_today_notification`에는 괄호를 붙이지 않습니다. 스케줄러가 나중에 실행해야 하기 때문입니다. (step08 2-9)

</details>

### 문제 3. 작은 수정: Ctrl+C로 끄면 "프로그램을 종료했습니다."가 나오지 않을 수 있습니다. 고치세요.

```python
try:
    uvicorn.run(app, host=HOST, port=PORT)
except Exception:
    pass

scheduler.shutdown()
print("프로그램을 종료했습니다.")
```

<details><summary>정답</summary>

```python
except KeyboardInterrupt:
    pass
```

Ctrl+C로 생기는 `KeyboardInterrupt`는 `Exception` 묶음에 들어 있지 않습니다. 그래서 `except Exception`으로는 잡히지 않고, 아래 줄이 실행되지 않은 채 프로그램이 끝납니다. (2-7의 "자주 하는 실수" 결과 참고)

</details>

---

## 이번 단계 핵심 정리

1. `main.py` 하나로 콜백 서버와 정기 알림 스케줄러를 함께 실행한다. 스케줄러는 다른 스레드에서 돈다.
2. 스케줄러는 서버보다 먼저 `start()`한다. `uvicorn.run`은 서버가 꺼질 때까지 돌아오지 않는다.
3. 매일 알림은 `"cron", hour=, minute=`으로 예약하고, 늦어도 1시간까지는 보낸다(`misfire_grace_time`).
4. 정기 알림에 `[오늘의 학사일정]`을 붙인다. 학사일정이 실패해도 급식 알림은 보낸다.
5. `except Exception`은 보통 오류를 모두 잡지만 Ctrl+C(`KeyboardInterrupt`)는 잡지 않는다.
