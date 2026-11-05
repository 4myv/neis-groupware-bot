# 6단계 개발 기록: 콜백 서버

## 이 문서를 다 읽으면 할 수 있게 되는 것

1. 콜백 서버와 터널을 켜고, Slack이 우리 서버로 메시지를 보내게 설정할 수 있다.
2. 터널 주소가 바뀌거나 끊겼을 때 다시 연결할 수 있다.
3. 6단계에서 실제로 겪은 문제 다섯 가지와 해결 방법을 알 수 있다.

---

## 1. 목표

- FastAPI로 콜백 엔드포인트를 만들고, Slack에서 받은 메시지를 출력한다.
- 터널 연결 방법을 안내한다. 터널 실행은 개발자의 역할이다.
- 서명 검증(7단계)과 답장(8단계)은 아직 하지 않는다.

---

## 2. 한 일 (순서대로)

1. **공식 문서 확인**
   - Slack: Events API, `url_verification`, `message.im`, App Home, 다시 설치와 토큰 자동 교체
   - 터널 도구: Cloudflare Quick Tunnel, ngrok
2. **터널 도구 고르기**
   - Cloudflare Quick Tunnel은 계정이 필요 없다(공식 문서). 그래서 가입 나이 조건에 걸리지 않는다.
   - ngrok은 공식 사이트에 접속되지 않아 나이 조건을 확인하지 못했다. 그래서 Cloudflare를 골랐다. (5번 문제 1)
3. **설치**: FastAPI 0.162.0, Uvicorn 0.54.0을 설치하고 `requirements.txt`에 적었다.
4. **서버 작성**: `app/server.py`를 만들었다.
   - `url_verification`에는 `challenge`를 그대로 돌려준다.
   - 이벤트는 출력하고 200을 돌려준다.
   - 자동 문서 주소(`/docs` 등)는 껐다.
5. **로컬 시험**
   - 서버를 백그라운드로 켰다.
   - Slack 공식 문서의 예시 요청과 같은 모양을 보냈다. (4번 결과 1)
6. **개발자 작업 1**
   - 터널을 켰다.
   - App Home의 Messages Tab을 켰다.
   - Event Subscriptions에서 Request URL을 등록하고(16:08 Verified), `message.im`을 구독했다.
7. **다시 설치 문제**
   - 권한(`im:history`)이 늘어 다시 설치해야 했는데, 앱 설정 화면에 다시 설치 버튼이 없었다.
   - 그사이 개발자가 "토큰 자동 교체가 꺼져 있다"고 알려 왔다. 확인해 보니 오해였다. (5번 문제 2, 3)
8. **`reinstall_slack_app.py` 작성**
   - Slack 공식 문서의 OAuth 설치 과정을 밟는 스크립트를 만들고, 테스트 4개를 추가했다.
   - 개발자가 실행해 다시 설치했다. 17:12에 새 토큰을 저장했고, 권한은 `chat:write,im:history`가 되었다.
9. **메시지 미도착 문제**
   - 개발자가 1:1 메시지를 보냈지만 서버에 오지 않았다.
   - 원인은 Cloudflare 쪽에서 터널이 지워진 것이었다. (5번 문제 4)
10. **개발자 작업 2**
    - 터널을 다시 켜고 새 주소를 등록했다.
    - 처음에는 `/slack/events`를 빠뜨려 확인에 실패했다. (5번 문제 5)
11. **성공**: 17:39:57에 1:1 메시지 "오늘 급식"이 `message.im` 이벤트로 서버에 도착했다. (4번 결과 2)
12. 학습 정리와 개발 기록을 쓰고, 비밀 파일이 커밋 대상에 없는지 확인한 뒤 커밋한다.

---

## 3. 바뀐 파일

