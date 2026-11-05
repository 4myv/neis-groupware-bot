# 9단계 실습 과제: 스케줄러, 스레드, `except Exception`, Ctrl+C

## 이 문서를 다 풀면 할 수 있게 되는 것

1. APScheduler로 "정해진 시각에 실행"을 예약하고, 다음 실행 시각을 확인할 수 있다.
2. 스케줄러가 원래 코드와 **함께** 도는 모습을 보고 설명할 수 있다.
3. `except Exception`이 잡는 것과 놓치는 것(Ctrl+C)을 구별하고, `main.py`와 같은 구조의 프로그램을 만들 수 있다.

## 시작하기 전에

- 함께 볼 문서: [`step09-learning.md`](step09-learning.md)
- 실습 파일은 `practice\step09\` 폴더에 만듭니다. (`New-Item -ItemType Directory -Force practice\step09`)
- 가상환경을 켜고 프로젝트 맨 위 폴더에서 실행합니다.
  - 보통 파일: `python practice\step09\파일.py`
  - 과제 6: `python -m practice.step09.mini_main`
- 실습 서버는 8001번 포트를 씁니다. 8000번은 급식 봇(`main.py`)이 쓰고 있을 수 있습니다.
- 결과는 모두 실제로 실행해 확인했습니다. **시각이 들어간 결과는 실행하는 때에 따라 다릅니다.** 2026-11-05(목) 저녁 9시쯤 실행한 결과입니다.

---

## 과제 1. 예약하고 다음 실행 시각 보기 (★)

**다지는 개념**: `BackgroundScheduler`, `add_job`(2-3), `next_run_time`과 `+09:00`(2-4)

**할 일**

`practice\step09\p1_next_run.py`를 만듭니다.

1. 아무 함수 `hello`를 만듭니다. (실제로 실행되기 전에 끌 것이라 내용은 상관없습니다)
2. 스케줄러에 예약 두 개를 넣습니다.
   - `id="lunch"`: 매일 12시 0분
   - `id="saturday"`: 매주 **토요일** 9시 0분 (`day_of_week="sat"`)
3. 스케줄러를 시작한 뒤, 두 예약의 규칙(`trigger`)과 다음 실행 시각(`next_run_time`)을 출력하고 끕니다.
4. **실행 전에** 다음 실행 시각을 먼저 예상해 적어 봅니다.

**확인 방법** (2026-11-05 목요일 저녁에 실행)

```
cron[hour='12', minute='0']
2026-11-06 12:00:00+09:00
cron[day_of_week='sat', hour='9', minute='0']
2026-11-07 09:00:00+09:00
```

- 오늘 12시는 이미 지나서, 다음은 내일(금) 12시입니다.
- `day_of_week`는 요일을 정하는 칸입니다. 이 칸을 정하지 않으면 "아무 요일이나"라서 매일 실행됩니다. (APScheduler 공식 문서의 cron 방식)

<details><summary>정답 예시</summary>

```python
# 예약 규칙과 다음 실행 시각 확인하기 (실제로 실행되기 전에 끈다)
from apscheduler.schedulers.background import BackgroundScheduler


def hello() -> None:
    print("안녕")


scheduler = BackgroundScheduler()
scheduler.add_job(hello, "cron", hour=12, minute=0, id="lunch")
scheduler.add_job(hello, "cron", day_of_week="sat", hour=9, minute=0, id="saturday")
scheduler.start()

print(scheduler.get_job("lunch").trigger)
print(scheduler.get_job("lunch").next_run_time)
print(scheduler.get_job("saturday").trigger)
print(scheduler.get_job("saturday").next_run_time)
scheduler.shutdown()
```

- `next_run_time`은 `start()` **뒤에** 계산됩니다. (2-4)
- 평일에만 알림을 보내고 싶다면 `day_of_week="mon-fri"`처럼 쓸 수 있습니다. 이 프로젝트는 CLAUDE.md의 "매일"에 따라 정하지 않았습니다.

</details>

---

## 과제 2. 두 일꾼이 함께 일하는 모습 보기 (★)

**다지는 개념**: 스레드(2-2), `start()`는 바로 돌아온다(2-3)

**할 일**

`practice\step09\p2_two_threads.py`를 만듭니다.

1. 지금 시각을 `시:분:초`로 출력하는 함수 `tick`을 만듭니다. (`time.strftime("%H:%M:%S")`)
2. `tick`을 **2초마다** 실행하도록 예약합니다. (`"cron", second="*/2"`)
3. 스케줄러를 시작한 뒤, 원래 코드는 `원래 코드: 7초 동안 다른 일을 합니다`를 출력하고 7초 기다립니다.
4. `원래 코드: 끝. 스케줄러를 끕니다`를 출력하고 스케줄러를 끕니다.

**확인 방법** (시각과 줄 수는 실행할 때마다 조금 다릅니다)

```
원래 코드: 7초 동안 다른 일을 합니다
  스케줄러: 21:01:42
  스케줄러: 21:01:44
  스케줄러: 21:01:46
