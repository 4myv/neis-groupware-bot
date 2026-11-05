# 7단계 개발 기록: 서명 검증과 명령어 해석

## 이 문서를 다 읽으면 할 수 있게 되는 것

1. 콜백 서버가 가짜 요청, 중복 요청, 봇 메시지를 어떻게 걸러내는지 설명할 수 있다.
2. 서명 검증이 제대로 되는지 테스트와 로컬 시험으로 직접 확인할 수 있다.
3. 7단계에서 정한 기준과 그 이유를 알 수 있다.

---

## 1. 목표

- 가짜 요청을 거부한다. (CLAUDE.md: 서명이 맞지 않는 콜백 → 요청을 거부하고 로그에 기록)
- 명령어를 분기한다. 띄어쓰기 차이는 무시하고, 그 밖의 말은 도움말로 본다.
- 6단계 개발 기록에서 약속한 두 가지도 한다.
  - 같은 이벤트는 한 번만 처리한다. (CLAUDE.md: 콜백 중복 수신)
  - 봇 메시지는 무시한다. (8단계 답장의 무한 반복 방지)
- 답장은 8단계에서 한다.

---

## 2. 한 일 (순서대로)

1. **공식 문서 확인**
   - "Verifying requests from Slack"에서 서명 계산 순서와 **계산 예시 값**(Secret, 시각, 본문, 정답 서명)을 확인했다.
   - `message` 이벤트 문서에서 봇 메시지(`bot_id`)와 `subtype` 목록을 확인했다.
2. **서명 검증**: `app/auth.py`에 `make_slack_signature`, `is_valid_slack_request`를 추가했다. `app/config.py`에 `SLACK_SIGNING_SECRET`을 추가했다.
3. **명령어 해석**: `app/commands.py`를 만들었다. 띄어쓰기를 모두 지운 뒤 명령어 표에서 찾는다.
4. **서버**: `app/server.py`를 고쳤다. 순서는 다음과 같다.
   1. 서명 확인
   2. 주소 확인 요청 처리
   3. 중복 확인
   4. 사람 메시지인지 확인
   5. 명령어 해석
5. **테스트**: 15개를 추가했다(전체 52개).
   - 서명 테스트의 정답은 공식 문서의 예시 값 그대로다.
6. **서버 다시 켜기**: 켜져 있던 6단계 서버를 끄고, 파일이 바뀌면 자동으로 다시 시작하는 옵션(`--reload`)으로 다시 켰다. 8단계에서 코드를 고칠 때 바로 반영하기 위해서다.
7. **로컬 시험**: 실제 Signing Secret으로 서명한 요청과 가짜 요청 10가지를 보냈다. (4번 결과 2)
8. 학습 정리와 개발 기록을 쓰고, 비밀 파일이 커밋 대상에 없는지 확인한 뒤 커밋한다.

---

## 3. 바뀐 파일

| 파일 | 추가·수정 | 내용 |
| --- | --- | --- |
| `app/auth.py` | 수정 | `SIGNATURE_VERSION`, `MAX_REQUEST_AGE_SECONDS`, `make_slack_signature`, `is_valid_slack_request` |
| `app/commands.py` | 새 파일 | 명령어 이름 상수, 명령어 표, `remove_spaces`, `parse_command` |
| `app/server.py` | 수정 | 서명 확인, 중복 확인(`is_duplicate_event`), 사람 메시지 확인(`is_user_message`), 명령어 해석 |
| `app/config.py` | 수정 | `SLACK_SIGNING_SECRET` 추가 |
| `tests/test_signature.py` | 새 파일 | 서명 테스트 6개 |
| `tests/test_commands.py` | 새 파일 | 명령어·이벤트 거르기 테스트 9개 |
| `docs/step07-learning.md` | 새 파일 | 7단계 학습 정리 |
| `docs/step07-devlog.md` | 새 파일 | 이 문서 |

---

## 4. 실행 방법과 결과

### 개발자가 따라 할 순서

```powershell
cd C:\neis_groupware_bot
.venv\Scripts\Activate.ps1
python -m pytest -v tests/test_signature.py tests/test_commands.py
python -m uvicorn app.server:app --port 8000 --reload     # 코드가 바뀌면 자동으로 다시 시작
```

### 결과 1: 테스트

```
tests/test_signature.py::test_signature_matches_official_example PASSED
tests/test_signature.py::test_valid_request_is_accepted PASSED
tests/test_signature.py::test_changed_body_is_rejected PASSED
tests/test_signature.py::test_wrong_secret_is_rejected PASSED
tests/test_signature.py::test_old_request_is_rejected_even_with_correct_signature PASSED
tests/test_signature.py::test_missing_headers_are_rejected PASSED
tests/test_commands.py::test_today_lunch PASSED
tests/test_commands.py::test_spaces_are_ignored PASSED
tests/test_commands.py::test_this_week_schedule PASSED
tests/test_commands.py::test_help_command PASSED
tests/test_commands.py::test_other_words_get_help PASSED
tests/test_commands.py::test_plain_user_message PASSED
tests/test_commands.py::test_bot_message_is_ignored PASSED
tests/test_commands.py::test_edited_message_is_ignored PASSED
tests/test_commands.py::test_same_event_id_is_duplicate_the_second_time PASSED
============================= 15 passed in 0.36s ==============================
```

