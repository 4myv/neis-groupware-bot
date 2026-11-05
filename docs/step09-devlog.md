# 9단계 개발 기록: 통합 (정기 알림 스케줄러 + 콜백 서버)

## 이 문서를 다 읽으면 할 수 있게 되는 것

1. `python main.py` 하나로 매일 아침 알림과 명령어 답장을 함께 실행할 수 있다.
2. 정기 알림 시각을 바꾸고, 다음 알림이 언제 나가는지 확인할 수 있다.
3. 9단계에서 정한 기준(알림 시각, 늦은 알림, 학사일정 실패 시 처리 등)과 그 이유를 알 수 있다.

---

## 1. 목표

- 스케줄러와 콜백 서버를 **한 프로그램**으로 합친다. (CLAUDE.md 9단계)
- 매일 아침 정해진 시각에 정기 알림을 보낸다. (CLAUDE.md 기능 표: 정기 급식 알림, 필수)
- 정기 알림에 오늘의 학사일정을 함께 표시한다. (CLAUDE.md 기능 표: 학사일정 알림, 선택)

  ```
  [11월 5일(목) 중식]
  쌀밥 / 된장찌개 / 제육볶음 / 배추김치 / 요구르트

  [오늘의 학사일정]
  없음
  ```

---

## 2. 한 일 (순서대로)

1. **공식 문서 확인** (APScheduler 3.x)
   - `BackgroundScheduler`: 이미 있는 프로그램 안에서, 따로 스레드를 만들어 돈다. `start()`는 바로 돌아온다.
   - `add_job(함수, "cron", hour=, minute=)`: 정하지 않은 날짜·요일은 "아무 날이나"라서 매일 실행된다.
   - 시간대: 정하지 않으면 PC의 시간대를 쓴다.
   - `misfire_grace_time`(늦어도 실행할 한도), `coalesce`(놓친 실행을 한 번으로): 예약마다 정할 수 있다.
   - `job.next_run_time`: 다음 실행 시각. `start()` 뒤에 계산된다.
2. **설치와 확인**
   - `apscheduler==3.11.3`(지금 나온 3.x 중 최신)을 설치했다. tzlocal, tzdata가 함께 설치되었다.
   - PC 시간대가 `Asia/Seoul`로 잡히는 것을 확인했다. (4번 결과 2)
   - 공식 문서에 적혀 있지 않던 기본값을 **설치된 APScheduler 코드**에서 확인했다. `misfire_grace_time` 1초, `coalesce` True, `max_instances` 1.
3. **설정**: `app/config.py`에 `read_int_setting`, `NOTIFY_HOUR`(기본 7), `NOTIFY_MINUTE`(기본 30)을 추가했다. `.env.example`에 항목 이름을 추가했다.
4. **메시지**: `app/formatter.py`에 `format_today_schedule`, `format_daily_message`를 추가했다. 8단계의 `group_events_by_date`를 그대로 쓴다.
5. **알림**: `app/notifier.py`의 정기 알림(`send_lunch_notification`)이 오늘의 학사일정도 붙여 보내게 했다. 학사일정 조회가 실패해도 급식 알림은 보낸다.
6. **스케줄러**: `app/scheduler.py`를 새로 만들었다.
7. **통합**: 프로젝트 맨 위에 `main.py`를 새로 만들었다. 스케줄러를 먼저 시작하고 `uvicorn.run`으로 서버를 켠다.
8. **uvicorn 종료 동작 확인**: Ctrl+C를 받으면 서버를 정리한 뒤 신호를 다시 보낸다는 것을 설치된 uvicorn 코드(`capture_signals`)에서 확인했다. 그래서 `main.py`가 `KeyboardInterrupt`를 잡게 했다. (5번 문제 1)
9. **테스트**: 8개를 추가했다. (전체 68개)
10. **미리보기**: 공개 예시 학교로 정기 알림 글을 만들어 화면에만 보여 줬다. 학사일정 조회가 실패하는 경우도 일부러 만들어 봤다. (4번 결과 3)
11. **통합 시험**: 8단계 서버를 끄고, 알림 시각을 "1분 뒤"로 바꿔 `main.py`를 실행했다. (4번 결과 4)
    - 그 사이에 서명한 `도움말` 이벤트를 보내 콜백 서버도 확인했다.
    - 정기 알림이 실제로 Slack 급식 알림 채널에 나갔다.
    - 알림이 끝난 뒤 Ctrl+C와 같은 신호를 보내 정상 종료를 확인했다.