원래 코드: 끝. 스케줄러를 끕니다
```

원래 코드가 `time.sleep(7)`로 멈춰 있는 동안에도, 스케줄러는 **다른 스레드**에서 2초마다 일했습니다.

<details><summary>정답 예시</summary>

```python
# 스케줄러(다른 스레드)와 원래 코드가 함께 일하는 모습 보기
import time

from apscheduler.schedulers.background import BackgroundScheduler


def tick() -> None:
    print("  스케줄러:", time.strftime("%H:%M:%S"))


scheduler = BackgroundScheduler()
scheduler.add_job(tick, "cron", second="*/2")
scheduler.start()

print("원래 코드: 7초 동안 다른 일을 합니다")
time.sleep(7)
print("원래 코드: 끝. 스케줄러를 끕니다")
scheduler.shutdown()
```

- `second="*/2"`는 "초가 2로 나누어떨어질 때마다"(0, 2, 4, …초)입니다. 실습에서 빨리 보려고 쓴 값입니다.
- `main.py`에서는 원래 코드가 `time.sleep` 대신 `uvicorn.run`(서버)으로 멈춰 있습니다.

</details>

---

## 과제 3. `except Exception`이 잡는 것과 놓치는 것 (★★)

**다지는 개념**: `except Exception`(2-6), `KeyboardInterrupt`(2-7), 함수를 값으로(step08)

**할 일**

`practice\step09\p3_exception_vs_ctrl_c.py`를 만듭니다.

1. 오류를 내는 함수 세 개를 만듭니다.
   - `divide_by_zero`: `10 // 0`
   - `missing_key`: 빈 딕셔너리에서 `"DDISH_NM"` 꺼내기
   - `press_ctrl_c`: `raise KeyboardInterrupt` (Ctrl+C 흉내)
2. 함수 `safe_run(job) -> None`: 받은 함수를 실행하고, `except Exception`으로 오류를 잡아 `잡음:`과 종류 이름을 출력합니다.
3. 세 함수를 `safe_run`에 넘깁니다. 셋째는 바깥에서 `try` / `except KeyboardInterrupt`로 감싸, 잡히면 `Ctrl+C는 except Exception을 지나 바깥까지 왔습니다`를 출력합니다.

**확인 방법**

```
잡음: ZeroDivisionError
잡음: KeyError
Ctrl+C는 except Exception을 지나 바깥까지 왔습니다
```

<details><summary>정답 예시</summary>

```python
# except Exception은 무엇을 잡고, 무엇을 놓치는가
def divide_by_zero() -> None:
    print(10 // 0)


def missing_key() -> None:
    print({}["DDISH_NM"])


def press_ctrl_c() -> None:
    raise KeyboardInterrupt


def safe_run(job) -> None:
    try:
        job()
    except Exception as error:
        print("잡음:", type(error).__name__)


safe_run(divide_by_zero)
safe_run(missing_key)
try:
    safe_run(press_ctrl_c)
except KeyboardInterrupt:
    print("Ctrl+C는 except Exception을 지나 바깥까지 왔습니다")
```

- `KeyboardInterrupt`는 `Exception` 묶음에 들어 있지 않습니다. 사용자가 일부러 멈춘 것이지 프로그램의 오류가 아니기 때문입니다. 그래서 `except Exception`이 있어도 Ctrl+C로 프로그램을 끌 수 있습니다.

</details>

---

## 과제 4. 숫자 설정을 읽고 범위까지 확인하기 (★★)

**다지는 개념**: 숫자 설정 읽기(2-9), `raise`(step05), 환경 변수(step01)

**할 일**

`practice\step09\p4_hour_setting.py`를 만듭니다.

1. 함수 `read_hour_setting(name: str, default: int) -> int`
   - 환경 변수가 없거나 비어 있으면 기본값
   - 있으면 `int()`로 바꾼 뒤, 0보다 작거나 23보다 크면 `ValueError("PRACTICE_HOUR는 0~23 사이여야 합니다: 25")` 모양의 오류를 일으킵니다.
