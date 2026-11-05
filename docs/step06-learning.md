# 6단계 학습 정리: 콜백 서버 (FastAPI)

## 이 문서를 다 읽으면 할 수 있게 되는 것

1. 웹 서버, 엔드포인트, 포트, 터널이 무엇이고 서로 어떻게 이어지는지 설명할 수 있다.
2. FastAPI로 "이 주소로 요청이 오면 이 함수를 실행하라"는 코드를 읽고 설명할 수 있다.
3. Slack이 우리 서버로 메시지를 보내는 과정(주소 확인 → 이벤트 전달)을 순서대로 말할 수 있다.

## 읽기 전에

- 코드 예시는 모두 실제로 실행한 결과를 붙였습니다. 긴 파일 경로는 `예시.py`처럼 줄여 적었습니다.
- Slack 사용자 ID, 채널 ID, 터널 주소는 `U***`, `C***`, `○○○`처럼 가렸습니다.
- 앞 단계에서 설명한 것은 "step02 참고"처럼 적었습니다.

---

## 1. 이번 단계에서 새로 나온 것

**개념**

1. 웹 서버, 엔드포인트, 포트, `127.0.0.1`
2. 터널 (Cloudflare Quick Tunnel)
3. Slack Events API: 주소 확인과 이벤트 전달

**Python 문법과 라이브러리**

4. FastAPI 앱과 `@app.post` (데코레이터)
5. `async def`와 `await`
6. `Request`: 들어온 요청 읽기
7. `dict.get`: 없을 수도 있는 키 꺼내기
8. Uvicorn으로 서버 실행하기
9. 주소 만들고 나누기: `urlencode`, `urlparse`, `parse_qs`
10. `secrets`: 짐작할 수 없는 무작위 값

**앞 단계에서 설명한 것**

- step02: 딕셔너리, `requests`, HTTP·GET·POST·헤더(step04), 쿼리 문자열
- step03: `join`, `strip`
- step05: `logging`

---

## 2. 하나씩 설명

### 2-1. 웹 서버, 엔드포인트, 포트, `127.0.0.1`

**설명**

지금까지 우리 프로그램은 NEIS와 Slack에 **요청을 보내는 쪽**이었습니다. 이번에는 Slack이 보내는 요청을 **받는 쪽**, 즉 웹 서버를 만듭니다.

엔드포인트는 서버가 요청을 받는 **주소 하나**입니다. 우리 서버의 엔드포인트는 `/slack/events` 하나뿐입니다.

포트는 한 컴퓨터 안에서 프로그램을 구별하는 **번호**입니다. 우리 서버는 8000번 포트에서 기다립니다.

`127.0.0.1`은 "바로 이 컴퓨터"를 뜻하는 특별한 주소입니다. 이 주소에서 기다리는 서버는 같은 컴퓨터 안에서만 접속할 수 있습니다.

**비유**

건물(컴퓨터) 안의 호수(포트) 8000번 가게(서버)에 "Slack 이벤트 접수"라는 창구(엔드포인트)가 하나 있는 것입니다.

**이 프로젝트에서**

```
http://127.0.0.1:8000/slack/events
       └ 이 컴퓨터 └ 포트 └ 엔드포인트
```

**Java 비교**

Spring Boot가 내장 Tomcat으로 8080 포트에서 기다리고, `@PostMapping("/slack/events")`가 엔드포인트를 정하는 것과 같습니다.

**자주 하는 실수: 엔드포인트 주소를 빠뜨린다**

이번 단계에서 실제로 겪었습니다. Slack의 Request URL에 터널 주소만 넣고 `/slack/events`를 빠뜨렸더니, 서버 기록이 이렇게 나왔습니다.

```
INFO:     100.31.211.229:0 - "POST / HTTP/1.1" 404 Not Found
```

Slack이 `/`(맨 앞 주소)로 보냈는데 그런 창구가 없어서 404(없음)가 났습니다.

---

### 2-2. 터널 (Cloudflare Quick Tunnel)

**설명**

Slack은 인터넷 저쪽에 있습니다. 그런데 우리 서버는 `127.0.0.1`에서만 기다려서, 바깥에서는 접속할 수 없습니다.