| 파일 | 추가·수정 | 내용 |
| --- | --- | --- |
| `app/server.py` | 새 파일 | FastAPI 앱, `POST /slack/events` 엔드포인트 |
| `app/auth.py` | 수정 | 다시 설치용 상수 3개, `build_authorize_url`, `read_code_from_redirect`, `exchange_code` |
| `reinstall_slack_app.py` | 새 파일 | 권한을 바꾼 뒤 OAuth 과정으로 다시 설치하고 새 토큰을 저장 |
| `tests/test_auth.py` | 수정 | `read_code_from_redirect` 테스트 4개 추가 (전체 37개) |
| `requirements.txt` | 수정 | `fastapi==0.162.0`, `uvicorn==0.54.0` 추가 |
| `docs/step06-learning.md` | 새 파일 | 6단계 학습 정리 |
| `docs/step06-devlog.md` | 새 파일 | 이 문서 |

---

## 4. 실행 방법과 결과

### 개발자가 콜백을 다시 연결하는 순서 (터널을 켤 때마다)

터널 주소는 켤 때마다 바뀝니다. 그래서 아래를 매번 합니다.

1. **서버 켜기** (PowerShell 창 1, 가상환경 켜고)
   ```powershell
   python -m uvicorn app.server:app --port 8000
   ```
2. **터널 켜기** (PowerShell 창 2)
   ```powershell
   & "$HOME\Downloads\cloudflared-windows-amd64.exe" tunnel --url http://127.0.0.1:8000
   ```
   - `localhost` 대신 `127.0.0.1`을 씁니다. 서버가 `127.0.0.1`에서만 기다리기 때문입니다.
3. **Slack 앱 설정 → Event Subscriptions → Request URL → Change**
   - `https://(새 터널 주소).trycloudflare.com/slack/events`를 넣습니다. **`/slack/events`를 꼭 붙입니다.**
   - **Verified**가 뜨면 **Save Changes**를 누릅니다.
4. Slack에서 `lunch-bot`과의 **1:1 대화**(메시지 탭)에 메시지를 보냅니다.
5. 서버 창에 `[받은 이벤트] ...`가 찍히면 연결된 것입니다.

> 이번 단계에서는 에이전트가 서버(1번)를 백그라운드로 켜 두었습니다.

### 결과 1: 로컬 시험 (Slack 공식 문서의 예시 요청과 같은 모양)

```
[url_verification] status: 200 | content-type: text/plain; charset=utf-8 | body: 3eZbrw1aBm2rZgRNFdxV2595E9CY3gmdALWMmHkvFXO7tYXAYM8P
challenge echoed exactly: True
[event_callback] status: 200 | body: ok | seconds: 0.016
[event_callback retry 1] status: 200
GET /docs -> 404
GET /redoc -> 404
GET /openapi.json -> 404
GET / -> 404
```

이벤트 응답에 0.016초가 걸렸습니다. Slack의 제한 시간 3초보다 훨씬 짧습니다.

### 결과 2: 실제 Slack 이벤트 (ID는 가림)

서버 화면:

```
INFO:     107.22.137.94:0 - "POST /slack/events HTTP/1.1" 200 OK
[받은 이벤트] 종류: message | 채널 종류: im | 보낸 사람: U*** | 내용: 오늘 급식
INFO:     13.222.6.204:0 - "POST /slack/events HTTP/1.1" 200 OK
```

로그(`logs/bot.log`):

```
2026-11-05 17:39:36,369 [INFO] Slack Request URL 확인 요청을 받아 challenge를 돌려줬습니다.
2026-11-05 17:39:57,367 [INFO] Slack 이벤트 수신: event_id=Ev***, 종류=message, 채널 종류=im, 재전송 번호=
```

`재전송 번호`가 비어 있으니, Slack이 다시 보낸 것이 아니라 처음 보낸 이벤트입니다.

### 결과 3: 다시 설치 뒤 토큰 (값은 출력하지 않음)

```
token file modified: Thu Nov  5 17:12:18 2026
access starts with xoxe.: True | refresh starts with xoxe-: True
auth.test ok: True | x-oauth-scopes: chat:write,im:history
```

Slack API 응답 헤더 `x-oauth-scopes`로 토큰의 권한을 확인했습니다. 재발급하지 않고도 알 수 있습니다.

### 결과 4: 테스트

```
============================= 37 passed in 0.16s ==============================
```

