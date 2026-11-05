# 8단계 개발 기록: 명령어 응답 (양방향 완성)

## 이 문서를 다 읽으면 할 수 있게 되는 것

1. 봇이 명령어마다 어떤 답장을 보내는지, 어떤 순서로 만드는지 설명할 수 있다.
2. 답장 기능을 미리보기·로컬 시험·실제 Slack 순서로 직접 확인할 수 있다.
3. 8단계에서 정한 기준(토요휴업일 숨김, "이번 주"의 범위, 답장 문구 등)과 그 이유를 알 수 있다.

---

## 1. 목표

- 명령어마다 데이터를 조회해 답장을 보낸다. (CLAUDE.md 명령어 표)

  | 보낸 말 | 답장 |
  | --- | --- |
  | `오늘 급식` | 오늘 중식 메뉴 |
  | `내일 급식` | 내일 중식 메뉴 |
  | `이번 주 일정` | 이번 주 학사일정 |
  | `도움말` 또는 그 밖의 말 | 사용 가능한 명령어 안내 |

- 조회·변환·전송은 정기 알림과 같은 모듈(`neis.py`, `formatter.py`, `sender.py`)을 쓴다. (CLAUDE.md: 모듈 중복 금지)
- 7단계에서 미룬 것도 확인한다.
  - 실제 Slack 요청이 서명 검증을 통과하는지
  - 봇이 자기 답장에 또 답하지 않는지
- → **양방향 완성**

---

## 2. 한 일 (순서대로)

1. **공식 문서 확인**
   - NEIS 학사일정 Open API 명세
     - 서비스 이름: `SchoolSchedule`
     - 요청 인자: `AA_FROM_YMD`(학사시작일자), `AA_TO_YMD`(학사종료일자)
     - 응답 항목: `AA_YMD`(학사일자), `EVENT_NM`(행사명), `SBTR_DD_SC_NM`(수업공제일명, 예: 휴업일)
   - Slack `chat.postMessage`: 받은 이벤트의 `channel`(1:1 대화방 ID)로 답장을 보낼 수 있다. 권한은 지금 가진 `chat:write`로 충분하다.
   - Slack Events API: 3초 안에 응답해야 하고, 늦으면 다시 보낸다.
   - FastAPI Background Tasks: `add_task`로 맡긴 함수는 응답을 돌려준 뒤에 실행된다.
2. **실제 학사일정 응답 보기**: 공개 예시 학교(서울고등학교)의 이번 주 일정을 받아 모양을 확인했다. (4번 결과 2)
3. **변환**: `app/formatter.py`에 학사일정 함수 3개를 추가했다. `format_lunch_message`에는 "급식 없음" 문구를 바꿀 수 있는 매개변수를 추가했다.
4. **조회**: `app/neis.py`에 `fetch_schedules`를 추가했다.
5. **답장 만들기**: `app/commands.py`에 날짜 계산 함수와 `build_reply`를 추가했다.
6. **답장 보내기**: `app/notifier.py`에 `send_command_reply`를 추가했다. NEIS 실패와 전송 실패는 관리자에게 알린다.
7. **서버**: `app/server.py`가 Slack에 먼저 200을 돌려주고, 답장은 `BackgroundTasks`로 뒤에서 보내게 했다.
8. **테스트**: 8개를 추가했다. (전체 60개)
9. **미리보기**: Slack으로 보내지 않고 화면에만 네 가지 답장을 만들어 봤다. (4번 결과 3)
10. **로컬 시험**: 서명한 `도움말` 이벤트를 로컬 서버에 보냈다. 처음에는 답장이 가지 않았다. (5번 문제) 서버를 다시 켠 뒤 성공했다. (4번 결과 4)
11. **실제 Slack 시험**: 개발자가 봇에게 명령어를 보냈고, 모두 답장을 받았다. (4번 결과 5)
12. **정리**
    - `오늘 급식`의 "오늘은 급식이 없습니다." 문구가 `commands.py`와 `formatter.py` 두 곳에 같은 글자로 있었다. `formatter.py`의 `NO_MEAL_TEXT` 하나만 쓰게 고쳤다. 테스트 60개 통과와 답장 모양(4번 결과 6)을 다시 확인하고 서버를 다시 켰다.
    - "토요휴업일이 매주 있다"는 근거를 세 학교의 실제 자료로 다시 확인했다. (4번 결과 2) 코드 주석도 확인한 범위에 맞게 고쳤다.