12. **오류 기록 확인**: 예약된 함수에서 오류가 나면 APScheduler가 어떻게 하는지 예시로 확인했다. 화면에만 출력하고 로그 파일에는 남기지 않았다. 그래서 정기 알림 함수가 모든 오류를 잡아 로그와 관리자 알림으로 남기게 했다. (학습 정리 2-6)
13. 학습 정리와 개발 기록을 쓰고, 비밀 정보가 커밋 대상에 없는지 확인한 뒤 커밋한다.

---

## 3. 바뀐 파일

| 파일 | 추가·수정 | 내용 |
| --- | --- | --- |
| `main.py` | 새 파일 | 스케줄러 시작 → 다음 알림 시각 출력 → 서버 실행 → 끝나면 스케줄러 정리 |
| `app/scheduler.py` | 새 파일 | `DAILY_JOB_ID`, `MISFIRE_GRACE_SECONDS`, `send_today_notification`, `create_scheduler` |
| `app/config.py` | 수정 | `read_int_setting`, `NOTIFY_HOUR`, `NOTIFY_MINUTE` 추가 |
| `app/formatter.py` | 수정 | `TODAY_SCHEDULE_TITLE`, `SCHEDULE_FAILED_TEXT`, `format_today_schedule`, `format_daily_message` 추가 |
| `app/notifier.py` | 수정 | `make_today_schedule_section` 추가, 정기 알림에 학사일정 붙이기 |
| `send_lunch_message.py` | 수정 | 설명 주석만 고침 (학사일정 포함, 자동 알림은 `main.py`) |
| `.env.example` | 수정 | `NOTIFY_HOUR=`, `NOTIFY_MINUTE=` 추가 (값은 비워 둠) |
| `requirements.txt` | 수정 | `apscheduler==3.11.3` 추가 |
| `tests/test_formatter.py` | 수정 | 테스트 4개 추가 |
| `tests/test_scheduler.py` | 새 파일 | 테스트 4개 |
| `docs/step09-learning.md` | 새 파일 | 9단계 학습 정리 |
| `docs/step09-devlog.md` | 새 파일 | 이 문서 |

**폴더 구조에서 바뀐 점**: CLAUDE.md 권장 구조에 없는 `main.py`를 프로젝트 맨 위에 더했다. `app/scheduler.py`(정기 알림)와 `app/server.py`(콜백 서버)를 한 프로그램으로 묶어 실행하는 파일이다. `python main.py`로 바로 실행하는 파일이라서, 다른 실행 파일(`send_lunch_message.py` 등)과 같은 곳에 두었다.

---

## 4. 실행 방법과 결과

### 개발자가 따라 할 순서

```powershell
cd C:\neis_groupware_bot
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt      # apscheduler가 새로 설치된다
python -m pytest
python main.py
```

- 명령어 답장도 받으려면, 다른 PowerShell 창에서 터널을 켭니다. (step06 개발 기록 참고)
- 끌 때는 `main.py`를 실행한 창에서 Ctrl+C를 누릅니다.
- 알림 시각을 바꾸려면 `.env`에 `NOTIFY_HOUR=8`, `NOTIFY_MINUTE=0`처럼 숫자만 적고 `main.py`를 다시 켭니다.
- 이제 `python -m uvicorn app.server:app ...`으로 서버만 켜면 정기 알림은 나가지 않습니다. `python main.py`로 켭니다.

### 결과 1: 테스트