---

## 5. 발생한 문제와 해결

### 문제 1. ngrok 공식 사이트에 접속되지 않아 나이 조건을 확인하지 못함

- **상황**: 개발자가 미성년자라서 터널 도구의 가입 나이 조건을 먼저 확인하려 했다. 그런데 `https://ngrok.com/tos`와 시작 안내 페이지 모두 "Socket is closed" 오류로 읽히지 않았다.
- **해결**
  - Cloudflare Quick Tunnel을 골랐다.
  - 공식 문서에 "You do not need a Cloudflare account or domain."이라고 되어 있다. 가입 절차가 없다.
  - Cloudflare 웹사이트 약관에도 나이 제한 문구는 없었다.

### 문제 2. 권한을 늘린 뒤 다시 설치하는 버튼이 없음

- **상황**
  - 공식 문서("Creating an app from app settings")는 왼쪽 메뉴 **Install App** → **Reinstall to Workspace**를 안내한다.
  - 그런데 개발자의 화면에는 Install App 메뉴가 없었다. OAuth & Permissions 화면에도 다시 설치 버튼이 없었다.
  - 화면 위 노란 안내에는 이렇게 적혀 있었다: "Please reinstall your app via the OAuth flow"(OAuth 과정으로 다시 설치하라).
- **원인**: Slack 화면이 공식 문서와 달라진 것으로 보인다. (1단계의 앱 만들기 화면과 같은 경우)
- **해결**
  - 공식 문서 "Installing with OAuth"의 과정을 그대로 밟는 `reinstall_slack_app.py`를 만들었다.
    1. 허락 화면 주소(`https://slack.com/oauth/v2/authorize`)에 Client ID, 권한, Redirect URL, `state`를 붙인다.
    2. 개발자가 Allow를 누르면 등록해 둔 `https://localhost/...`로 돌아오면서 일회용 `code`가 붙는다.
    3. 개발자가 그 주소를 스크립트에 붙여 넣으면, `state`를 확인하고 `oauth.v2.access`로 새 토큰을 받아 저장한다.
  - 결과: 17:12에 새 토큰을 저장했고 권한은 `chat:write,im:history`가 되었다.
  - 4단계에서 자리 채움용으로 등록한 Redirect URL이 여기서 실제로 쓰였다.

### 문제 3. "토큰 자동 교체가 꺼져 있다"는 오해

- **상황**: 개발자가 설정 화면을 보다가 "token rotation이 꺼져 있다"고 알려 왔다. 그런데 에이전트 쪽에서는 자동 교체 토큰이 정상으로 동작하고 있었다.
- **확인 과정**
  1. 저장된 토큰으로 정상 재발급을 한 번 해서 앱 ID를 확인했다. 개발자의 앱은 하나뿐이었다.
  2. 개발자가 OAuth & Permissions 화면을 캡처해 보여 줬다. (토큰 칸은 가림)
- **원인**
  - 개발자가 본 초록색 **Opt In** 버튼은 **PKCE**("Proof Key for Code Exchange") 기능의 버튼이었다. 토큰 자동 교체와는 다른 기능이다.
  - 같은 화면의 OAuth Tokens 부분에는 "**This app is using token rotation**"이라고 적혀 있었다. 표시된 토큰 만료 시각도 에이전트가 재발급한 토큰과 같았다.
- **해결**: PKCE 버튼은 누르지 않도록 안내했다. 자동 교체는 처음부터 켜져 있었다.

### 문제 4. 1:1 메시지가 서버에 도착하지 않음 (터널이 끊김)

- **상황**
  - 다시 설치 뒤 개발자가 봇에게 "오늘 급식"을 두 번 보냈지만 서버에 아무 요청도 오지 않았다.
  - 개발자의 캡처로 보면 Event Subscriptions 설정(Verified, `message.im` 구독)과 보낸 곳(봇과의 1:1 대화)은 맞았다.