2. `read_hour_setting("PRACTICE_HOUR", 7)`의 결과를 `알림 시:`와 함께 출력합니다.
3. PowerShell에서 네 번 실행합니다.
   ```powershell
   python practice\step09\p4_hour_setting.py
   $env:PRACTICE_HOUR = "8";  python practice\step09\p4_hour_setting.py
   $env:PRACTICE_HOUR = "25"; python practice\step09\p4_hour_setting.py
   $env:PRACTICE_HOUR = "8시"; python practice\step09\p4_hour_setting.py
   Remove-Item Env:PRACTICE_HOUR
   ```

**확인 방법** (오류는 맨 아래 줄만)

```
알림 시: 7
알림 시: 8
ValueError: PRACTICE_HOUR는 0~23 사이여야 합니다: 25
ValueError: invalid literal for int() with base 10: '8시'
```

마지막 `Remove-Item Env:PRACTICE_HOUR`는 실습용 환경 변수를 지웁니다.

<details><summary>정답 예시</summary>

```python
# 숫자 설정을 읽고, 범위까지 확인하기
import os


def read_hour_setting(name: str, default: int) -> int:
    value = os.getenv(name, "")
    if value == "":
        return default
    hour = int(value)
    if hour < 0:
        raise ValueError(f"{name}는 0~23 사이여야 합니다: {hour}")
    if hour > 23:
        raise ValueError(f"{name}는 0~23 사이여야 합니다: {hour}")
    return hour


print("알림 시:", read_hour_setting("PRACTICE_HOUR", 7))
```

- 프로젝트의 `read_int_setting`은 범위를 따로 확인하지 않습니다. 대신 APScheduler가 `add_job`에서 25시 같은 값을 거부합니다. (step09 학습 정리 2-4)
- 잘못된 설정은 몰래 기본값으로 바꾸지 않고, 켤 때 바로 오류로 알리는 편이 찾기 쉽습니다.

</details>

---

## 과제 5. 예약된 일에서 오류가 나도 계속 돌게 하기 (★★★)

**다지는 개념**: `except Exception`(2-6), 스케줄러에서 난 오류(학습 정리 2-6의 예시)

**할 일**

`practice\step09\p5_job_error.py`를 만듭니다.

1. 늘 오류가 나는 함수 `broken_job`: `print(10 // 0)`
2. 함수 `safe_job`: `broken_job`을 실행하고, `except Exception`으로 잡아 `오류를 기록했습니다:`, 종류 이름, 지금 시각을 출력합니다.
3. `safe_job`을 **매초**(`second="*"`) 실행하도록 예약하고, 3.5초 기다린 뒤 끕니다.
4. 마지막에 `프로그램은 끝까지 실행되었습니다`를 출력합니다.

**확인 방법** (시각과 줄 수(3~4줄)는 실행할 때마다 조금 다릅니다)

```
  오류를 기록했습니다: ZeroDivisionError 21:02:03
  오류를 기록했습니다: ZeroDivisionError 21:02:04
  오류를 기록했습니다: ZeroDivisionError 21:02:05
프로그램은 끝까지 실행되었습니다
```

**더 해 보기**: `add_job`에 `safe_job` 대신 `broken_job`을 넣어 보세요. 오류가 화면에 길게 나오고, 내 코드의 `print`는 없습니다. 실제 프로그램이었다면 로그 파일에 아무것도 남지 않았을 것입니다.

<details><summary>정답 예시</summary>

```python
# 예약된 일에서 오류가 나도 기록을 남기고 계속 돌게 하기
import time

from apscheduler.schedulers.background import BackgroundScheduler


def broken_job() -> None:
    print(10 // 0)


def safe_job() -> None:
    try:
        broken_job()
    except Exception as error:
        print("  오류를 기록했습니다:", type(error).__name__, time.strftime("%H:%M:%S"))


scheduler = BackgroundScheduler()
scheduler.add_job(safe_job, "cron", second="*")
scheduler.start()
time.sleep(3.5)
scheduler.shutdown()
print("프로그램은 끝까지 실행되었습니다")
```

- `app/scheduler.py`의 `send_today_notification`이 같은 구조입니다. `print` 대신 `logger.error`와 `notify_admin`으로 기록합니다.

</details>

---

## 과제 6. 도전: 나만의 작은 `main.py` (★★★)