```
tests/test_scheduler.py::test_daily_job_runs_every_day_at_notify_time PASSED
tests/test_scheduler.py::test_daily_job_calls_today_notification PASSED
tests/test_scheduler.py::test_daily_job_allows_one_hour_late PASSED
tests/test_scheduler.py::test_missing_number_setting_uses_default PASSED
tests/test_formatter.py::test_today_schedule_with_two_events PASSED
tests/test_formatter.py::test_today_schedule_on_saturday_holiday_is_none PASSED
tests/test_formatter.py::test_today_schedule_without_data PASSED
tests/test_formatter.py::test_daily_message_has_blank_line_between_parts PASSED
```

전체: `68 passed`

### 결과 2: 시간대와 APScheduler 기본값

```
PC 시간대: Asia/Seoul
스케줄러 기본 시간대: Asia/Seoul
trigger: cron[hour='7', minute='30']
pending: True
next: 2026-11-06 07:30:00+09:00
default: "misfire_grace_time": asint(job_defaults.get("misfire_grace_time", 1)),
default: "coalesce": asbool(job_defaults.get("coalesce", True)),
default: "max_instances": asint(job_defaults.get("max_instances", 1)),
```

`default:` 세 줄은 설치된 APScheduler 코드(`apscheduler/schedulers/base.py`)에서 기본값을 정하는 줄을 그대로 찾아 출력한 것이다.

### 결과 3: 정기 알림 미리보기 (공개 예시 학교, Slack으로 보내지 않음)

```
===== 20261104
[11월 4일(수) 중식]
녹두밥 / 북어계란국 / 치커리유자청무침 / 볼어묵볶음 / 찹쌀도넛 / 바베큐폭찹 / 배추김치

[오늘의 학사일정]
수업공개의 날, 독서골든벨
===== 20261105
[11월 5일(목) 중식]
흑미밥 / 부대찌개 / 호박볶음 / 오지치즈스틱 / 고등어구이 / 백김치

[오늘의 학사일정]
과학 하이챌린지(1,2)
===== 20261107
[11월 7일(토) 중식]
오늘은 급식이 없습니다.

[오늘의 학사일정]
없음
```

학사일정 조회가 실패하는 경우 (시험 코드에서 학사일정 조회 함수를 "늘 실패하는 함수"로 바꾸고, 관리자 알림은 화면 출력으로 바꿨다):

```
[관리자 알림 대신 출력] 20261105 학사일정을 NEIS에서 받지 못했습니다. 급식 알림은 학사일정 없이 보냅니다.
NEIS SchoolSchedule 호출이 두 번 모두 실패했습니다. 원인: 응답을 받지 못함(ConnectionError)
[11월 5일(목) 중식]
흑미밥 / 부대찌개 / 호박볶음 / 오지치즈스틱 / 고등어구이 / 백김치

[오늘의 학사일정]
학사일정을 가져오지 못했습니다.
```

이 시험 때문에 `logs/bot.log`에 아래 줄이 남았다. 일부러 만든 실패다.

```
2026-11-05 18:27:25,582 [ERROR] 20261105 학사일정 조회 실패: NEIS SchoolSchedule 호출이 두 번 모두 실패했습니다. 원인: 응답을 받지 못함(ConnectionError)
```

### 결과 4: 통합 시험 (`main.py`, 알림 시각만 18시 29분으로 바꿈)

`main.py`를 고치지 않고 그대로 실행했다. 시험 코드가 환경 변수 `NOTIFY_HOUR=18`, `NOTIFY_MINUTE=29`를 넣은 뒤 `main.py`를 실행했다. 알림이 끝나면 Ctrl+C와 같은 신호(SIGINT)를 보냈다. (5번 문제 1)

화면 (`test:`로 시작하는 줄은 시험 코드가 출력한 것, 포트 번호는 가림):

```
test: notify time set to 18:29
정기 알림 다음 실행 시각: 2026-11-05 18:29:00+09:00
INFO:     Started server process [9464]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
[명령어] help | 보낸 글: 도움말
INFO:     127.0.0.1:*** - "POST /slack/events HTTP/1.1" 200 OK
test: sending SIGINT (same as Ctrl+C)
INFO:     Shutting down
INFO:     Waiting for application shutdown.
INFO:     Application shutdown complete.
INFO:     Finished server process [9464]
프로그램을 종료했습니다.
test: main.py finished without an error
exit code: 0
```