- **원인 조사**
  - 에이전트가 터널 주소로 시험 요청을 보냈더니 `ConnectionError`가 났다.
  - 주소 확인(DNS) 결과는 `DNS name does not exist`였다. 그런데 cloudflared 프로그램은 16:05부터 계속 켜져 있었다.
  - 개발자가 확인한 터널 창 마지막 줄은 이것이었다.
    ```
    2026-11-05T08:32:17Z ERR Register tunnel error from server side error="Unauthorized: Tunnel not found"
    ```
  - Cloudflare 쪽에서 임시 터널이 지워졌고, 프로그램은 다시 연결하려다 거절당하고 있었다. 공식 문서에도 Quick Tunnel은 "no uptime guarantee"(계속 연결된다는 보장 없음)라고 되어 있다.
- **해결**
  - 터널을 끄고 다시 켜서 새 주소를 받았다. Event Subscriptions의 Request URL을 새 주소로 바꿨다.
  - 끊겨 있는 동안 보낸 메시지는 Slack이 세 번 다시 보내다(5분 안) 포기했을 것이므로 받지 못했다.

### 문제 5. 새 Request URL 확인 실패

- **에러** (Slack 화면): `Your URL didn't respond with the value of the challenge parameter.`
- **원인**
  - 서버 기록에 `POST / HTTP/1.1" 404 Not Found`가 여러 번 찍혀 있었다.
  - Request URL에 터널 주소만 넣고 `/slack/events`를 빠뜨려, Slack이 맨 앞 주소(`/`)로 보낸 것이다.
- **해결**: 주소 끝에 `/slack/events`를 붙였다. 17:39:36에 Verified가 됐고, 21초 뒤 메시지 이벤트가 도착했다. 4번의 "다시 연결하는 순서"에 `/slack/events`를 꼭 붙이라고 적었다.

---

## 6. 결정한 것과 이유

| 결정 | 다른 선택지 | 고른 이유 |
| --- | --- | --- |
| 명령어는 봇과의 **1:1 대화**(`message.im`)로 받음 | 채널 메시지 전체(`message.channels`), 봇 멘션(`app_mention`), 슬래시 명령(`/급식`) | CLAUDE.md의 "봇에 보낸 명령어"와 처음 계획한 네이버웍스의 1:1 봇 대화에 가장 가깝다. 채널의 모든 대화를 읽지 않아도 된다. |
| 터널은 Cloudflare Quick Tunnel | ngrok | 계정이 필요 없어 미성년 개발자도 쓸 수 있다. ngrok은 나이 조건을 확인하지 못했다. |
| 서버는 `127.0.0.1`에서만 기다림 (Uvicorn 기본값) | `0.0.0.0`(모든 주소) | 같은 와이파이의 다른 기기에서 직접 접속할 수 없다. 바깥에서는 터널로만 들어온다. |
| FastAPI 자동 문서(`/docs` 등) 끔 | 기본값 그대로 | 터널로 인터넷에 열리므로 필요 없는 주소를 열어 두지 않는다. |
| 로그에는 메시지 내용을 남기지 않음 (화면 출력에만) | 내용도 로그에 | 사용자가 무엇을 보낼지 모른다. 로그에는 문제를 찾는 데 필요한 이벤트 ID와 종류만 남긴다. |
| 6단계 서버는 출력만 하고 바로 200 응답 | 받자마자 답장까지 | CLAUDE.md 개발 단계 순서를 따랐다. 3초 규칙도 지킨다. |
| `async def` 사용 | 일반 `def` | 7단계 서명 검증에는 요청 본문의 원래 글자(`await request.body()`)가 필요하다. 지금부터 같은 모양으로 둔다. |
| 다시 설치를 `reinstall_slack_app.py`(OAuth 과정)로 | 개발자가 Slack 화면에서 찾기, 앱을 새로 만들기 | 화면에 버튼이 없었다. Slack 노란 안내와 공식 문서가 OAuth 과정을 안내한다. 앱을 새로 만들면 토큰·설정을 처음부터 다시 해야 한다. |
| 다시 설치 때 `state` 확인 | 생략 | 공식 문서: 다르면 위조로 보라. 짐작할 수 없는 값은 `secrets`로 만든다. |
| `exchange_code`는 Client ID·Secret을 폼 본문으로 보냄 | HTTP Basic 인증 | 공식 문서는 Basic 인증을 권하지만, 폼 본문 방식(공식 예시)도 지원한다. 4단계의 교환·재발급과 같은 방식으로 맞춰 초보자가 읽기 쉽게 했다. 둘 다 HTTPS로만 보낸다. |
| refresh token이 없는 응답은 저장하지 않음 | 받은 대로 저장 | 자동 교체 앱인데 refresh token이 없으면 이상한 응답이다. 지금 토큰 파일을 덮어쓰지 않아 지킨다. |
| `SLACK_BOT_SCOPES`를 `app/auth.py`에 상수로 둠 | `.env`에 | 비밀값이 아니고 코드가 필요로 하는 권한 목록이라 코드와 함께 관리한다. |

