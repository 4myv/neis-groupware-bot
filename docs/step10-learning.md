# 10단계 학습 정리: 정리 (README와 프로그램 전체 흐름)

## 이 문서를 다 읽으면 할 수 있게 되는 것

1. README가 무엇이고, 마크다운으로 제목·목록·표·코드를 쓰는 방법을 설명할 수 있다.
2. 아침 알림 하나, 명령어 답장 하나가 어느 파일의 어느 함수를 차례로 거치는지 따라갈 수 있다.
3. 1~9단계에서 배운 Python 문법이 이 프로젝트의 어디에 쓰였는지 찾아갈 수 있다.

## 읽기 전에

- 이번 단계에서는 **새 Python 코드를 쓰지 않았습니다.** 그래서 새 문법 대신 지금까지 만든 프로그램 전체를 한 번에 따라가 봅니다.
- 실행 결과는 9단계 통합 시험(2026-11-05 18:29)의 실제 로그입니다. 채널 ID는 `***`로 가렸습니다.
- 앞 단계에서 설명한 것은 "step05 참고"처럼 적었습니다.

---

## 1. 이번 단계에서 새로 나온 것

**개념**

1. README: 프로젝트의 첫 안내문
2. 마크다운: 기호로 모양을 적는 글쓰기 방법

**Python 문법**: 새로 나온 것 없음

---

## 2. 하나씩 설명

### 2-1. README: 프로젝트의 첫 안내문

**설명**

README(리드미)는 "나를 먼저 읽어라"라는 뜻의 파일입니다. 프로젝트 맨 위 폴더에 `README.md`라는 이름으로 둡니다.

GitHub는 저장소 첫 화면에 README를 자동으로 보여 줍니다. 그래서 처음 보는 사람이 가장 먼저 읽는 문서입니다.

CLAUDE.md는 README에 세 가지를 넣으라고 합니다.

1. 구조도
2. 실행 방법
3. 막혔던 문제와 해결 과정

이 프로젝트의 README에는 여기에 "할 수 있는 일", "폴더 구조", "알아 둘 점", "주요 결정", "문서 목록", "확인한 공식 문서"를 더했습니다.

**비유**

새로 산 물건의 상자에 든 사용 설명서입니다. 무엇을 하는 물건인지, 어떻게 켜는지, 고장 나면 어떻게 하는지가 들어 있습니다.

**Java 비교**

Spring Boot 프로젝트도 GitHub에 올릴 때 똑같이 `README.md`를 둡니다. 언어와 상관없이 쓰는 관례입니다.

**자주 하는 실수: 실행 방법을 "내 컴퓨터 기준"으로만 쓴다**

"그냥 `python main.py` 하면 됨"이라고만 쓰면, 처음 받은 사람은 `.env`, 토큰 준비, 가상환경을 모릅니다. README는 **처음 받은 사람이 순서대로 따라 할 수 있게** 씁니다. 그래서 이 프로젝트의 README는 설치 → `.env` → Slack 설정 → 토큰 → 실행 → 터널 순서로 적었습니다.

---

### 2-2. 마크다운: 기호로 모양을 적는 글쓰기 방법

**설명**

마크다운(Markdown)은 `#`, `-`, `|` 같은 기호로 제목, 목록, 표를 적는 방법입니다. 파일 이름 끝이 `.md`입니다.

메모장으로 열면 기호가 그대로 보입니다. GitHub나 VS Code 미리 보기로 열면 기호 대신 꾸며진 모양으로 보입니다.

이 프로젝트의 문서(`README.md`, `docs/*.md`, `CLAUDE.md`)는 모두 마크다운입니다.

**자주 쓰는 기호**

| 쓰는 법 | 보이는 모양 |
| --- | --- |
| `# 제목` | 큰 제목 (`#`이 많을수록 작은 제목: `##`, `###`) |
| `- 항목` | 점이 붙은 목록 |
| `1. 항목` | 번호가 붙은 목록 |
| `**굵게**` | **굵게** |
| `` `코드` `` | `코드` (글자 폭이 같은 글꼴, 회색 배경) |
| `[글자](주소)` | 누르면 주소로 가는 링크 |
| 줄 맨 앞에 `>` | 왼쪽에 세로줄이 있는 인용 상자 |