**다지는 개념**: 스케줄러를 먼저 시작(2-2), `uvicorn.run`(2-8), `KeyboardInterrupt`(2-7), `shutdown`(2-3)

**할 일**

`practice\step09\mini_main.py`를 만듭니다. `main.py`의 구조를 그대로 따라 합니다.

1. 빈 FastAPI 앱 `app`을 만듭니다. (창구는 없어도 됩니다)
2. 지금 시각을 `[스케줄러]`와 함께 출력하는 `tick`을 **5초마다**(`second="*/5"`, `id="tick"`) 예약하고 시작합니다.
3. 다음 실행 시각을 출력합니다.
4. `uvicorn.run(app, host="127.0.0.1", port=8001)`로 서버를 켭니다. `KeyboardInterrupt`가 오면 넘어갑니다.
5. 서버가 꺼지면 스케줄러를 끄고 `프로그램을 종료했습니다.`를 출력합니다.
6. `python -m practice.step09.mini_main`으로 실행하고, `[스케줄러]` 줄이 두세 번 나오면 **Ctrl+C**를 누릅니다.

**확인 방법** (시각과 번호는 다릅니다)

```
다음 실행 시각: 2026-11-05 21:02:15+09:00
INFO:     Started server process [19064]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:8001 (Press CTRL+C to quit)
[스케줄러] 21:02:15
[스케줄러] 21:02:20
INFO:     Shutting down
INFO:     Waiting for application shutdown.
INFO:     Application shutdown complete.
INFO:     Finished server process [19064]
프로그램을 종료했습니다.
```

- 서버가 요청을 기다리는 동안에도 `[스케줄러]` 줄이 나옵니다. 급식 봇이 명령어를 기다리면서 아침 7시 30분을 기다리는 것과 같습니다.
- 위 결과는 에이전트 환경에서 **Ctrl+C와 같은 신호를 흉내 내어** 얻은 것입니다. 에이전트 환경에서는 진짜 Ctrl+C를 보낼 수 없었습니다. (step09 개발 기록 문제 1) 직접 Ctrl+C를 눌러 마지막 줄이 같은지 확인해 보세요. 이것이 9단계에서 남은 확인과 같은 확인입니다.

<details><summary>정답 예시</summary>

```python
# main.py를 줄인 실습 프로그램. 실행: python -m practice.step09.mini_main  (끄기: Ctrl+C)
import time

import uvicorn
from apscheduler.schedulers.background import BackgroundScheduler
from fastapi import FastAPI

app = FastAPI()


def tick() -> None:
    print("[스케줄러]", time.strftime("%H:%M:%S"))


scheduler = BackgroundScheduler()
scheduler.add_job(tick, "cron", second="*/5", id="tick")
scheduler.start()
print("다음 실행 시각:", scheduler.get_job("tick").next_run_time)

try:
    uvicorn.run(app, host="127.0.0.1", port=8001)
except KeyboardInterrupt:
    pass

scheduler.shutdown()
print("프로그램을 종료했습니다.")
```

- 스케줄러를 `uvicorn.run` **아래에** 두면, 서버가 꺼질 때까지 스케줄러가 시작되지 않습니다. (step09 학습 정리 2-2 자주 하는 실수)
- `except KeyboardInterrupt`를 `except Exception`으로 바꾸면 Ctrl+C를 잡지 못할 수 있습니다. (과제 3)

</details>

---

## 다 풀었다면

- [ ] `add_job(함수, "cron", hour=, minute=)`으로 예약하고 `next_run_time`으로 확인할 수 있다.
- [ ] 스케줄러가 다른 스레드에서 돌아서, 원래 코드와 함께 일한다는 것을 말할 수 있다.
- [ ] `except Exception`과 `except KeyboardInterrupt`를 각각 어디에 쓰는지 말할 수 있다.

## 이번 단계 핵심 정리

1. `BackgroundScheduler()` → `add_job(함수, "cron", ...)` → `start()` → (일) → `shutdown()` 순서다.
2. `start()`는 바로 돌아오고, 예약된 일은 다른 스레드에서 실행된다. 그래서 서버보다 먼저 시작한다.
3. `next_run_time`의 `+09:00`은 한국 시간이고, 정하지 않은 cron 칸은 "아무 때나"다.
4. 예약된 일 안에서는 `except Exception`으로 오류를 잡아 기록해야 로그에 남는다.
5. Ctrl+C(`KeyboardInterrupt`)는 `Exception`이 아니므로 따로 잡는다.