---

## 7. 다음 단계에서 할 일 (7단계: 서명 검증과 명령어 해석)

1. **서명 검증**: Slack 공식 문서("Verifying requests from Slack")대로 확인한다.
   - `X-Slack-Request-Timestamp`가 지금 시각과 5분 넘게 차이 나면 거부한다.
   - `v0:타임스탬프:요청 본문`을 Signing Secret으로 HMAC-SHA256 계산하고, 앞에 `v0=`을 붙인다.
   - `X-Slack-Signature`와 안전한 방법(`hmac.compare_digest`)으로 비교하고, 다르면 거부·로그를 남긴다.
2. **명령어 해석**: `오늘 급식`, `내일 급식`, `이번 주 일정`, 그 밖의 말은 `도움말`. 앞뒤 공백과 띄어쓰기 차이는 무시한다. (`내일급식` = `내일 급식`)
3. **봇 자신의 메시지 무시**: 8단계에서 봇이 답장하면 그 메시지도 이벤트로 올 수 있다. 무한 반복을 막도록 공식 문서의 `message` 이벤트 설명을 확인한다.
4. **콜백 중복 수신**: 같은 `event_id`는 한 번만 처리한다. (CLAUDE.md 예외 처리 표)

---

## 확인한 공식 문서

**Slack**

- Events API: https://docs.slack.dev/apis/events-api/
- `url_verification`: https://docs.slack.dev/reference/events/url_verification/
- `message.im`: https://docs.slack.dev/reference/events/message.im/
- App Home: https://docs.slack.dev/surfaces/app-home/
- OAuth 설치: https://docs.slack.dev/authentication/installing-with-oauth/
- `oauth.v2.access`: https://docs.slack.dev/reference/methods/oauth.v2.access/
- 다시 설치가 필요한 경우: https://docs.slack.dev/app-management/distribution/
- 토큰 자동 교체: https://docs.slack.dev/authentication/using-token-rotation/
- 요청 서명(7단계용): https://docs.slack.dev/authentication/verifying-requests-from-slack/

**Cloudflare**

- Quick Tunnels: https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/do-more-with-tunnels/trycloudflare/
- cloudflared 내려받기: https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/downloads/
- 웹사이트 이용약관: https://www.cloudflare.com/website-terms/

**ngrok** (접속 실패로 확인하지 못함)

- https://ngrok.com/tos

## 이번 단계 핵심 정리

1. `app/server.py`의 `POST /slack/events`가 Slack 이벤트를 받는다. 주소 확인에는 `challenge`, 이벤트에는 바로 200을 돌려준다.
2. Slack → Cloudflare 임시 주소 → `127.0.0.1:8000` 순서로 들어온다. 터널은 끊길 수 있고, 주소는 켤 때마다 바뀐다.
3. Request URL에는 반드시 `/slack/events`까지 넣고, Verified 뒤 Save Changes를 누른다.
4. 권한을 늘리면 `reinstall_slack_app.py`로 OAuth 과정을 밟아 다시 설치한다.
5. 실제 1:1 메시지 "오늘 급식"이 `message.im` 이벤트로 서버에 도착했다. 양방향의 절반(받기)이 연결되었다.
