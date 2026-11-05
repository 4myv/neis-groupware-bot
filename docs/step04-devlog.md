# 4단계 개발 기록: 메시지 전송 (단방향 완성)

## 이 문서를 다 읽으면 할 수 있게 되는 것

1. Slack 토큰이 어떻게 발급되고, 12시간마다 어떻게 새로 발급되는지 설명할 수 있다.
2. 내 학교 급식 메시지를 Slack 채널로 직접 보낼 수 있다.
3. 4단계에서 실제로 겪은 문제와, 토큰을 다룰 때 조심할 점을 알 수 있다.

---

## 1. 목표

- 토큰을 발급받아 봇으로 메시지를 보낸다. → **단방향 완성**
- CLAUDE.md의 "토큰 발급, 만료되면 새로 발급"을 Slack에 맞게 구현한다.
- 메신저를 바꿔도 전송 부분만 바꿀 수 있게, Slack 관련 코드는 `app/auth.py`와 `app/sender.py`에만 둔다.

---

## 2. 한 일 (순서대로)

1. **Slack 공식 문서 확인**: `chat.postMessage`, `auth.test`, Web API 기본, 토큰 자동 교체, `oauth.v2.exchange`, OAuth 설치 문서를 확인했다. (주소는 맨 아래)
2. **개발자 결정: 토큰 자동 교체 켜기**
   - Slack 봇 토큰(`xoxb-`)은 토큰 자동 교체를 켜지 않으면 만료되지 않는다.
   - CLAUDE.md의 "만료 시 재발급"을 실제로 구현하려고, 개발자가 자동 교체를 켜기로 했다. 한 번 켜면 끌 수 없다는 것을 알리고 결정받았다.
3. **개발자 작업**
   - 자동 교체를 켜려면 Redirect URL이 필요해서 `https://localhost/slack/oauth/callback`을 등록했다. (5번 문제 1)
   - 자동 교체를 켰다.
   - Client ID와 Client Secret을 `.env`에 넣었다.
   - 급식 알림 채널과 관리자 알림 채널(`lunch-bot-admin`, 새로 만듦)의 ID를 `.env`에 넣었다.
4. **준비 확인**: `.env` 값 6개가 있는지 확인했다(값은 출력하지 않음). 처음 토큰으로 `auth.test`가 `ok: True`인 것도 확인했다.
5. **코드 작성**: `app/config.py`(Slack 설정, 토큰 파일 경로), `app/auth.py`, `app/sender.py`, `setup_slack_token.py`, `send_lunch_message.py`, `tests/test_auth.py`를 작성했다.
6. **토큰 교환(한 번만)**
   - `setup_slack_token.py`로 `xoxb-` 토큰을 "12시간짜리 토큰 + refresh token"으로 바꿔 `secrets/slack_tokens.json`에 저장했다.
   - 다시 실행하면 교환을 거부하는 것도 확인했다.
7. **재발급 시험**
   - 12시간을 기다리지 않고 재발급을 한 번 강제로 실행했다. 새 토큰으로 `auth.test`가 성공하는 것을 확인했다.
   - 이 시험에서 이미 쓴 refresh token을 다시 쓰는 실수를 했다. 그래서 저장된 토큰이 괜찮은지 다시 확인했다. (5번 문제 2)
8. **메시지 전송**: 예시 학교(서울고등학교)의 11월 5일 중식을 급식 알림 채널로 보냈다. 성공했다.
9. **오류 응답 확인**: 토큰 없음, 틀린 토큰, `Bearer` 빠뜨림, 없는 채널일 때 Slack 응답을 확인했다. (4번)
10. 학습 정리와 개발 기록을 쓰고, 비밀 파일이 커밋 대상에 없는지 확인한 뒤 커밋한다.

---

## 3. 바뀐 파일

| 파일 | 추가·수정 | 내용 |
| --- | --- | --- |
| `app/config.py` | 수정 | Slack 설정 4개(`SLACK_BOT_TOKEN`, `SLACK_CLIENT_ID`, `SLACK_CLIENT_SECRET`, `SLACK_CHANNEL_ID`), `PROJECT_ROOT`, `SLACK_TOKEN_FILE` 추가 |
| `app/auth.py` | 새 파일 | 토큰 저장·읽기, 교환, 재발급, 재발급 시점 판단, 지금 쓸 토큰 주기 |
| `app/sender.py` | 새 파일 | `post_message`: Slack 채널로 메시지 보내기 |
| `setup_slack_token.py` | 새 파일 | 처음 한 번만 실행하는 토큰 교환 스크립트 |
| `send_lunch_message.py` | 새 파일 | `.env` 학교의 중식 메시지를 급식 알림 채널로 보내기 |
| `tests/test_auth.py` | 새 파일 | `needs_refresh` 테스트 4개 |
| `.env.example` | 수정 | `SLACK_CLIENT_ID`, `SLACK_CLIENT_SECRET`, `SLACK_CHANNEL_ID`, `SLACK_ADMIN_CHANNEL_ID` 추가, 설명 보강 |
| `docs/step04-learning.md` | 새 파일 | 4단계 학습 정리 |
| `docs/step04-devlog.md` | 새 파일 | 이 문서 |