터널은 인터넷에 **임시 주소**(`https://○○○.trycloudflare.com`)를 하나 만들어 줍니다. 그 주소로 온 요청을 우리 컴퓨터의 서버로 넘겨줍니다.

**비유**

건물 밖에 임시 우편함을 세우고, 거기 들어온 편지를 안쪽 창구까지 배달해 주는 사람입니다.

```
Slack ──▶ https://○○○.trycloudflare.com/slack/events ──(터널)──▶ http://127.0.0.1:8000/slack/events ──▶ 우리 서버
```

**이 프로젝트에서** (개발자가 실행)

```powershell
& "$HOME\Downloads\cloudflared-windows-amd64.exe" tunnel --url http://127.0.0.1:8000
```

Cloudflare 공식 문서에 따른 성질은 이렇습니다.

- 계정이 필요 없다.
- 실행할 때마다 주소가 바뀐다.
- 켜져 있는 동안은 주소를 아는 누구나 접속할 수 있다.
- 계속 연결된다는 보장이 없다.

**자주 하는 실수: 터널이 끊긴 줄 모른다**

이번 단계에서 실제로 겪었습니다. 프로그램은 켜져 있었지만, 터널 창에 이런 줄이 남아 있었습니다.

```
2026-11-05T08:32:17Z ERR Register tunnel error from server side error="Unauthorized: Tunnel not found"
```

Cloudflare 쪽에서 터널이 지워져 주소가 사라졌습니다. 이럴 때는 터널을 끄고 다시 켠 뒤, **새 주소를 Slack에 다시 등록**해야 합니다.

---

### 2-3. Slack Events API: 주소 확인과 이벤트 전달

**설명**

Slack은 우리 서버로 두 종류의 요청을 보냅니다. 둘 다 JSON 본문의 `type`으로 구별합니다.

| `type` | 언제 | 우리가 할 일 |
| --- | --- | --- |
| `url_verification` | Request URL을 등록할 때 한 번 | 받은 `challenge` 값을 **글자 그대로** 돌려준다 |
| `event_callback` | 봇에게 메시지가 오는 등 일이 생길 때마다 | 3초 안에 200(정상)으로 응답한다 |

Slack 공식 문서의 규칙은 이렇습니다.

- 3초 안에 응답하지 않으면 실패로 봅니다. 그러면 바로, 1분 뒤, 5분 뒤 이렇게 세 번 다시 보냅니다.
- 다시 보낼 때는 `x-slack-retry-num` 헤더에 몇 번째인지(1, 2, 3) 적습니다.

봇에게 온 1:1 메시지는 `event` 안에 이런 모양으로 옵니다. (실제로 받은 것, ID는 가림)

```
{"type": "message", "channel": "D***", "user": "U***", "text": "오늘 급식", "ts": "...", "channel_type": "im", ...}
```

`event`의 `type`은 `"message"`이고, 1:1 대화라는 것은 `channel_type`이 `"im"`인 것으로 압니다.

**Java 비교**

Slack이 우리 서버의 REST API를 호출하는 것입니다. Spring으로 만들면 `@PostMapping`으로 받은 `@RequestBody Map`의 `type`을 보고 분기하는 모양입니다.

**자주 하는 실수: 처리에 시간이 오래 걸린다**

이벤트를 받고 나서 오래 걸리는 일(NEIS 조회 등)을 다 끝낸 뒤 응답하면, 3초를 넘겨 Slack이 같은 이벤트를 또 보냅니다. 답장을 보내는 8단계에서 이 점을 다룹니다.

---

### 2-4. FastAPI 앱과 `@app.post` (데코레이터)

**설명**

FastAPI는 웹 서버 코드를 쉽게 쓰게 해 주는 외부 라이브러리입니다.

`app = FastAPI()`로 서버 앱 객체를 만듭니다.

함수 바로 위에 `@app.post("/주소")`를 쓰면, "이 주소로 **POST** 요청이 오면 아래 함수를 실행하라"고 등록됩니다.
이렇게 `@`로 시작해 함수에 기능을 덧붙이는 표시를 **데코레이터**라고 합니다.