`도움말` 이벤트를 보낸 쪽 (8단계와 같은 서명 시험 코드, 답장은 관리자 채널로):

```
status: 200 | body: ok | seconds until response: 0.02
```

로그 (`logs/bot.log`, 채널 ID는 가림):

```
2026-11-05 18:27:58,938 [INFO] 프로그램 시작: 정기 알림 다음 실행 시각 2026-11-05 18:29:00+09:00
2026-11-05 18:28:09,077 [INFO] 명령어 해석: event_id=Ev-local-help-1793870889, 명령어=help
2026-11-05 18:28:09,466 [INFO] Slack 전송 성공: 채널 ***
2026-11-05 18:28:09,467 [INFO] 명령어 답장 완료: help
2026-11-05 18:29:00,015 [INFO] 정기 알림 시작: 20261105
2026-11-05 18:29:00,110 [INFO] NEIS mealServiceDietInfo 호출 성공: 결과 코드 INFO-000
2026-11-05 18:29:00,214 [INFO] NEIS SchoolSchedule 호출 성공: 결과 코드 INFO-200
2026-11-05 18:29:00,550 [INFO] Slack 전송 성공: 채널 ***
2026-11-05 18:29:00,550 [INFO] 20261105 급식 알림 완료
2026-11-05 18:29:03,585 [INFO] 프로그램 종료
```

확인한 것:

| 확인할 것 | 결과 |
| --- | --- |
| 정해진 시각에 실행 | 18:29:00에 정기 알림이 시작되었다(0.015초 차이). |
| 정기 알림 전송 | 0.5초 뒤 Slack 급식 알림 채널로 전송이 끝났다. 개발자 학교는 이날 학사일정이 없어서(`INFO-200`) `[오늘의 학사일정]` 아래가 `없음`이었다. |
| 같은 프로그램에서 명령어 답장 | 서버가 0.02초 만에 응답하고, 0.39초 뒤 답장을 보냈다. |
| 정상 종료 | 신호를 받고 서버 정리 → 스케줄러 정리 → `프로그램 종료` 로그 → 종료 코드 0 |

---

## 5. 발생한 문제와 해결

### 문제 1. 진짜 Ctrl+C로는 종료 시험을 할 수 없었음

- **상황**
  - uvicorn 코드에는 "Ctrl+C로 서버를 정리한 뒤, 받은 신호를 다시 보낸다"는 부분이 있다. 그러면 `uvicorn.run` 다음에 `KeyboardInterrupt`가 생겨야 한다.
  - 에이전트가 Ctrl+C를 흉내 내는 방법(`_thread.interrupt_main(signal.SIGINT)`)으로 시험했더니, 서버는 정상으로 꺼졌다. 하지만 `KeyboardInterrupt`는 생기지 않고 `uvicorn.run`이 그냥 돌아왔다.
  - 그래서 진짜 Ctrl+C로 확인하려고, 새 콘솔 창을 띄워 그 창에 Ctrl+C(`CTRL_C_EVENT`)를 보냈다. 그랬더니 서버 정리 메시지 없이 바로 끝났다. 종료 코드는 `3221225786`(`0xC000013A`, "Ctrl+C로 끝남")이었다.
- **원인 조사**
  - 같은 방법으로 uvicorn 없이 아주 짧은 Python 코드에 Ctrl+C를 보냈다. 이번에는 Ctrl+C가 아예 전달되지 않았다(`10초가 그냥 지났습니다`).
  - 에이전트가 프로그램을 실행하는 환경에서는 진짜 Ctrl+C가 보통처럼 전달되지 않는다고 판단했다. 이 환경에서는 진짜 Ctrl+C 시험을 믿을 수 없다.