**Git에 올라가지 않는 파일**

- `secrets/slack_tokens.json`: 토큰 파일입니다. `.gitignore`의 `secrets/` 규칙으로 제외되는 것을 `git check-ignore`로 확인했습니다.

---

## 4. 실행 방법과 결과

### 개발자가 따라 할 순서

```powershell
cd C:\neis_groupware_bot
.venv\Scripts\Activate.ps1
python -m pytest                 # 테스트 24개
python send_lunch_message.py     # 날짜를 넣으면 내 학교 중식이 급식 알림 채널로 갑니다
```

> `setup_slack_token.py`는 에이전트가 이미 한 번 실행했습니다. 다시 실행해도 "토큰 파일이 이미 있어서 다시 바꾸지 않습니다"만 나오고 아무 일도 하지 않습니다.
> `secrets/slack_tokens.json`은 지우지 마세요. 지우면 토큰을 다시 받기 위해 Slack 앱을 다시 설치해야 할 수 있습니다.

### 결과 1: 준비 확인 (값은 출력하지 않음)

```
SLACK_BOT_TOKEN filled: True | starts with xoxb-: True
SLACK_SIGNING_SECRET filled: True
SLACK_CLIENT_ID filled: True
SLACK_CLIENT_SECRET filled: True
SLACK_CHANNEL_ID filled: True | starts with C: True
SLACK_ADMIN_CHANNEL_ID filled: True | starts with C: True
two channel IDs differ: True
auth.test HTTP: 200 | ok: True | error: None | has bot_id: True
```

### 결과 2: 토큰 교환 (`setup_slack_token.py`)

```
토큰을 바꿔 저장했습니다: C:\neis_groupware_bot\secrets\slack_tokens.json
새 토큰은 43200 초 뒤에 만료됩니다. 그 전에 프로그램이 알아서 새로 발급받습니다.
```

두 번째 실행:

```
토큰 파일이 이미 있어서 다시 바꾸지 않습니다: C:\neis_groupware_bot\secrets\slack_tokens.json
```

### 결과 3: 토큰 파일과 재발급 시험 (값은 출력하지 않음)

```
file keys: ['access_token', 'expires_at', 'refresh_token']
access starts with xoxe.xoxb-: True
refresh starts with xoxe-: True
seconds until expiry: 43183
auth.test with exchanged token: (True, None)
refresh ok: True | error: None | token_type: bot | expires_in: 43200
new access differs from old: True
new refresh differs from old: True
auth.test with refreshed token: (True, None)
old refresh token reused (should fail): None
```

마지막 줄은 5번 문제 2에서 설명합니다. 그 뒤 저장된 토큰을 다시 확인한 결과입니다.

```
auth.test with currently saved access token: (True, None)
refresh with saved refresh token -> ok: True | error: None
saved new pair; auth.test: (True, None)
```

### 결과 4: 메시지 전송 (`send_lunch_message.py`, 예시 학교, `20261105`)

이 실행에서만 예시 학교 코드를 임시 환경 변수로 넣었습니다. Slack 값은 개발자의 `.env`를 그대로 썼습니다.

```
날짜를 YYYYMMDD 형식으로 입력하세요 (예: 20261105): [11월 5일(목) 중식]
흑미밥 / 부대찌개 / 호박볶음 / 오지치즈스틱 / 고등어구이 / 백김치
Slack으로 보냈습니다.
```

### 결과 5: Slack 오류 응답 (확인용)

| 상황 | HTTP 상태 | 응답 |
| --- | --- | --- |
| 토큰 없이 `auth.test` | 200 | `{'ok': False, 'error': 'not_authed'}` |
| 틀린 토큰(`Bearer xoxb-wrong`) | 200 | `{'ok': False, 'error': 'invalid_auth'}` |
| `Bearer ` 빠뜨림(`xoxb-wrong`만) | | `{'ok': False, 'error': 'not_authed'}` |
| 없는 채널(`C0000000000`)로 `post_message` | | `{'ok': False, 'error': 'channel_not_found'}` |

Slack은 오류일 때도 HTTP 200을 돌려줬습니다. 공식 문서에는 오류일 때의 HTTP 상태가 적혀 있지 않았고, 실제 응답으로 확인했습니다.