13. 학습 정리와 개발 기록을 쓰고, 비밀 정보가 커밋 대상에 없는지 확인한 뒤 커밋한다.

---

## 3. 바뀐 파일

| 파일 | 추가·수정 | 내용 |
| --- | --- | --- |
| `app/neis.py` | 수정 | `fetch_schedules` 추가 |
| `app/formatter.py` | 수정 | `NO_SCHEDULE_TEXT`, `HIDDEN_EVENT_NAMES`, `EVENT_SEPARATOR`, `group_events_by_date`, `format_schedule_lines`, `format_week_schedule_message` 추가. `format_lunch_message`에 `no_meal_text` 매개변수(기본값 있음) 추가 |
| `app/commands.py` | 수정 | `NO_LUNCH_TOMORROW_TEXT`, `to_yyyymmdd`, `week_start`, `week_end`, `make_lunch_reply`, `make_week_schedule_reply`, `build_reply` 추가 |
| `app/notifier.py` | 수정 | `COMMAND_FAILED_TEXT`, `send_command_reply` 추가 |
| `app/server.py` | 수정 | `BackgroundTasks`로 답장 맡기기 |
| `tests/test_formatter.py` | 수정 | 테스트 3개 추가 (내일 문구, 학사일정 묶기, 일정 없음) |
| `tests/test_commands.py` | 수정 | 테스트 5개 추가 (날짜 모양, 이번 주 계산 3개, 도움말 답장) |
| `docs/step08-learning.md` | 새 파일 | 8단계 학습 정리 |
| `docs/step08-devlog.md` | 새 파일 | 이 문서 |

폴더 구조는 바꾸지 않았다.

---

## 4. 실행 방법과 결과

### 개발자가 따라 할 순서

```powershell
cd C:\neis_groupware_bot
.venv\Scripts\Activate.ps1
python -m pytest
python -m uvicorn app.server:app --port 8000      # --reload는 붙이지 않는다 (5번 문제)
```

다른 PowerShell 창에서 터널을 켭니다. (step06 개발 기록 참고)

```powershell
& "$HOME\Downloads\cloudflared-windows-amd64.exe" tunnel --url http://127.0.0.1:8000
```

터널 주소가 바뀌었다면 Slack 앱 설정의 Event Subscriptions → Request URL을 `https://새주소/slack/events`로 바꿉니다. 그다음 Slack에서 봇과의 1:1 대화로 명령어를 보냅니다.

### 결과 1: 테스트

```
tests/test_commands.py::test_date_to_neis_format PASSED
tests/test_commands.py::test_this_week_from_thursday PASSED
tests/test_commands.py::test_this_week_from_monday_and_sunday PASSED
tests/test_commands.py::test_this_week_across_new_year PASSED
tests/test_commands.py::test_help_reply_does_not_need_neis PASSED
tests/test_formatter.py::test_format_lunch_message_with_tomorrow_wording PASSED
tests/test_formatter.py::test_week_schedule_groups_by_date_and_hides_saturday_holiday PASSED
tests/test_formatter.py::test_week_schedule_without_events PASSED
============================= 60 passed in 0.38s ==============================
```

### 결과 2: 학사일정 원본 (서울고등학교, 2026-11-02 ~ 11-08)

`head` 부분:

```json
{"head": [{"list_total_count": 7}, {"RESULT": {"CODE": "INFO-000", "MESSAGE": "정상 처리되었습니다."}}]}
```

`row`의 첫 번째 항목:

```json
{
  "ATPT_OFCDC_SC_CODE": "B10",
  "SD_SCHUL_CODE": "7010083",
  "AY": "2026",
  "AA_YMD": "20261102",
  "ATPT_OFCDC_SC_NM": "서울특별시교육청",
  "SCHUL_NM": "서울고등학교",
  "DGHT_CRSE_SC_NM": "주간",
  "SCHUL_CRSE_SC_NM": "고등학교",
  "EVENT_NM": "수학 하이챌린지(1,2)",
  "EVENT_CNTNT": "",
  "ONE_GRADE_EVENT_YN": "Y",
  "TW_GRADE_EVENT_YN": "Y",
  "THREE_GRADE_EVENT_YN": "N",
  "FR_GRADE_EVENT_YN": "*",
  "FIV_GRADE_EVENT_YN": "*",
  "SIX_GRADE_EVENT_YN": "*",
  "SBTR_DD_SC_NM": "해당없음",
  "LOAD_DTM": "20261105"
}
```