**이 프로젝트 코드** (`app/server.py`)

```python
# 터널로 인터넷에 열리는 서버라서, FastAPI가 자동으로 만드는 문서 페이지(/docs 등)는 끈다.
app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)


@app.post("/slack/events")
async def receive_slack_event(request: Request) -> PlainTextResponse:
    ...
```

**실제로 확인한 동작**

| 요청 | 결과 |
| --- | --- |
| `POST /slack/events` | 200 OK (함수가 실행됨) |
| `GET /docs`, `GET /redoc`, `GET /openapi.json` | 404 (꺼 둔 자동 문서) |
| `GET /`, `POST /` | 404 (등록한 함수 없음) |

**Java 비교**

```java
@RestController
public class SlackController {
    @PostMapping("/slack/events")
    public String receiveSlackEvent(@RequestBody Map<String, Object> payload) { ... }
}
```

Java의 어노테이션 `@PostMapping`과 생김새와 하는 일이 거의 같습니다.

**자주 하는 실수: 자동 문서 페이지를 그대로 열어 둔다**

FastAPI는 기본으로 `/docs`에 API 설명 페이지를 만들어 줍니다. 혼자 쓸 때는 편합니다. 하지만 터널로 인터넷에 열면 아무나 볼 수 있으니, 필요 없으면 끕니다.

---

### 2-5. `async def`와 `await`

**설명**

`async def`로 만든 함수는 **기다려야 하는 일**(네트워크로 들어오는 본문 읽기 등)을 하는 동안 다른 요청도 처리할 수 있는 함수입니다.

그 안에서 기다려야 하는 일을 부를 때는 앞에 `await`를 붙입니다. "이 일이 끝날 때까지 기다렸다가 결과를 받아라"는 뜻입니다.

**작은 예시** (`asyncio`는 이런 함수를 실행하는 표준 라이브러리입니다)

```python
import asyncio


async def read_body() -> str:
    await asyncio.sleep(0.1)
    return "받은 내용"


async def handler() -> None:
    body = await read_body()
    print(body)


asyncio.run(handler())
```

결과:

```
받은 내용
```

**이 프로젝트 코드**

```python
async def receive_slack_event(request: Request) -> PlainTextResponse:
    payload = await request.json()
```

요청 본문은 네트워크로 조금씩 들어옵니다. 그래서 `request.json()` 앞에 `await`를 붙입니다.
FastAPI가 이 함수를 대신 실행해 주므로, 우리 코드에서 `asyncio.run`을 쓸 일은 없습니다.

**Java 비교**

Java의 `CompletableFuture`나 Spring WebFlux의 `Mono`처럼 "나중에 오는 결과"를 다루는 방식입니다. Python은 `async`/`await` 두 단어로 씁니다.

**자주 하는 실수: `await`를 빠뜨린다**

```python
async def handler() -> None:
    body = read_body()
    print(body)
```

결과:

```
<coroutine object read_body at 0x000001D63BBDA2A0>
RuntimeWarning: coroutine 'read_body' was never awaited
```

`await`가 없으면 결과가 아니라 "아직 실행되지 않은 일"(coroutine 객체)을 받습니다. 그래서 `request.json()`에 `await`를 빠뜨리면 딕셔너리를 받지 못합니다.

---

### 2-6. `Request`: 들어온 요청 읽기

**설명**

FastAPI 함수의 매개변수에 `request: Request` 타입 힌트를 붙이면, FastAPI가 들어온 요청 객체를 넣어 줍니다.

| 쓰는 법 | 꺼내는 것 |
| --- | --- |
| `await request.json()` | JSON 본문을 딕셔너리로 |
| `request.headers.get("이름", 기본값)` | 헤더 값. 헤더 이름은 대소문자를 가리지 않음 |

응답은 `PlainTextResponse("글자")`로 돌려줍니다. 글자를 그대로 보내는 응답이라, `challenge` 값을 따옴표 없이 정확히 돌려줄 수 있습니다.

**이 프로젝트 코드**