- **해결**
  - `main.py`는 두 경우를 모두 처리하게 두었다. `KeyboardInterrupt`가 와도 잡고, 오지 않고 `uvicorn.run`이 그냥 돌아와도 아래 줄이 실행된다.
  - 주석은 확인한 만큼만 쓰도록 "KeyboardInterrupt가 생길 **수 있다**"로 고쳤다.
  - 흉내 낸 신호로는 정상 종료를 확인했다. (4번 결과 4)
  - **진짜 Ctrl+C 확인은 개발자의 PowerShell에서 한다.** (7번)

그 밖의 문제는 없었다.

---

## 6. 결정한 것과 이유

| 결정 | 다른 선택지 | 고른 이유 |
| --- | --- | --- |
| `BackgroundScheduler` | `BlockingScheduler`, `AsyncIOScheduler` | 공식 문서: `BlockingScheduler`는 스케줄러만 도는 프로그램용이다. 이 프로그램에는 서버도 함께 돈다. `AsyncIOScheduler`는 `start()`할 때 이미 돌고 있는 서버의 실행 흐름(이벤트 루프)이 있어야 한다(설치된 코드에서 `get_running_loop()` 확인). 그러면 서버 안에서 시작해야 해서 아래의 lifespan 같은 새 문법이 필요하다. `BackgroundScheduler`는 서버와 상관없이 먼저 시작할 수 있다. |
| `main.py`에서 스케줄러를 먼저 시작하고 `uvicorn.run`으로 서버 실행 | FastAPI의 시작·종료 이벤트(lifespan)에서 스케줄러 켜기 | lifespan은 새 문법(`yield`, `asynccontextmanager`)이 여러 개 필요하다. `main.py`는 위에서 아래로 읽히는 순서가 실행 순서와 같아서 이해하기 쉽다. |
| 기본 알림 시각 7시 30분, `.env`로 바꿀 수 있게 | 시각을 코드에 고정 / 개발자에게 묻기 | CLAUDE.md는 "매일 아침 정해진 시각"이라고만 한다. 등교 전에 볼 수 있는 시각으로 정했고, `.env`의 `NOTIFY_HOUR`, `NOTIFY_MINUTE`로 언제든 바꿀 수 있다. |
| 주말·방학에도 매일 보냄 | 월~금만 보냄 | CLAUDE.md: 기능 표는 "매일", 변환 규칙은 "주말·방학·공휴일은 오류가 아닌 정상 상황 → 오늘은 급식이 없습니다." |
| 시간대를 따로 정하지 않음 (PC 시간대) | `Asia/Seoul`을 코드에 적기 | 스케줄러와 `date.today()`, 로그 시각이 모두 같은 PC 시계를 기준으로 하게 된다. PC 시간대가 `Asia/Seoul`인 것을 확인했다. |
| `misfire_grace_time` 1시간 | 기본값 1초 그대로 / 제한 없음(`None`) | 기본값이면 PC가 잠깐 바쁘거나 잠자기 상태여도 그날 알림을 건너뛴다. 제한이 없으면 저녁에 PC를 켰을 때 아침 알림이 늦게 나간다. 1시간이면 등교 시간 전후까지다. |
| `coalesce=True` | `False` | 여러 번 놓쳤어도 같은 알림이 여러 번 나가지 않게 한다. (기본값도 True지만, 뜻이 보이도록 직접 적었다) |
| 학사일정 조회가 실패하면 "학사일정을 가져오지 못했습니다."로 급식 알림은 보냄 + 관리자 알림 | 알림 전체를 보내지 않음 | 급식은 "필수", 학사일정은 "선택" 기능이다(CLAUDE.md). 선택 기능 때문에 필수 기능이 멈추면 안 된다. |
| 급식 조회가 실패하면 5단계처럼 메시지를 보내지 않음 | 학사일정만이라도 보냄 | 5단계 규칙 그대로. 메시지의 중심이 급식이라, 급식 없이 보내면 사용자가 "급식이 없는 날"로 오해할 수 있다. |
| 학사일정을 "오늘 하루"(시작일 = 끝일)로 조회 | 이번 주 일정을 받아 오늘 것만 고르기 | 필요한 만큼만 받는다. 8단계의 `fetch_schedules`를 고치지 않고 그대로 쓸 수 있다. |
| 함수 이름 `send_lunch_notification`을 그대로 둠 | `send_daily_notification`으로 바꾸기 | CLAUDE.md도 "정기 급식 알림에 학사일정을 함께 표시"라고 부른다. 이름을 바꾸면 앞 단계 문서와 이름이 달라진다. |
| 정기 알림 함수에서 `except Exception`으로 모든 오류를 잡음 | NEIS·Slack 오류만 잡기 | 잡지 않은 오류는 APScheduler가 화면에만 출력하고 로그 파일에는 남기지 않는다(직접 확인). 아침에는 화면을 보는 사람이 없다. |
| 스케줄러 테스트는 `start()` 하지 않고 예약 내용만 확인 | 테스트에서 스케줄러를 실제로 돌리기 | 테스트할 때마다 Slack으로 알림이 나가면 안 된다. 실제 실행은 통합 시험(4번 결과 4)으로 한 번 확인했다. |
| 통합 시험의 정기 알림은 실제 급식 알림 채널로 보냄 | 관리자 채널로 보내기 | 시각만 바꾸고 `main.py`를 그대로 실행해야 진짜 통합 시험이 된다. 4·5단계에서도 같은 채널로 시험 알림을 보냈다. |