**코드 블록**: 줄 맨 앞에 백틱 세 개(```` ``` ````)를 쓰고, 끝에도 세 개를 씁니다. 그 사이의 줄은 쓴 그대로(띄어쓰기 포함) 보입니다. 첫 백틱 뒤에 `python`, `powershell`처럼 언어 이름을 적으면 색이 입혀집니다.

````
```powershell
python main.py
```
````

**표**: `|`로 칸을 나누고, 둘째 줄에 `| --- | --- |`를 씁니다. 이 둘째 줄이 "첫 줄은 제목 줄"이라는 표시입니다.

```
| 명령어 | 답장 |
| --- | --- |
| `오늘 급식` | 오늘 중식 메뉴 |
```

GitHub에서 보이는 모양: 제목 줄이 굵은 2칸짜리 표가 되고, 그 아래에 `오늘 급식 | 오늘 중식 메뉴` 한 줄이 들어갑니다.

**접기**: 확인 문제의 정답을 접어 둔 방법입니다. 마크다운 안에 HTML 태그 `<details>`를 씁니다.

```
<details><summary>정답</summary>

여기에 정답

</details>
```

GitHub에서 보이는 모양: "▶ 정답"만 보이고, 누르면 펼쳐집니다.

**이 프로젝트에서는** (`README.md`의 명령어 표)

```
| 명령어 | 답장 |
| --- | --- |
| `오늘 급식` | 오늘 중식 메뉴 |
| `내일 급식` | 내일 중식 메뉴 |
| `이번 주 일정` | 이번 주(월~일) 학사일정 |
| `도움말` 또는 그 밖의 말 | 사용할 수 있는 명령어 안내 |
```

**Java 비교**

Java의 설명 주석(Javadoc)은 HTML 태그로 꾸밉니다. 마크다운은 태그 대신 짧은 기호를 써서, 꾸미지 않은 글로 읽어도 알아보기 쉽습니다.

**자주 하는 실수: 표의 둘째 줄(`| --- |`)을 빠뜨린다**

```
| 명령어 | 답장 |
| `오늘 급식` | 오늘 중식 메뉴 |
```

이렇게 쓰면 표가 되지 않습니다. `|` 기호가 그대로 보이는 평범한 글 두 줄로 나옵니다.

---

## 3. 프로그램 전체 흐름 따라가기

이번 단계는 새 코드가 없으므로, 대신 **지금까지 만든 코드를 한 번에 따라갑니다.** 각 줄 오른쪽의 "단계"는 그 코드를 만든 단계입니다.

### 3-1. 프로그램 켜기: `python main.py`

| 순서 | 파일 · 함수 | 하는 일 | 단계 |
| --- | --- | --- | --- |
| 1 | `app/config.py` | `.env`를 읽어 설정값을 준비한다 (`load_dotenv`, `os.getenv`) | 01, 09 |
| 2 | `app/log.py` | 로그 파일 `logs/bot.log`를 준비한다 | 05 |
| 3 | `main.py` → `create_scheduler()` | 매일 7시 30분 예약을 만든다 | 09 |
| 4 | `main.py` → `scheduler.start()` | 스케줄러가 다른 스레드에서 시계를 보기 시작한다 | 09 |
| 5 | `main.py` → `uvicorn.run(app, ...)` | 콜백 서버(`app/server.py`의 `app`)가 요청을 기다린다 | 06, 09 |

실행 결과(로그):

```
2026-11-05 18:27:58,938 [INFO] 프로그램 시작: 정기 알림 다음 실행 시각 2026-11-05 18:29:00+09:00
```

### 3-2. 아침 알림 하나가 나가기까지

| 순서 | 파일 · 함수 | 하는 일 | 단계 |
| --- | --- | --- | --- |
| 1 | `scheduler.py` → `send_today_notification()` | 정해진 시각이 되면 스케줄러가 부른다. 오늘 날짜를 `"20261105"` 모양으로 만든다 | 09 |
| 2 | `notifier.py` → `send_lunch_notification(meal_date)` | 정기 알림을 처음부터 끝까지 맡는다 | 05, 09 |
| 3 | `neis.py` → `fetch_meals` → `call_neis_api` → `try_neis_once` | NEIS에 급식을 요청한다. 실패하면 3초 뒤 한 번 더 시도한다 | 02, 05 |
| 4 | `formatter.py` → `format_lunch_message` | `<br/>` 나누기, 알레르기 번호 빼기, 날짜 바꾸기로 급식 부분을 만든다 | 03 |
| 5 | `notifier.py` → `make_today_schedule_section` → `neis.py` → `fetch_schedules` | 오늘의 학사일정을 요청한다. 실패해도 급식 알림은 계속 간다 | 08, 09 |
| 6 | `formatter.py` → `format_today_schedule`, `format_daily_message` | 학사일정 부분을 만들고, 빈 줄을 사이에 두고 합친다 | 08, 09 |
| 7 | `sender.py` → `post_message` | Slack `chat.postMessage`로 보낸다. 토큰 오류면 새 토큰으로 한 번 더 보낸다 | 04, 05 |
| 8 | `auth.py` → `get_access_token` | 저장된 토큰을 꺼낸다. 만료 5분 전이면 새로 발급받아 저장한다 | 04 |

실행 결과(로그) — 각 줄을 남긴 곳:

```
2026-11-05 18:29:00,015 [INFO] 정기 알림 시작: 20261105                              ← scheduler.py 1번
2026-11-05 18:29:00,110 [INFO] NEIS mealServiceDietInfo 호출 성공: 결과 코드 INFO-000  ← neis.py 3번
2026-11-05 18:29:00,214 [INFO] NEIS SchoolSchedule 호출 성공: 결과 코드 INFO-200      ← neis.py 5번 (이날 일정 없음)
2026-11-05 18:29:00,550 [INFO] Slack 전송 성공: 채널 ***                              ← sender.py 7번
2026-11-05 18:29:00,550 [INFO] 20261105 급식 알림 완료                                 ← notifier.py 2번
```

### 3-3. 명령어 답장 하나가 나가기까지

| 순서 | 파일 · 함수 | 하는 일 | 단계 |
| --- | --- | --- | --- |
| 1 | (밖) 사용자 → Slack → 터널 | 봇과의 1:1 대화에 보낸 글이 `POST /slack/events`로 들어온다 | 06 |
| 2 | `server.py` → `receive_slack_event` | 원래 본문(바이트)과 서명 헤더를 읽는다 | 06, 07 |
| 3 | `auth.py` → `is_valid_slack_request` | 서명이 맞는지, 5분 안의 요청인지 확인한다. 아니면 401 | 07 |
| 4 | `server.py` → `is_duplicate_event`, `is_user_message` | 이미 처리한 이벤트나 봇의 메시지면 건너뛴다 | 07 |
| 5 | `commands.py` → `parse_command` | 띄어쓰기를 지우고 명령어 표에서 찾는다 | 07 |
| 6 | `server.py` → `background_tasks.add_task(...)` | 답장은 뒤로 맡기고 Slack에 바로 200을 돌려준다 (3초 규칙) | 08 |
| 7 | `notifier.py` → `send_command_reply` | 응답이 나간 뒤 실행된다 | 08 |
| 8 | `commands.py` → `build_reply` | 명령어마다 NEIS 조회(`neis.py`)와 변환(`formatter.py`)으로 답장 글을 만든다 | 08 |
| 9 | `sender.py` → `post_message` | 명령어가 온 1:1 대화로 답장을 보낸다 | 04, 08 |

실행 결과(로그):

```
2026-11-05 18:28:09,077 [INFO] 명령어 해석: event_id=Ev-local-help-1793870889, 명령어=help  ← server.py 5번
2026-11-05 18:28:09,466 [INFO] Slack 전송 성공: 채널 ***                                   ← sender.py 9번
2026-11-05 18:28:09,467 [INFO] 명령어 답장 완료: help                                       ← notifier.py 7번
```

### 3-4. 문제가 생기면 어디서 처리하나

| 상황 (CLAUDE.md 예외 처리 표) | 처리하는 곳 | 단계 |
| --- | --- | --- |
| 급식이 없는 날 | `formatter.py`의 `find_lunch_row`가 `{}` → "오늘은 급식이 없습니다." | 03 |
| NEIS 응답 없음·오류 | `neis.py`의 `call_neis_api`가 한 번 재시도 → `NeisError` → `notifier.py`가 관리자 알림 | 05 |
| Access Token 만료 | `auth.py`의 `get_access_token`이 미리 재발급, `sender.py`가 토큰 오류면 재발급 후 재전송 | 04, 05 |
| 서명이 맞지 않는 콜백 | `server.py`가 401로 거부하고 로그 | 07 |
| 콜백 중복 수신 | `server.py`의 `is_duplicate_event`가 바로 200, 처리는 한 번만 | 07 |
| 학사일정만 실패 | `notifier.py`의 `make_today_schedule_section`이 대신할 문구로 바꾸고 관리자 알림 | 09 |
| 생각하지 못한 오류 (정기 알림) | `scheduler.py`의 `except Exception`이 로그와 관리자 알림 | 09 |

---

## 4. 단계별로 배운 Python 문법 한눈에 보기

| 단계 | 배운 것 | 이 프로젝트에서 쓰인 곳 (예) |
| --- | --- | --- |
| 01 | 파일 실행, 가상환경, pip, `.env`, 변수, 타입 힌트, `if`/`else`와 들여쓰기, `import`, `None`, 상수 | `app/config.py` |
| 02 | `def`/`return`, 딕셔너리, 리스트, `for`, 키워드 인자, `input()`, 메서드, `requests`, `json` | `app/neis.py`, `find_school.py` |
| 03 | `split`/`strip`/`join`, 슬라이싱, `append`, `in`/`not in`, `datetime.strptime`, f-문자열, `\n`, pytest와 `assert` | `app/formatter.py`, `tests/` |
| 04 | `requests.post`, HTTP 헤더, `pathlib`, `with open`, `json.dump`/`load`, `time.time()`, `-> None` | `app/auth.py`, `app/sender.py` |
| 05 | `try`/`except`, `raise`, 직접 만든 예외(`class`), `from None`, `and`, `logging`, `time.sleep` | `app/neis.py`, `app/notifier.py`, `app/log.py` |
| 06 | 웹 서버, FastAPI, 데코레이터(`@app.post`), `async`/`await`, `dict.get`, `urlencode`, `secrets` | `app/server.py`, `reinstall_slack_app.py` |
| 07 | 바이트와 `encode`, `hmac`/`hashlib`, `int()`/`abs()`, 집합(`set`), `dict[str, str]` | `app/auth.py`, `app/commands.py` |
| 08 | `date`/`timedelta`, `strftime`, 기본값 매개변수, `continue`, `dict[str, list[str]]`, `sorted`, 함수를 값으로 넘기기, `BackgroundTasks` | `app/commands.py`, `app/formatter.py` |
| 09 | 스케줄러(APScheduler), 스레드, `except Exception`, `KeyboardInterrupt`, `uvicorn.run` | `app/scheduler.py`, `main.py` |

---

## 5. 사용한 라이브러리 (프로젝트 전체)

| 라이브러리 | 종류 | 하는 일 | 처음 쓴 단계 |
| --- | --- | --- | --- |
| python-dotenv | 따로 설치 | `.env`를 읽는다 | 01 |
| requests | 따로 설치 | NEIS, Slack에 HTTP 요청을 보낸다 | 02 |
| pytest | 따로 설치 | 테스트를 실행한다 | 03 |
| FastAPI, Uvicorn | 따로 설치 | 콜백 서버를 만들고 실행한다 | 06 |
| APScheduler | 따로 설치 | 매일 정해진 시각에 함수를 실행한다 | 09 |
| json, datetime, pathlib, time, logging, urllib.parse, secrets, hmac, hashlib, os, sys | 표준 (설치 필요 없음) | JSON, 날짜, 경로, 시각, 로그, 주소, 무작위 값, 서명, 환경 변수 | 01~09 |

---

## 6. 용어 정리

| 용어 | 쉬운 뜻 | 예시 |
| --- | --- | --- |
| README | 프로젝트를 처음 보는 사람이 먼저 읽는 안내문 | `README.md` |
| 마크다운 | `#`, `-`, 세로줄 같은 기호로 모양을 적는 글쓰기 방법 | `.md` 파일 |
| 코드 블록 | 백틱 세 개로 감싸 쓴 그대로 보이게 하는 부분 | ```` ```powershell ```` |
| 흐름 | 요청 하나가 거쳐 가는 함수의 순서 | 스케줄러 → 알림 → 조회 → 변환 → 전송 |

---

## 7. 개발자 질문과 답 (9~10단계 중)

### 질문 1. "아침 알림은 뭐야?"

9단계에서 만든 **정기 급식 알림**입니다.

- 매일 아침 7시 30분에, `.env`의 `SLACK_CHANNEL_ID` 채널로 보냅니다.
- 오늘 중식 메뉴와 `[오늘의 학사일정]`을 한 메시지로 보냅니다.
- `python main.py`로 켠 프로그램 안의 스케줄러가 보냅니다. 그래서 그 시각에 PC와 `main.py`가 켜져 있어야 합니다.
- PC가 잠자기 상태였어도 1시간 안에 깨어나면 늦게라도 보냅니다. (step09 2-5)
- 시각은 `.env`의 `NOTIFY_HOUR`, `NOTIFY_MINUTE`로 바꿉니다. (step09 2-9)

### 질문 2. "터널은 계속 수동으로 켜줘야 해?"

지금 방식(Cloudflare Quick Tunnel)에서는 그렇습니다. 그런데 터널은 **명령어 답장에만** 필요합니다.

- **아침 알림**: 우리 프로그램이 Slack으로 **보내기만** 합니다. 터널이 필요 없습니다.
- **명령어 답장**: Slack이 우리 PC로 **먼저 연락**해야 합니다. 집 PC는 인터넷에서 바로 찾아올 수 없어서 터널이 필요합니다.

Quick Tunnel은 계정 없이 쓰는 대신, 켤 때마다 주소가 바뀌고 가끔 끊깁니다. 그래서 켤 때마다 Slack의 Request URL을 바꿔야 합니다.

| 방법 | 좋은 점 | 걸리는 점 |
| --- | --- | --- |
| 지금처럼 Quick Tunnel | 계정이 필요 없음 | 매번 켜고 주소를 바꿔야 함 |
| 주소가 고정된 터널 | Request URL을 한 번만 등록 | 계정(일부는 도메인)이 필요하고, 가입 나이 조건을 확인하지 못함 |
| Slack Socket Mode | 터널이 아예 필요 없음 (우리 프로그램이 Slack에 먼저 연결) | 6~7단계의 콜백 서버와 서명 검증을 쓰지 않게 되어, 이 프로젝트의 목표인 "콜백 수신" 학습이 빠짐 |

이 프로젝트는 콜백 수신을 배우는 것이 목표라서 지금 방식을 유지했습니다. Socket Mode는 공식 문서를 확인한 뒤 추가 단계로 해 볼 수 있습니다.

---

## 8. 확인 문제

### 문제 1. 코드 읽기: 출력은?

1~9단계에서 만든 함수를 그대로 불러 씁니다.

```python
from app.formatter import format_date, remove_allergy_numbers
from app.commands import parse_command

print(format_date("20261106"))
print(remove_allergy_numbers("된장찌개(5.6.9.)"))
print(parse_command(" 이번주 일정 "))
```

<details><summary>정답</summary>

```
11월 6일(금)
된장찌개
this_week_schedule
```

- `format_date`: `"20261106"`을 날짜로 읽고 요일을 붙입니다. (step03)
- `remove_allergy_numbers`: 맨 뒤 괄호 안이 숫자와 점뿐이면 괄호째 지웁니다. (step03)
- `parse_command`: 띄어쓰기를 모두 지우면 `이번주일정`이고, 명령어 표에 있어서 `this_week_schedule`입니다. (step07)

</details>

### 문제 2. 빈칸 채우기: 아침 알림의 흐름

```
scheduler.py의 send_today_notification
  → notifier.py의 ____________________
    → neis.py의 fetch_meals
    → formatter.py의 format_lunch_message
    → neis.py의 _______________ (오늘의 학사일정)
    → sender.py의 ____________
```

<details><summary>정답</summary>

- `send_lunch_notification`: 정기 알림 하나를 처음부터 끝까지 맡습니다. (step05, step09)
- `fetch_schedules`: 학사일정을 가져옵니다. 오늘 하루만 가져오려고 시작일과 끝일을 같은 날로 넘깁니다. (step08, step09)
- `post_message`: Slack으로 보냅니다. 토큰 오류면 새 토큰으로 한 번 더 보냅니다. (step04, step05)

</details>

### 문제 3. 작은 수정: README의 표가 표로 보이지 않습니다. 고치세요.

```
| 명령어 | 답장 |
| `오늘 급식` | 오늘 중식 메뉴 |
| `내일 급식` | 내일 중식 메뉴 |
```

<details><summary>정답</summary>

```
| 명령어 | 답장 |
| --- | --- |
| `오늘 급식` | 오늘 중식 메뉴 |
| `내일 급식` | 내일 중식 메뉴 |
```

둘째 줄에 `| --- | --- |`가 있어야 "첫 줄은 제목 줄이고 이것은 표다"라고 알아봅니다. 칸 수(2칸)도 첫 줄과 맞춥니다. (2-2)

</details>

---

## 이번 단계 핵심 정리

1. README는 처음 보는 사람이 따라 할 수 있게 구조, 실행 방법, 막혔던 문제를 적는 안내문이다.
2. 마크다운은 `#`(제목), `-`(목록), `|`와 `| --- |`(표), 백틱 세 개(코드)로 모양을 적는다.
3. 아침 알림: `scheduler.py` → `notifier.py` → `neis.py` → `formatter.py` → `sender.py`(+`auth.py`).
4. 명령어 답장: `server.py`(서명 검증·명령어 해석·먼저 응답) → `notifier.py` → `commands.py` → 같은 조회·변환·전송.
5. 두 흐름이 같은 조회·변환·전송 모듈을 함께 쓴다. (CLAUDE.md: 모듈 중복 금지)