```python
if payload["type"] == "url_verification":
    logger.info("Slack Request URL 확인 요청을 받아 challenge를 돌려줬습니다.")
    return PlainTextResponse(payload["challenge"])

retry_number = request.headers.get("x-slack-retry-num", "")
```

**실제로 확인한 결과** (Slack 공식 문서의 예시 요청을 보냄)

```
[url_verification] status: 200 | content-type: text/plain; charset=utf-8 | body: 3eZbrw1aBm2rZgRNFdxV2595E9CY3gmdALWMmHkvFXO7tYXAYM8P
challenge echoed exactly: True
```

**Java 비교**

```java
@PostMapping("/slack/events")
public ResponseEntity<String> receive(@RequestBody Map<String, Object> payload,
                                      @RequestHeader(value = "X-Slack-Retry-Num", required = false) String retryNum) {
    return ResponseEntity.ok((String) payload.get("challenge"));
}
```

**자주 하는 실수: 서버 파일을 바로 실행한다** (2-8 참고)

---

### 2-7. `dict.get`: 없을 수도 있는 키 꺼내기

**설명**

`딕셔너리.get(키)`는 키가 있으면 값을, **없으면 오류 대신 `None`**을 돌려줍니다.
`딕셔너리.get(키, 기본값)`처럼 두 번째 값을 주면, 없을 때 그 값을 돌려줍니다.

**작은 예시**

```python
event = {"type": "message", "text": "오늘 급식"}
print(event.get("text"))
print(event.get("user"))
print(event.get("user", "알 수 없음"))
```

결과:

```
오늘 급식
None
알 수 없음
```

**이 프로젝트 코드**

```python
print(
    "[받은 이벤트]",
    "종류:", event.get("type"),
    "| 채널 종류:", event.get("channel_type"),
    "| 보낸 사람:", event.get("user"),
    "| 내용:", event.get("text"),
)
```

이벤트 종류마다 들어 있는 항목이 다릅니다. 그래서 없을 수도 있는 항목은 `get`으로 꺼냅니다.
괄호 안에서는 이렇게 여러 줄로 나눠 써도 하나의 `print`입니다.

**Java 비교**

Java `Map.get(key)`는 없으면 `null`이고, `getOrDefault(key, 기본값)`이 `get(키, 기본값)`과 같습니다.
그러니 Python의 `딕셔너리[키]`보다 `딕셔너리.get(키)`가 Java의 `map.get(key)`에 더 가깝습니다.

**자주 하는 실수: 없을 수도 있는 키를 `[]`로 꺼낸다**

```python
event = {"type": "message", "text": "오늘 급식"}
print(event["user"])
```

결과 (마지막 줄):

```
KeyError: 'user'
```

반대로 **반드시 있어야 하는 키**(`payload["type"]`)는 `[]`로 꺼냅니다. 없으면 이상한 요청이니 바로 알아채는 편이 낫기 때문입니다.

---

### 2-8. Uvicorn으로 서버 실행하기

**설명**

FastAPI로 쓴 코드는 혼자 실행되지 않습니다. **Uvicorn**이라는 서버 프로그램이 FastAPI 앱을 실행해 요청을 받아 줍니다.

```powershell
python -m uvicorn app.server:app --port 8000
```

| 부분 | 뜻 |
| --- | --- |
| `python -m uvicorn` | 가상환경에 설치된 uvicorn을 실행 (`python -m pip`과 같은 방식) |
| `app.server` | `app` 패키지의 `server` 모듈 (`app/server.py`) |
| `:app` | 그 모듈 안의 `app` 변수 (`app = FastAPI(...)`) |
| `--port 8000` | 8000번 포트에서 기다림 |

주소(`--host`)를 정하지 않으면 Uvicorn은 `127.0.0.1`에서 기다립니다. (실행 화면: `Uvicorn running on http://127.0.0.1:8000`)

끌 때는 그 창에서 `Ctrl + C`를 누릅니다.

**실제 실행 화면**