7개 행의 날짜, 행사 이름, 수업공제일 구분:

```
20261102 수학 하이챌린지(1,2) 해당없음
20261103 정보 하이챌린지 해당없음
20261104 수업공개의 날 해당없음
20261104 독서골든벨 해당없음
20261105 과학 하이챌린지(1,2) 해당없음
20261106 학교폭력예방교육 해당없음
20261107 토요휴업일 휴업일
```

이 자료에서 알게 된 것:

- 하루에 행사가 여러 개일 수 있다. (11월 4일)
- 일요일(11월 8일)처럼 행사가 없는 날은 행이 없다.
- 토요일에는 `토요휴업일`이 들어 있다.

세 학교의 실제 자료로 더 확인했다. (개발자 학교 이름은 적지 않았다)

```
서울고(B10/7010083): 행 27개, 11월 토요일 4개 중 토요휴업일 있는 토요일 4개, 같은 날 같은 행사 중복 0건
부산고등학교(C10/7150100): 행 7개, 11월 토요일 4개 중 토요휴업일 있는 토요일 4개, 같은 날 같은 행사 중복 0건
개발자 학교(.env): 행 8개, 11월 토요일 4개 중 토요휴업일 있는 토요일 4개, 같은 날 같은 행사 중복 0건
```

2026학년도 전체(2026-03-01 ~ 2027-02-28)로 넓혀 보니, 부산고등학교에는 같은 날 같은 행사가 두 번 들어 있는 경우가 8건 있었다.

```
부산고 행 225 중복 묶음 8
    20260302 대체공휴일 2 번
    20260501 노동절 2 번
    20260505 어린이날 2 번
    20260525 대체공휴일 2 번
    20260717 제헌절 2 번
```

(서울고와 개발자 학교는 0건)

### 결과 3: 답장 미리보기 (공개 예시 학교, Slack으로 보내지 않음)

```
===== 오늘 급식 (11월 5일 목) (0.11초)
[11월 5일(목) 중식]
흑미밥 / 부대찌개 / 호박볶음 / 오지치즈스틱 / 고등어구이 / 백김치
===== 내일 급식 (11월 7일 토 기준 → 일요일) (0.1초)
[11월 8일(일) 중식]
내일은 급식이 없습니다.
===== 이번 주 일정 (11월 5일 목 기준) (0.08초)
[11월 2일(월) ~ 11월 8일(일) 학사일정]
11월 2일(월) 수학 하이챌린지(1,2)
11월 3일(화) 정보 하이챌린지
11월 4일(수) 수업공개의 날, 독서골든벨
11월 5일(목) 과학 하이챌린지(1,2)
11월 6일(금) 학교폭력예방교육
===== 도움말 (0.0초)
사용할 수 있는 명령어입니다.
• 오늘 급식: 오늘 중식 메뉴
• 내일 급식: 내일 중식 메뉴
• 이번 주 일정: 이번 주 학사일정
• 도움말: 이 안내
```

괄호 안의 초는 NEIS 조회를 포함해 답장 글을 만드는 데 걸린 시간이다.

### 결과 4: 로컬 시험 (서명한 `도움말` 이벤트 → 관리자 채널로 답장)

실제 Signing Secret으로 서명했고, Secret 값은 출력하지 않았다.

```
status: 200 | body: ok | seconds until response: 0.02
```

로그(`logs/bot.log`, 채널 ID는 가림):

```
2026-11-05 17:55:23,128 [INFO] 명령어 해석: event_id=Ev-local-help-1793868923, 명령어=help
2026-11-05 17:55:23,498 [INFO] Slack 전송 성공: 채널 ***
2026-11-05 17:55:23,498 [INFO] 명령어 답장 완료: help
```

응답은 0.02초 만에 갔고, 답장은 그 뒤 0.37초 만에 전송이 끝났다.

### 결과 5: 실제 Slack 시험

개발자가 봇과의 1:1 대화로 명령어를 9번 보냈다. 로그에는 9번 모두 `명령어 답장 완료`가 남았다. 개발자도 Slack에서 답장이 온 것을 확인했다.

서버 화면 (주소와 포트는 가림):