전체: `52 passed`

### 결과 2: 로컬 서버에 서명한 요청과 가짜 요청 보내기

실제 Signing Secret으로 서명했고, Secret 값은 출력하지 않았습니다. 이벤트 ID와 사용자·채널 값은 시험용 가짜 값입니다.

| 번호 | 보낸 요청 | 응답 |
| --- | --- | --- |
| 1 | 서명 헤더 없음 | `401 invalid signature` |
| 2 | 서명한 주소 확인 요청 | `200 signed-ok-123` (challenge 그대로) |
| 3 | 서명한 1:1 메시지 `내일급식` | `200 ok` |
| 4 | 3과 같은 이벤트를 재전송 번호 1로 | `200 ok` (처리는 건너뜀) |
| 5 | 봇 메시지(`bot_id` 있음) | `200 ok` (처리는 건너뜀) |
| 6 | `  이번 주   일정 ` | `200 ok` |
| 7 | `안녕 급식봇` | `200 ok` |
| 8 | 틀린 Secret으로 서명 | `401 invalid signature` |
| 9 | 서명은 맞지만 6분 전 시각 | `401 invalid signature` |
| 10 | 서명 뒤 본문을 바꿈 | `401 invalid signature` |

서버 화면:

```
INFO:     127.0.0.1:55100 - "POST /slack/events HTTP/1.1" 401 Unauthorized
INFO:     127.0.0.1:55101 - "POST /slack/events HTTP/1.1" 200 OK
[명령어] tomorrow_lunch | 보낸 글: 내일급식
INFO:     127.0.0.1:55102 - "POST /slack/events HTTP/1.1" 200 OK
INFO:     127.0.0.1:55103 - "POST /slack/events HTTP/1.1" 200 OK
INFO:     127.0.0.1:55104 - "POST /slack/events HTTP/1.1" 200 OK
[명령어] this_week_schedule | 보낸 글:   이번 주   일정 
INFO:     127.0.0.1:55105 - "POST /slack/events HTTP/1.1" 200 OK
[명령어] help | 보낸 글: 안녕 급식봇
INFO:     127.0.0.1:55106 - "POST /slack/events HTTP/1.1" 200 OK
INFO:     127.0.0.1:55108 - "POST /slack/events HTTP/1.1" 401 Unauthorized
INFO:     127.0.0.1:55109 - "POST /slack/events HTTP/1.1" 401 Unauthorized
INFO:     127.0.0.1:55110 - "POST /slack/events HTTP/1.1" 401 Unauthorized
```

로그(`logs/bot.log`):

```
[WARNING] 서명이 맞지 않는 요청을 거부했습니다.
[INFO] Slack Request URL 확인 요청을 받아 challenge를 돌려줬습니다.
[INFO] 명령어 해석: event_id=Ev-local-001, 명령어=tomorrow_lunch
[INFO] 이미 처리한 이벤트라 건너뜁니다: event_id=Ev-local-001, 재전송 번호=1
[INFO] 사람이 보낸 새 메시지가 아니라 건너뜁니다: event_id=Ev-local-002, subtype=None
[INFO] 명령어 해석: event_id=Ev-local-003, 명령어=this_week_schedule
[INFO] 명령어 해석: event_id=Ev-local-004, 명령어=help
[WARNING] 서명이 맞지 않는 요청을 거부했습니다.
[WARNING] 서명이 맞지 않는 요청을 거부했습니다.
[WARNING] 서명이 맞지 않는 요청을 거부했습니다.
```

### 실제 Slack 요청의 서명 확인

실제 Slack이 보낸 요청이 서명 검증을 통과하는지는 **8단계에서 함께 확인한다.** 8단계에서 봇이 답장하게 되면 개발자에게 메시지를 한 번 보내 달라고 하는 것으로 두 가지를 함께 확인할 수 있다. 개발자에게 부탁하는 횟수를 줄이기 위해서다.

---

## 5. 발생한 문제와 해결

없음.

---

## 6. 결정한 것과 이유