### 결과 6: 테스트 (`python -m pytest`)

```
collected 24 items

tests\test_auth.py ....                                                  [ 16%]
tests\test_formatter.py ....................                             [100%]

============================= 24 passed in 0.31s ==============================
```

---

## 5. 발생한 문제와 해결

### 문제 1. 토큰 자동 교체를 켜려면 Redirect URL이 필요함

- **상황**: 개발자가 자동 교체를 켜려고 하자, Slack 화면이 "최소 하나의 리디렉션 URL을 설정해야 한다"고 했다.
- **원인 조사**
  - Slack 공식 문서에서 이 조건을 찾지 못했다. "Using token rotation"에도, "Installing with OAuth"에도 없다.
  - 공식 문서에 따르면 Redirect URL은 앱 **설치 과정**에서 Slack이 임시 코드를 붙여 돌려보내는 주소다.
  - 그 임시 코드는 Client Secret과 **함께 있어야만** 토큰으로 바꿀 수 있다.
  - 이 프로젝트는 설치 과정을 쓰지 않고 토큰 교환(`oauth.v2.exchange`)을 쓴다. 그래서 Redirect URL로 들어오는 요청은 없다.
  - 주소 규칙은 https여야 하고 `#`이 없어야 한다는 것이다. `localhost`를 받아 주는지는 문서에 없었다.
- **해결**
  - 개발자와 상의해 `https://localhost/slack/oauth/callback`을 등록했다. 등록이 받아들여졌고, 자동 교체를 켰다.
  - 남의 사이트 주소(예: `example.com`) 대신 개발자 컴퓨터를 가리키는 주소를 골랐다. 혹시 설치 과정이 진행되더라도 임시 코드가 바깥으로 나가지 않게 하려는 것이다.

### 문제 2. 재발급 시험에서 이미 쓴 refresh token을 다시 씀

- **상황**
  - 재발급이 잘 되는지 시험하는 코드의 마지막 줄에서, 방금 쓴 옛 refresh token으로 한 번 더 재발급을 요청했다.
  - "버려진 토큰이라 실패할 것"이라고 예상했는데 **오류가 나지 않았다**. 결과 3의 마지막 줄 `None`은 오류 코드가 없다는 뜻이다.
  - 그 응답은 저장하지 않았다.
- **원인**
  - Slack 공식 문서에 따르면 옛 refresh token은 "짧은 유예 시간이 지난 뒤" 폐기된다. 유예 시간 안이라 받아 준 것으로 보인다.
  - 이것은 에이전트 시험 방식의 실수다. 저장하지 않을 재발급 요청을 보내서는 안 됐다. 그 바람에 저장된 refresh token이 무효가 되었을 위험이 있었다.
- **해결**
  - 저장된 토큰으로 정상 방법 그대로 재발급하고 결과를 저장했다. 성공했고, 새 토큰도 `auth.test`를 통과했다. (결과 3의 아래쪽)
  - 프로젝트 코드(`get_access_token`)는 재발급하면 **항상 바로 저장**한다. 옛 refresh token을 다시 쓰는 코드는 없다.

---

## 6. 결정한 것과 이유