```
[명령어] today_lunch | 보낸 글: 오늘 급식
INFO:     *** - "POST /slack/events HTTP/1.1" 200 OK
INFO:     *** - "POST /slack/events HTTP/1.1" 200 OK
[명령어] tomorrow_lunch | 보낸 글: 내일급식
INFO:     *** - "POST /slack/events HTTP/1.1" 200 OK
INFO:     *** - "POST /slack/events HTTP/1.1" 200 OK
[명령어] tomorrow_lunch | 보낸 글: 내일 급식
INFO:     *** - "POST /slack/events HTTP/1.1" 200 OK
INFO:     *** - "POST /slack/events HTTP/1.1" 200 OK
[명령어] this_week_schedule | 보낸 글: 이번 주 일정
INFO:     *** - "POST /slack/events HTTP/1.1" 200 OK
INFO:     *** - "POST /slack/events HTTP/1.1" 200 OK
[명령어] help | 보낸 글: 안녕
INFO:     *** - "POST /slack/events HTTP/1.1" 200 OK
INFO:     *** - "POST /slack/events HTTP/1.1" 200 OK
[명령어] help | 보낸 글: 다음 주 일정
INFO:     *** - "POST /slack/events HTTP/1.1" 200 OK
INFO:     *** - "POST /slack/events HTTP/1.1" 200 OK
[명령어] today_lunch | 보낸 글: 오늘 급식
INFO:     *** - "POST /slack/events HTTP/1.1" 200 OK
INFO:     *** - "POST /slack/events HTTP/1.1" 200 OK
[명령어] tomorrow_lunch | 보낸 글: 내일 급식
INFO:     *** - "POST /slack/events HTTP/1.1" 200 OK
INFO:     *** - "POST /slack/events HTTP/1.1" 200 OK
[명령어] this_week_schedule | 보낸 글: 이번 주 일정
INFO:     *** - "POST /slack/events HTTP/1.1" 200 OK
INFO:     *** - "POST /slack/events HTTP/1.1" 200 OK
```

로그 일부 (이벤트 ID와 채널 ID는 가림):

```
2026-11-05 17:55:59,639 [INFO] 명령어 해석: event_id=Ev***, 명령어=today_lunch
2026-11-05 17:55:59,756 [INFO] NEIS mealServiceDietInfo 호출 성공: 결과 코드 INFO-000
2026-11-05 17:56:00,092 [INFO] Slack 전송 성공: 채널 ***
2026-11-05 17:56:00,092 [INFO] 명령어 답장 완료: today_lunch
2026-11-05 17:56:00,248 [INFO] 사람이 보낸 새 메시지가 아니라 건너뜁니다: event_id=Ev***, subtype=None
```

확인한 것:

| 확인할 것 | 결과 |
| --- | --- |
| 실제 Slack 요청의 서명 검증 (7단계에서 미룬 것) | 요청 18개가 모두 통과했다. 시험하는 동안 "서명이 맞지 않는 요청" 로그는 없었다. |
| 띄어쓰기 무시 | `내일급식`과 `내일 급식` 모두 `tomorrow_lunch`로 해석했다. |
| 그 밖의 말 | `안녕`, `다음 주 일정`은 도움말로 답했다. |
| 답장 속도 | 명령어 해석부터 답장 전송 완료까지 0.33~0.45초였다. |
| 봇의 답장 무시 | 답장 하나마다 봇의 답장 이벤트가 하나씩 다시 들어왔다(18개 중 9개). 모두 "사람이 보낸 새 메시지가 아니라 건너뜁니다"로 처리되어, 봇이 자기 답장에 또 답하지 않았다. |

### 결과 6: `오늘 급식` 문구 정리 뒤 확인 (공개 예시 학교)

```
[11월 8일(일) 중식]
오늘은 급식이 없습니다.
[11월 8일(일) 중식]
내일은 급식이 없습니다.
```

첫 번째는 11월 8일(일)에 `오늘 급식`, 두 번째는 11월 7일(토)에 `내일 급식`을 보낸 경우다.

---

## 5. 발생한 문제와 해결

### 문제 1. 로컬 시험에서 답장이 가지 않음 (`--reload` 서버가 예전 코드로 동작)

- **상황**
  - 서명한 `도움말` 이벤트를 로컬 서버에 보냈다. 응답은 `200 ok`(0.004초)였다.
  - 로그에는 `명령어 해석: ... 명령어=help`만 있고 `명령어 답장 완료`가 없었다.