```
INFO:     Started server process [11632]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     107.22.137.94:0 - "POST /slack/events HTTP/1.1" 200 OK
[받은 이벤트] 종류: message | 채널 종류: im | 보낸 사람: U*** | 내용: 오늘 급식
```

**Java 비교**

Spring Boot는 `main` 메서드를 실행하면 내장 Tomcat이 함께 켜집니다. Python은 서버 프로그램(Uvicorn)과 앱 코드(FastAPI)가 나뉘어 있습니다.

**자주 하는 실수: 서버 파일을 바로 실행한다**

```powershell
python app\server.py
```

결과:

```
Traceback (most recent call last):
  File "C:\neis_groupware_bot\app\server.py", line 13, in <module>
    from app.log import logger
ModuleNotFoundError: No module named 'app'
```

파일을 바로 실행하면 Python이 `app` 폴더 안에서 모듈을 찾기 시작해서 `app` 패키지를 찾지 못합니다. (step01 패키지 참고)
설령 실행되더라도, 앱 객체를 만들기만 하고 요청을 기다리지는 않습니다. 서버는 늘 Uvicorn으로 실행합니다.

---

### 2-9. 주소 만들고 나누기: `urlencode`, `urlparse`, `parse_qs`

**설명**

이번 단계에서는 Slack 앱을 다시 설치하는 스크립트(`reinstall_slack_app.py`)를 만들었습니다. 이때 주소를 만들고 나누는 표준 라이브러리 `urllib.parse`를 씁니다.

- `urlencode(딕셔너리)`: 딕셔너리를 쿼리 문자열(`이름=값&이름=값`)로 만들고, 특수 문자는 퍼센트 인코딩합니다. (step02의 `requests`가 `params=`로 해 주던 일)
- `urlparse(주소)`: 주소를 부분으로 나눕니다. `.query`는 `?` 뒤의 쿼리 문자열입니다.
- `parse_qs(쿼리 문자열)`: 쿼리 문자열을 딕셔너리로 바꿉니다. **값은 늘 리스트**입니다.

**작은 예시 1**

```python
from urllib.parse import urlencode

params = {"scope": "chat:write,im:history", "redirect_uri": "https://localhost/slack/oauth/callback"}
print(urlencode(params))
```

결과:

```
scope=chat%3Awrite%2Cim%3Ahistory&redirect_uri=https%3A%2F%2Flocalhost%2Fslack%2Foauth%2Fcallback
```

**작은 예시 2** (`code`, `state`는 가짜 값)

```python
from urllib.parse import parse_qs, urlparse

url = "https://localhost/slack/oauth/callback?code=fake-123&state=abc"
parts = urlparse(url)
print(parts.query)
query = parse_qs(parts.query)
print(query)
print(query["code"][0])
```

결과:

```
code=fake-123&state=abc
{'code': ['fake-123'], 'state': ['abc']}
fake-123
```

**이 프로젝트 코드** (`app/auth.py`)

```python
def build_authorize_url(state: str) -> str:
    params = {
        "client_id": SLACK_CLIENT_ID,
        "scope": ",".join(SLACK_BOT_SCOPES),
        "redirect_uri": SLACK_REDIRECT_URI,
        "state": state,
    }
    return SLACK_AUTHORIZE_URL + "?" + urlencode(params)


def read_code_from_redirect(redirected_url: str, expected_state: str) -> str:
    query = parse_qs(urlparse(redirected_url.strip()).query)
    if query.get("state") != [expected_state]:
        return ""
    if "code" not in query:
        return ""
    return query["code"][0]
```

- Slack 공식 문서에 따라 권한 목록은 쉼표로 이어 붙입니다. (step03 `join`)
- `parse_qs`의 값이 리스트라서, `state`도 리스트 `[expected_state]`와 비교합니다.

**Java 비교**

```java
UriComponentsBuilder.fromHttpUrl(SLACK_AUTHORIZE_URL).queryParam("client_id", clientId) ... .toUriString();
UriComponentsBuilder.fromUriString(redirectedUrl).build().getQueryParams().getFirst("code");
```

**자주 하는 실수: `parse_qs`의 값이 문자열이라고 생각한다**