| 결정 | 다른 선택지 | 고른 이유 |
| --- | --- | --- |
| 서명 확인을 모든 처리보다 먼저, 주소 확인 요청에도 적용 | 이벤트에만 적용 | 공식 문서: url_verification도 "요청이 진짜인지 확인한 뒤" challenge로 응답하라. 가짜 요청에는 아무것도 하지 않는다. |
| 서명이 맞지 않으면 `401` | `403`, `400`, 아무 응답 없음 | 공식 문서에 정해진 번호가 없다. "인증되지 않음"이라는 뜻이 가장 가깝다. |
| 원래 본문(`await request.body()`)으로 계산하고, JSON은 `json.loads(body)`로 따로 만듦 | `await request.json()` 뒤 다시 직렬화 | 공식 문서: JSON으로 바꾸기 전의 원래 본문을 써야 한다. |
| 서명 함수가 Secret과 지금 시각을 매개변수로 받음 | 함수 안에서 `.env` 값과 `time.time()`을 직접 씀 | 테스트에서 공식 문서 예시 Secret과 예시 시각을 넣어 정답과 비교할 수 있다. |
| `hmac.compare_digest`로 비교 | `==` | 공식 문서가 hmac 비교 함수를 권한다. 비교 시간으로 서명을 알아내는 공격을 막는다. |
| 시각은 `isdigit()`로 먼저 확인한 뒤 `int()` | 바로 `int()` | 헤더는 가짜 요청이 마음대로 보낼 수 있다. 숫자가 아니면 `ValueError`로 서버 오류가 나지 않게 미리 거른다. |
| 사람 메시지는 `bot_id`도 `subtype`도 없는 `message`로 판단 | `user`가 있으면 사람 메시지 | 공식 문서: 요즘 앱의 메시지는 `bot_id`로 알 수 있다. 수정·삭제 등은 `subtype`이 붙는다. "subtype이 없으면 사람 메시지"라는 문장은 문서에 없어서, 이 프로젝트가 정한 기준이다. |
| 중복 확인은 메모리의 집합(`set`)으로 | 파일이나 데이터베이스에 저장 | Slack은 실패하면 바로, 1분 뒤, 5분 뒤에 다시 보낸다. 서버가 켜져 있는 동안만 기억해도 충분하다. 서버를 다시 켜면 비워지고, 오래 켜 두면 계속 쌓이는 한계는 있다. 연습 프로젝트 규모에서는 문제가 되지 않는다. |
| 중복이면 처리하지 않고 바로 `200` | `x-slack-no-retry: 1` 헤더를 붙인 다른 응답 | CLAUDE.md 규칙이 "응답을 바로 돌려주고 한 번만 처리"다. `x-slack-no-retry`는 200이 아닌 응답에서만 쓰는 헤더(공식 문서)라 맞지 않는다. |
| 명령어 표의 키를 띄어쓰기 없는 모양으로 | 띄어쓰기 있는 모양으로 적고 비교할 때 지우기 | 표와 찾는 값을 늘 같은 모양으로 맞추기 쉽다. |
| 로그에는 보낸 글 대신 명령어 이름만 | 보낸 글도 로그에 | 6단계와 같은 이유. 사용자가 무엇을 보낼지 모른다. |
| 서버를 `--reload`로 실행 | 코드를 고칠 때마다 직접 껐다 켜기 | 8단계에서 코드를 고치면 바로 반영된다. 개발할 때만 쓰는 옵션이다. |

---

## 7. 다음 단계에서 할 일 (8단계: 명령어 응답 → 양방향 완성)

1. 명령어별로 답장을 만든다.
   - `오늘 급식`, `내일 급식`: NEIS 조회 → 3단계 변환 → 같은 1:1 대화로 답장
   - `이번 주 일정`: NEIS 학사일정 API의 공식 명세를 확인해야 한다. 2단계에서 쓴 방법(포털 명세 데이터)으로 확인한다.
   - `도움말`: 사용 가능한 명령어 안내
2. 답장은 `chat.postMessage`로, 받은 이벤트의 `channel`(1:1 대화방)로 보낸다. 지금 권한(`chat:write`)으로 충분한지 확인한다.
3. **3초 규칙**: NEIS 조회와 전송은 3초를 넘길 수 있다. 응답을 먼저 돌려주고 답장은 그 뒤에 보내는 방법(FastAPI의 백그라운드 작업)을 쓴다.
4. 3단계에서 남긴 문구 문제를 정한다. `내일 급식`에 "오늘은 급식이 없습니다."는 어색하다.
5. **개발자 역할**: 터널이 켜져 있는지 확인하고, 봇에게 명령어를 보내 답장을 받아 본다. 이때 실제 Slack 요청의 서명 검증 통과도 함께 확인한다.

---

## 확인한 공식 문서

- 요청 서명 확인: https://docs.slack.dev/authentication/verifying-requests-from-slack/
- `message` 이벤트: https://docs.slack.dev/reference/events/message/
- `bot_message`: https://docs.slack.dev/reference/events/message/bot_message/
- `message_changed`: https://docs.slack.dev/reference/events/message/message_changed/
- Events API(재전송, `x-slack-no-retry`): https://docs.slack.dev/apis/events-api/

## 이번 단계 핵심 정리

1. 서버는 모든 요청의 서명을 가장 먼저 확인하고, 맞지 않으면 401로 거부하고 로그를 남긴다.
2. 서명 계산은 공식 문서 예시 값으로 테스트해 정답과 같은 것을 확인했다.
3. 5분 넘게 지난 요청은 서명이 맞아도 거부한다.
4. 같은 `event_id`는 한 번만 처리하고, 봇·수정 메시지는 명령어로 보지 않는다.
5. 명령어는 띄어쓰기를 모두 지운 뒤 표에서 찾고, 없으면 도움말로 본다.