- **원인 조사**
  - 7단계에서 서버를 `--reload`(파일이 바뀌면 자동으로 다시 시작) 옵션으로 켜 두었다.
  - 서버 화면의 마지막 줄은 이것이었다.
    ```
    WARNING:  StatReload detected changes in 'app\server.py'. Reloading...
    ```
  - 그 뒤로 "다시 시작했다"는 줄이 나오지 않았다. 그런데 요청에는 계속 응답하고 있었다.
  - 켜져 있던 프로세스를 확인하니, `server.py`가 바뀌기 **전에** 시작된 작업 프로세스가 남아 응답하고 있었다. 이 프로세스의 `server.py`에는 답장을 맡기는 줄(`add_task`)이 없었다.
- **해결**
  - 서버 프로세스 세 개를 모두 끄고, `--reload` 없이 다시 켰다.
  - 같은 시험을 다시 하니 답장이 보내졌다. (4번 결과 4)
- **배운 것**: Windows에서는 `--reload`가 다시 시작하다 멈출 수 있다. 코드를 고친 뒤에는 서버를 직접 껐다 켜는 편이 확실하다. 이번 단계부터 `--reload`를 쓰지 않는다.

그 밖의 문제는 없었다. (터널이 끊기는 문제와 Request URL 확인 실패는 6단계에서 겪었다. step06 개발 기록 5번 참고)

---

## 6. 결정한 것과 이유

| 결정 | 다른 선택지 | 고른 이유 |
| --- | --- | --- |
| 답장은 `BackgroundTasks`로 응답 뒤에 보냄 | 답장을 다 보낸 뒤 응답 / 따로 작업 대기열 프로그램 쓰기 | Slack은 3초 안에 응답을 받아야 한다. NEIS가 실패하면 재시도 대기만 3초다. FastAPI에 들어 있는 기능이라 새 라이브러리가 필요 없다. |
| 답장은 이벤트의 `channel`(명령어를 보낸 1:1 대화방)로 | `.env`의 `SLACK_CHANNEL_ID`(정기 알림 채널) | 물어본 사람에게 답해야 한다. 정기 알림 채널에 답하면 다른 사람에게도 보인다. |
| 학사일정에서 `토요휴업일`만 이름으로 숨김 | 모두 보여 줌 / `SBTR_DD_SC_NM`이 "휴업일"인 것을 모두 숨김 | 세 학교 모두 매주 토요일에 들어 있어서, 그대로 두면 매주 같은 줄이 붙는다. 공휴일·재량휴업일 같은 다른 휴업일은 알아야 할 정보라서 남긴다. 숨길 이름은 목록 상수로 두어 나중에 더하기 쉽게 했다. |
| 같은 날 행사는 한 줄에 `, `로 잇고, 같은 이름은 한 번만 | 행사마다 한 줄 / 중복도 그대로 | 메시지가 짧아진다. 실제 자료(부산고)에 같은 날 같은 행사가 두 번 온 경우가 있었다. |
| 날짜순은 `sorted`로 직접 맞춤 | NEIS 응답 순서를 그대로 믿음 | 응답 순서에 기대지 않아도 늘 날짜순이 된다. |
| 일정이 없으면 `없음` | "이번 주는 일정이 없습니다." 등 | CLAUDE.md 메시지 예시(`[오늘의 학사일정]` 아래 `없음`)와 같은 말을 쓴다. 9단계 정기 알림과도 맞춘다. |
| "이번 주"는 월요일~일요일 | 오늘부터 7일 / 월~금 | 달력의 한 주와 같아서 헷갈리지 않는다. 주말에 있는 행사도 보이게 일요일까지 포함한다. |
| `내일 급식`에 급식이 없으면 "내일은 급식이 없습니다." | "오늘은 급식이 없습니다." 그대로 | 7단계 개발 기록에서 남긴 일. "내일 급식"에 "오늘은…"은 어색하다. 기본값 매개변수로 더해서 정기 알림 코드와 테스트는 고치지 않았다. |
| `오늘 급식`의 문구는 `formatter.py`의 `NO_MEAL_TEXT`를 그대로 씀 | `commands.py`에 같은 글자를 하나 더 둠 | 같은 글자를 두 곳에 두면 한쪽만 고치는 실수가 생긴다. |
| NEIS 실패 시 사용자에게 "지금은 정보를 가져오지 못했습니다…" + 관리자 알림 | 아무 답도 하지 않음 / 오류 내용을 그대로 보여 줌 | 답이 없으면 사용자는 봇이 고장 났는지 모른다. 오류 내용은 관리자만 보면 된다. (CLAUDE.md: 실패하면 관리자에게 오류 알림) |
| 답장 글 만들기는 `commands.py`, 보내기는 `notifier.py` | 서버 파일에 모두 넣기 | 조회(`neis.py`), 변환(`formatter.py`), 전송(`sender.py`)을 정기 알림과 함께 쓴다. `notifier.py`가 `commands.py`를 가져다 쓰고, 반대 방향으로는 가져오지 않는다. 두 파일이 서로를 가져오면 Python이 파일을 읽다가 오류를 낼 수 있어서다. |
| `build_reply`가 오늘 날짜를 매개변수로 받음 | 함수 안에서 `date.today()` | 테스트에서 원하는 날짜를 넣을 수 있다. 실제 오늘 날짜는 `notifier.py`가 넣는다. |
| 급식·일정 답장은 자동 테스트 대신 미리보기와 실제 시험으로 확인 | 가짜 NEIS 응답을 끼워 넣는 테스트 | 가짜 응답을 끼워 넣는 방법(모의 객체)은 새 개념이 많아 이번 단계에 넣지 않았다. 변환 함수는 이미 실제 자료로 테스트하고 있다. |
| 로컬 시험의 답장은 관리자 채널로 | 개발자의 1:1 대화방 | 에이전트는 개발자의 1:1 대화방 ID를 모른다. 도움말 안내문이라 학교 정보도 들어 있지 않다. |
| 미리보기와 문서의 예시는 공개 예시 학교(서울고) 자료 | 개발자 학교 자료 | 문서에 개발자의 학교가 드러나지 않게 했다. |
| Slack 권한은 추가하지 않음 | `im:write` 등 추가 | 받은 이벤트의 대화방으로 보내는 데는 `chat:write`로 충분했다. 실제 시험에서 답장 9번이 모두 성공했다. |
| 서버를 `--reload` 없이 실행 | 7단계처럼 `--reload` | 5번 문제. 7단계의 결정을 바꿨다. |