위 예시 2처럼 `query["code"]`는 `'fake-123'`이 아니라 `['fake-123']`(리스트)입니다. 글자를 쓰려면 `[0]`으로 첫 칸을 꺼내야 합니다.

---

### 2-10. `secrets`: 짐작할 수 없는 무작위 값

**설명**

`secrets.token_urlsafe(16)`은 남이 짐작할 수 없는 무작위 글자를 만듭니다. 주소에 넣어도 안전한 글자만 씁니다.

**작은 예시**

```python
import secrets

print(secrets.token_urlsafe(16))
print(secrets.token_urlsafe(16))
```

결과 (실행할 때마다 다름):

```
5ktsSjEAV-0NPxm1brBtaQ
sKlyW1Z5MF7lvjiXysEaVw
```

**이 프로젝트 코드** (`reinstall_slack_app.py`)

```python
# 이번 설치에서만 쓰는 무작위 값. 돌아온 주소의 state와 같아야 우리가 시작한 설치로 믿는다.
state = secrets.token_urlsafe(16)
```

허락 화면 주소에 이 값을 넣어 보내고, 돌아온 주소의 `state`와 비교합니다.
Slack 공식 문서에 따르면 값이 다르면 위조로 봐야 합니다. 남이 미리 만든 주소를 붙여 넣게 하는 속임수를 막습니다.

**Java 비교**

```java
SecureRandom random = new SecureRandom();
```

Java의 `SecureRandom`이 Python의 `secrets`입니다.

**자주 하는 실수: 보안용 값을 `random`으로 만든다**

Python의 `random` 모듈은 게임이나 시뮬레이션용이라 짐작될 수 있습니다. 비밀번호, 토큰, `state`처럼 보안에 쓰는 값은 `secrets`로 만듭니다.

---

## 3. 코드 줄 단위 해설

### 3-1. `app/server.py` (새 파일)

| 줄 | 코드 | 설명 |
| --- | --- | --- |
| 10~11 | `from fastapi import ...` | FastAPI 앱, 요청 객체, 글자 응답을 가져옵니다. |
| 13 | `from app.log import logger` | 5단계 로그를 씁니다. |
| 16 | `app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)` | 서버 앱을 만듭니다. 자동 문서 주소 세 개를 끕니다. (2-4) |
| 19 | `@app.post("/slack/events")` | 아래 함수를 `/slack/events`의 POST 창구로 등록합니다. (2-4) |
| 20 | `async def receive_slack_event(request: Request) -> PlainTextResponse:` | 요청 객체를 받아 글자 응답을 돌려주는 함수입니다. (2-5, 2-6) |
| 21 | `payload = await request.json()` | JSON 본문을 딕셔너리로 읽습니다. |
| 25~27 | `if payload["type"] == "url_verification": ...` | 주소 확인 요청이면 `challenge`를 그대로 돌려주고 끝냅니다. (2-3) |
| 30 | `retry_number = request.headers.get("x-slack-retry-num", "")` | Slack이 다시 보낸 것이면 몇 번째인지 꺼냅니다. 처음이면 빈 문자열입니다. |
| 32~46 | `if payload["type"] == "event_callback": ...` | 이벤트면 화면에 종류·채널 종류·보낸 사람·내용을 출력합니다. 로그에는 내용 없이 이벤트 정보만 남깁니다. (2-7) |
| 49 | `return PlainTextResponse("ok")` | 받았다는 뜻으로 바로 200을 돌려줍니다. 3초 규칙을 지키려고 다른 일은 하지 않습니다. |

로그에 메시지 **내용**을 남기지 않는 이유가 있습니다. 사용자가 무엇을 보낼지 모르니, 로그에는 문제를 찾는 데 필요한 정보(이벤트 ID, 종류)만 남깁니다.

### 3-2. `app/auth.py` (바뀐 부분)