| 결정 | 다른 선택지 | 고른 이유 |
| --- | --- | --- |
| 토큰 자동 교체 켜기 | 만료 없는 `xoxb-` 토큰 그대로 쓰기 | CLAUDE.md의 "토큰 발급, 만료 시 재발급"을 실제로 구현한다. 되돌릴 수 없다는 것을 알리고 **개발자가 정했다**. |
| Redirect URL로 `https://localhost/slack/oauth/callback` 등록 | 자동 교체 포기, `example.com` 같은 주소 | 쓰이지 않는 자리 채움용이다. 개발자 컴퓨터를 가리켜 가장 안전하다. **개발자가 정했다**. (5번 문제 1) |
| 처음 토큰은 `oauth.v2.exchange`로 교환 | 앱 다시 설치하기 | 공식 문서가 안내하는 방법이다. 개발자가 화면에서 할 일이 없다. |
| 바뀌는 토큰은 `secrets/slack_tokens.json`에 저장 | `.env`에 저장 | 프로그램이 12시간마다 스스로 고쳐 써야 하는 값이다. 사람이 적는 `.env`와 나눴다. `secrets/`는 `.gitignore`에 이미 있다. |
| `expires_in`(남은 초)을 `expires_at`(만료 시각)으로 바꿔 저장 | 받은 값 그대로 저장 | 파일을 나중에 읽어도 지금 시각과 바로 비교할 수 있다. |
| 만료 5분(300초) 전부터 재발급 | 만료된 뒤에 재발급 | 메시지를 보내는 도중에 만료되지 않게 한다. "만료된 뒤 다시 보내기"는 5단계 예외 처리에서 더한다. |
| `setup_slack_token.py`는 토큰 파일이 있으면 아무것도 하지 않음 | 매번 교환 시도 | Slack은 같은 토큰을 한 번만 바꿔 준다. 실수로 다시 실행해 파일을 덮어쓰는 일을 막는다. |
| 교환 전에 저장 폴더부터 만듦 | 저장할 때 만들기 | 교환은 되돌릴 수 없다. 저장 실패로 토큰을 잃을 가능성을 줄인다. |
| 토큰 관리(`auth.py`)와 전송(`sender.py`) 분리 | 한 파일에 모두 | 함수마다 한 가지 일만 한다. 메신저를 바꾸면 이 두 파일만 바꾼다. (CLAUDE.md 진행 규칙) |
| 메시지는 JSON 본문 + `Content-Type: application/json; charset=utf-8` | 폼 모양 | Slack 문서가 `chat.postMessage`에는 JSON을 강하게 권한다. 한글이 깨지지 않게 utf-8을 적었다. |
| 토큰 교환·재발급은 폼 모양(`data=`) | JSON | 공식 문서의 Content type이 `application/x-www-form-urlencoded`다. |
| 관리자 알림은 관리자 전용 채널(`lunch-bot-admin`)로 | 관리자에게 1:1 메시지 | 1:1 메시지는 앱 권한을 더 받고 다시 설치해야 할 수 있다. 채널이면 지금 권한(`chat:write`)으로 충분하다. 5단계에서 쓴다. |
| `SLACK_ADMIN_CHANNEL_ID`는 아직 `config.py`에서 읽지 않음 | 지금 읽기 | 5단계에서 처음 쓴다. 쓰지 않는 코드를 미리 넣지 않는다. `.env.example`에는 이름을 적어 두었다. |
| 시험 전송은 예시 학교 데이터로 | 개발자 학교 데이터 | 에이전트가 개발자의 학교 급식을 볼 필요가 없다. 개발자가 직접 보내 보면 된다. |
| Slack에 실제로 요청하는 함수는 단위 테스트하지 않음 | 가짜 응답으로 테스트 | 가짜 응답을 만드는 방법(모킹)은 새 개념이 많다. 시간 계산(`needs_refresh`)만 테스트하고, 실제 동작은 직접 실행해 확인했다. |

---

## 7. 다음 단계에서 할 일 (5단계: 예외 처리)

CLAUDE.md 예외 처리 표 중 남은 것들입니다.

1. **NEIS 응답 없음·오류**: 잠시 후 한 번 재시도한다. 그래도 실패하면 관리자 채널로 오류를 알린다.
   - 3단계에서 남긴 한계(오류가 "급식 없음"으로 보임)도 여기서 고친다.
2. **Access Token 만료**: 미리 재발급(4단계)을 해도 `token_expired`나 `invalid_auth`가 올 수 있다. 그러면 새 토큰을 발급받아 한 번 다시 보낸다.
3. **Slack 전송 실패**(`ok: False`): 관리자 채널로 오류를 알린다.
4. **로그**: 모든 요청과 오류를 시각과 함께 로그 파일(`logs/`)에 남긴다. 토큰과 인증키는 로그에 쓰지 않는다.
5. 서명이 맞지 않는 콜백과 콜백 중복 수신은 콜백 서버가 생기는 6~7단계에서 다룬다.

---

## 확인한 공식 문서

- Slack Web API 기본: https://docs.slack.dev/apis/web-api/
- `chat.postMessage`: https://docs.slack.dev/reference/methods/chat.postMessage/
- `auth.test`: https://docs.slack.dev/reference/methods/auth.test/
- 토큰 자동 교체: https://docs.slack.dev/authentication/using-token-rotation/
- `oauth.v2.exchange`: https://docs.slack.dev/reference/methods/oauth.v2.exchange/
- OAuth 설치와 Redirect URL: https://docs.slack.dev/authentication/installing-with-oauth/
- `chat:write` scope: https://docs.slack.dev/reference/scopes/chat.write/

## 이번 단계 핵심 정리

1. 토큰 자동 교체를 켜고, 처음 토큰을 한 번 교환해 `secrets/slack_tokens.json`에 저장했다.
2. `get_access_token`이 만료 5분 전부터 refresh token으로 새 토큰을 받아 바로 저장한다.
3. `post_message`가 `Authorization: Bearer` 헤더와 JSON 본문으로 Slack 채널에 메시지를 보낸다.
4. NEIS 조회 → 변환 → Slack 전송이 이어져 단방향 알림이 완성되었다.
5. Slack은 실패해도 HTTP 200을 주므로 `ok`와 `error`를 확인한다. 이 처리는 5단계에서 보강한다.