---

## 7. 개발자가 직접 확인할 것

1. **진짜 Ctrl+C 종료**: `python main.py`로 켠 뒤 Ctrl+C를 누릅니다. 마지막 줄에 `프로그램을 종료했습니다.`가 나오는지 봅니다. (5번 문제 1)
2. **내일 아침 정기 알림**: 7시 30분에 `main.py`가 켜져 있어야 알림이 나갑니다. PC가 꺼져 있거나 프로그램이 꺼져 있으면 나가지 않습니다.

---

## 8. 다음 단계에서 할 일 (10단계: 정리)

1. `README.md`를 쓴다. (CLAUDE.md 10단계)
   - 구조도: 스케줄러·콜백 서버 → 조회 → 변환 → 전송
   - 실행 방법: 설치, `.env`, 처음 한 번 토큰 준비, `python main.py`, 터널
   - 막혔던 문제와 해결 과정: 1~9단계 개발 기록의 "발생한 문제와 해결"을 모아 정리
2. 네이버웍스 대신 Slack을 쓰게 된 결정과 이유도 README에 남긴다.

---

## 확인한 공식 문서

- APScheduler 3.x 사용 안내: https://apscheduler.readthedocs.io/en/3.x/userguide.html
- cron 방식: https://apscheduler.readthedocs.io/en/3.x/modules/triggers/cron.html
- `BackgroundScheduler`: https://apscheduler.readthedocs.io/en/3.x/modules/schedulers/background.html
- 스케줄러 공통 기능(`add_job`, `start`, `shutdown`, `get_job`): https://apscheduler.readthedocs.io/en/3.x/modules/schedulers/base.html
- 예약(`Job.next_run_time`): https://apscheduler.readthedocs.io/en/3.x/modules/job.html
- 공식 문서에 없던 것은 설치된 코드에서 확인했다.
  - APScheduler 기본값: `.venv/Lib/site-packages/apscheduler/schedulers/base.py`
  - uvicorn의 Ctrl+C 처리: `.venv/Lib/site-packages/uvicorn/server.py`의 `capture_signals`

## 이번 단계 핵심 정리

1. `python main.py` 하나로 콜백 서버와 정기 알림 스케줄러가 함께 돈다.
2. 정기 알림은 매일 7시 30분(`.env`로 변경 가능)에 급식과 오늘의 학사일정을 보낸다.
3. 학사일정이 실패해도 급식 알림은 보내고, 관리자에게 알린다.
4. 1시간까지 늦은 알림은 보내고, 예상하지 못한 오류도 로그와 관리자 알림으로 남긴다.
5. 통합 시험에서 정기 알림, 명령어 답장, 정상 종료를 모두 확인했다. 진짜 Ctrl+C는 개발자가 확인한다.