| 줄 | 코드 | 설명 |
| --- | --- | --- |
| 9 | `from urllib.parse import parse_qs, urlencode, urlparse` | 주소 만들기·나누기 도구입니다. (2-9) |
| 23 | `SLACK_AUTHORIZE_URL` | Slack 허락 화면 주소입니다. (Slack 공식 문서) |
| 25 | `SLACK_REDIRECT_URI` | 4단계에서 등록한 Redirect URL입니다. |
| 28 | `SLACK_BOT_SCOPES: list[str] = ["chat:write", "im:history"]` | 이 앱이 쓰는 봇 권한 전체입니다. 권한을 늘리면 여기도 고칩니다. |
| 96~105 | `build_authorize_url` | 허락 화면 주소를 만듭니다. (2-9) |
| 108~116 | `read_code_from_redirect` | 돌아온 주소에서 `state`를 확인하고 `code`를 꺼냅니다. (2-9, 2-10) |
| 119~132 | `exchange_code` | `code`를 `oauth.v2.access`로 보내 새 토큰을 받습니다. Slack 공식 문서에 따라 허락 화면에 넣은 것과 같은 `redirect_uri`를 함께 보냅니다. |

### 3-3. `reinstall_slack_app.py` (새 파일)

| 부분 | 설명 |
| --- | --- |
| `state = secrets.token_urlsafe(16)` | 이번 설치에서만 쓰는 무작위 값입니다. (2-10) |
| `print(build_authorize_url(state))` | 브라우저에서 열 허락 화면 주소를 보여 줍니다. |
| `input(...)` | 개발자가 Allow를 누른 뒤 이동한 주소를 붙여 넣습니다. |
| `code = read_code_from_redirect(...)` | `state`가 같을 때만 `code`를 꺼냅니다. |
| `if response_body["ok"] and "refresh_token" in response_body:` | 성공했고 refresh token도 왔을 때만 저장합니다. refresh token이 없는 응답으로 토큰 파일을 덮어쓰지 않게 지킵니다. |

### 3-4. 테스트 (`tests/test_auth.py`에 4개 추가)

| 테스트 | 확인하는 것 |
| --- | --- |
| `test_read_code_when_state_matches` | `state`가 같으면 `code`를 꺼낸다 |
| `test_read_code_ignores_spaces_around_pasted_url` | 붙여 넣은 주소 앞뒤 빈칸·줄바꿈은 무시한다 |
| `test_no_code_when_state_differs` | `state`가 다르면 빈 문자열 (위조로 봄) |
| `test_no_code_when_user_did_not_allow` | Allow를 누르지 않아 `code`가 없으면 빈 문자열 |

---

## 4. 사용한 라이브러리

| 라이브러리 | 종류 | 이번에 쓴 것 | 뜻 |
| --- | --- | --- | --- |
| FastAPI 0.162.0 | 따로 설치 | `FastAPI(docs_url=None, ...)`, `@app.post(주소)`, `Request`, `PlainTextResponse` | 웹 서버 코드를 씁니다. |
| Uvicorn 0.54.0 | 따로 설치 | `python -m uvicorn app.server:app --port 8000` | FastAPI 앱을 실행해 요청을 받습니다. |
| urllib.parse | 표준 | `urlencode`, `urlparse`, `parse_qs` | 주소를 만들고 나눕니다. |
| secrets | 표준 | `token_urlsafe(16)` | 보안용 무작위 값을 만듭니다. |
| (딕셔너리 메서드) | 기본 기능 | `get(키, 기본값)` | 없을 수도 있는 키를 꺼냅니다. |
| cloudflared | 프로그램 (개발자가 실행) | `tunnel --url http://127.0.0.1:8000` | 임시 인터넷 주소를 우리 서버로 연결합니다. |

---

## 5. 용어 정리