---

## 7. 다음 단계에서 할 일 (9단계: 통합)

1. **APScheduler 공식 문서를 확인**하고 `requirements.txt`에 버전을 고정해 추가한다.
2. **스케줄러와 콜백 서버를 한 프로그램으로 합친다.** 서버를 켜면 매일 아침 정해진 시각에 정기 알림도 보내게 한다.
3. **알림 시각**은 `.env`에서 바꿀 수 있게 하고, 기본값을 정한다.
4. **정기 알림에 오늘의 학사일정을 더한다.** CLAUDE.md 메시지 예시를 따른다.
   ```
   [11월 5일(목) 중식]
   쌀밥 / 된장찌개 / 제육볶음 / 배추김치 / 요구르트

   [오늘의 학사일정]
   없음
   ```
   이번 단계의 `group_events_by_date`를 그대로 쓴다.
5. 학사일정 조회가 실패해도 급식 알림은 보낼지 정한다.

---

## 확인한 공식 문서

- NEIS 학사일정 Open API: https://open.neis.go.kr/portal/data/service/selectServicePage.do?infId=OPEN17220190722175038389180&infSeq=2
  - 명세 자료(요청 인자, 응답 항목): https://open.neis.go.kr/portal/data/openapi/selectOpenApiMeta.do (POST, `infId=OPEN17220190722175038389180`, `infSeq=2`)
  - 호출 주소: `https://open.neis.go.kr/hub/SchoolSchedule`
- Slack `chat.postMessage`: https://docs.slack.dev/reference/methods/chat.postMessage/
- Slack Events API (3초 규칙, 재전송): https://docs.slack.dev/apis/events-api/
- Slack `message.im` 이벤트: https://docs.slack.dev/reference/events/message.im/
- FastAPI Background Tasks: https://fastapi.tiangolo.com/tutorial/background-tasks/

## 이번 단계 핵심 정리

1. `오늘 급식`, `내일 급식`, `이번 주 일정`, `도움말`에 답장한다. → 양방향 완성
2. 서버는 Slack에 먼저 200을 돌려주고, 답장은 `BackgroundTasks`로 뒤에서 명령어를 보낸 대화방에 보낸다.
3. 학사일정은 날짜별로 묶고, 토요휴업일과 중복을 빼고, 없으면 `없음`으로 답한다.
4. 실제 Slack 요청 18개가 서명 검증을 통과했고, 봇은 자기 답장에 답하지 않았다.
5. Windows에서는 `--reload`가 멈출 수 있어서, 코드를 고치면 서버를 직접 다시 켠다.