| 용어 | 쉬운 뜻 | 예시 |
| --- | --- | --- |
| 웹 서버 | 요청을 받아 응답을 돌려주는 프로그램 | 우리 콜백 서버 |
| 콜백 | 일이 생기면 상대가 우리 쪽 주소로 알려 주는 방식 | Slack → `/slack/events` |
| 엔드포인트 | 서버가 요청을 받는 주소 하나 | `/slack/events` |
| 포트 | 한 컴퓨터 안에서 프로그램을 구별하는 번호 | 8000 |
| `127.0.0.1` | "이 컴퓨터"를 뜻하는 주소 | `http://127.0.0.1:8000` |
| 터널 | 인터넷 임시 주소를 내 컴퓨터 서버로 이어 주는 것 | `https://○○○.trycloudflare.com` |
| 이벤트 | Slack에서 일어난 일을 알리는 데이터 | 1:1 메시지(`message.im`) |
| 데코레이터 | 함수 위 `@...`로 기능을 덧붙이는 표시 | `@app.post(...)` |
| `async`/`await` | 기다리는 동안 다른 일도 할 수 있게 하는 문법 | `await request.json()` |
| coroutine | `async` 함수를 부르면 생기는 "아직 실행 안 된 일" | `await` 빠뜨렸을 때 |
| 404 | "그런 주소 없음" 상태 코드 | `POST /` |
| OAuth | 사용자가 허락하면 앱이 토큰을 받는 약속된 과정 | 다시 설치 |
| `state` | 허락 과정이 우리가 시작한 것인지 확인하는 무작위 값 | `secrets.token_urlsafe(16)` |
| 일회용 code | 허락 뒤 받는 10분짜리 값. 토큰으로 바꿀 때 쓴다 | `?code=...` |

---

## 6. 확인 문제

### 문제 1. 코드 읽기: 아래 요청이 오면 서버는 무엇을 돌려줄까요?

```json
{"type": "url_verification", "challenge": "abc123", "token": "xxx"}
```

<details><summary>정답</summary>

`200` 상태 코드와 글자 `abc123`을 돌려줍니다.

`payload["type"]`이 `"url_verification"`이라서 첫 번째 `if`에 들어갑니다. `PlainTextResponse(payload["challenge"])`가 `challenge` 값을 그대로 돌려줍니다. 그 아래 코드는 실행되지 않습니다.

`token` 값은 쓰지 않습니다. Slack 공식 문서도 이 값은 무시해도 된다고 합니다.

</details>

### 문제 2. 빈칸 채우기

```python
@app.____("/slack/events")
_____ def receive_slack_event(request: Request) -> PlainTextResponse:
    payload = _____ request.json()
```

<details><summary>정답</summary>

```python
@app.post("/slack/events")
async def receive_slack_event(request: Request) -> PlainTextResponse:
    payload = await request.json()
```

- `post`: Slack은 POST로 보냅니다.
- `async`: 안에서 `await`를 쓰려면 `async def`여야 합니다.
- `await`: 본문을 다 받을 때까지 기다렸다가 딕셔너리를 받습니다. 빠뜨리면 coroutine 객체가 옵니다. (2-5)

</details>

### 문제 3. 작은 수정: Slack이 "Your URL didn't respond with the value of the challenge parameter."라고 합니다. 서버 기록은 아래와 같습니다. 무엇을 고쳐야 할까요?

```
INFO:     100.31.211.229:0 - "POST / HTTP/1.1" 404 Not Found
```

<details><summary>정답</summary>

Slack 앱 설정의 Request URL 끝에 `/slack/events`를 붙입니다.

```
https://○○○.trycloudflare.com/slack/events
```

기록에 `POST /`가 찍혔으므로, Slack은 맨 앞 주소로 보냈습니다. 우리 서버의 창구는 `/slack/events`뿐이라 404가 났고, `challenge`를 돌려주지 못했습니다. 이번 단계에서 실제로 겪은 일입니다.

</details>

---

## 이번 단계 핵심 정리

1. Slack → 터널 주소 → `127.0.0.1:8000/slack/events` → 우리 함수 순서로 메시지가 들어온다.
2. `@app.post("/slack/events")`로 창구를 만들고, `async def` 안에서 `await request.json()`으로 본문을 읽는다.
3. 주소 확인(`url_verification`)에는 `challenge`를 그대로, 이벤트에는 3초 안에 200으로 응답한다.
4. 서버는 `python -m uvicorn app.server:app --port 8000`으로 켜고, 터널 주소가 바뀌면 Slack에 다시 등록한다.
5. 권한을 늘리면 `reinstall_slack_app.py`로 다시 설치한다. `state`로 위조를 막는다.
