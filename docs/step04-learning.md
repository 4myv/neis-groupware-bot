# 4단계 학습 정리: 토큰, 파일, 그리고 메시지 보내기

## 이 문서를 다 읽으면 할 수 있게 되는 것

1. access token과 refresh token이 무엇이고, 왜 12시간마다 새로 받는지 설명할 수 있다.
2. 파일에 값을 저장하고 다시 읽는 코드(`with open`, `json.dump`, `json.load`)를 설명할 수 있다.
3. `requests.post`로 Slack에 메시지를 보내는 `app/sender.py`를 한 줄씩 설명할 수 있다.

## 읽기 전에

- 코드 예시는 모두 실제로 실행한 결과를 붙였습니다. 긴 파일 경로는 `예시.py`처럼 줄여 적었습니다.
- 토큰 같은 비밀값은 어디에도 적지 않았습니다. 예시의 `xoxb-wrong`, `예시-토큰`은 가짜 값입니다.
- 앞 단계에서 설명한 것은 "step01 참고"처럼 적었습니다.

---

## 1. 이번 단계에서 새로 나온 것

**개념**

1. 토큰: access token, refresh token, 토큰 자동 교체

**인터넷**

2. POST 요청과 `requests.post`: `data=`와 `json=`
3. HTTP 헤더와 `Authorization: Bearer`
4. Slack 응답 모양: `{"ok": ..., "error": ...}`

**Python 문법**

5. `pathlib`: 파일 경로 다루기 (`Path`, `__file__`, `/`)
6. `with open(...) as file`: 파일 쓰고 읽기
7. `json.dump`, `json.load`: 파일에 JSON 쓰고 읽기
8. `time.time()`: 지금 시각을 초로
9. `-> None`: 돌려주는 값이 없는 함수

**앞 단계에서 설명한 것**

- step01: `.env`, `os.getenv`, `if`/`else`
- step02: 함수, 딕셔너리, 키워드 인자, `requests.get`, `json.dumps`/`json.loads`, 메서드
- step03: `not`, f-문자열, `assert`, pytest

---

## 2. 하나씩 설명

### 2-1. 토큰: access token, refresh token, 토큰 자동 교체

**설명**

토큰은 "이 요청은 우리 봇이 보낸 것"을 증명하는 긴 글자입니다. Slack에 요청할 때마다 함께 보냅니다.

**access token**은 실제 요청에 쓰는 토큰입니다. 토큰 자동 교체를 켜면 **12시간(43,200초)마다 만료**됩니다.

**refresh token**은 새 access token을 받을 때만 쓰는 토큰입니다. **한 번 쓰면 버려지고**, 새 refresh token이 함께 옵니다. 그래서 받을 때마다 반드시 다시 저장해야 합니다.

**비유**

놀이공원 이용권과 같습니다.
access token은 하루짜리 입장권이고, refresh token은 "새 입장권으로 바꿔 주는 교환권"입니다.
교환권을 내면 새 입장권과 **새 교환권**을 줍니다. 새 교환권을 잃어버리면 다음 날 입장권을 받을 수 없습니다.

**이 프로젝트에서 한 일**

| 순서 | 한 일 | 쓴 Slack 기능 |
| --- | --- | --- |
| 1 | 처음 받은 `xoxb-` 토큰(만료 없음)을 "만료되는 토큰 + refresh token"으로 **한 번** 바꿈 | `oauth.v2.exchange` |
| 2 | 바꾼 토큰들을 `secrets/slack_tokens.json`에 저장 | |
| 3 | 메시지를 보낼 때마다 만료 시각을 확인하고, 5분 안에 만료되면 새로 받아 저장 | `oauth.v2.access` |

바꾼 뒤의 access token은 `xoxe.xoxb-`로, refresh token은 `xoxe-`로 시작합니다. (실제로 확인)

**Java 비교**

Spring Security OAuth2 Client의 `OAuth2AuthorizedClientManager`가 refresh token으로 access token을 자동으로 바꿔 주는 것과 같은 일입니다. 이 프로젝트는 그 과정을 직접 코드로 씁니다.

**자주 하는 실수: refresh token을 저장하지 않는다**

새로 받은 refresh token을 저장하지 않으면, 다음 재발급 때 쓸 교환권이 없습니다.
그래서 `get_access_token`은 재발급하자마자 `save_token_response`로 파일에 저장합니다. (3-2 참고)

---

### 2-2. POST 요청과 `requests.post`: `data=`와 `json=`

**설명**

POST 요청은 "이 내용을 받아서 처리해 주세요"라는 HTTP 요청입니다. (GET은 step02 참고)
보낼 내용은 주소 뒤가 아니라 요청의 **본문**(body)에 담습니다.

`requests.post`는 본문을 두 가지 모양으로 만들 수 있습니다.

- `data=딕셔너리`: `이름=값&이름=값` 모양(폼 모양)으로 보냅니다.
- `json=딕셔너리`: JSON 모양으로 보냅니다.

**작은 예시** (보내지 않고 본문 모양만 확인)

```python
import requests

form = requests.Request("POST", "https://slack.com/api/oauth.v2.access", data={"grant_type": "refresh_token", "client_id": "123"}).prepare()
print(form.headers["Content-Type"])
print(form.body)

as_json = requests.Request("POST", "https://slack.com/api/chat.postMessage", json={"channel": "C123", "text": "hello"}).prepare()
print(as_json.headers["Content-Type"])
print(as_json.body)
```

결과:

```
application/x-www-form-urlencoded
grant_type=refresh_token&client_id=123
application/json
b'{"channel": "C123", "text": "hello"}'
```

`requests.Request(...).prepare()`는 요청을 실제로 보내지 않고 "보낼 모양"만 만들어 보는 방법입니다. 이 예시에서만 씁니다.

**이 프로젝트 코드**

```python
response = requests.post(SLACK_API_URL + "oauth.v2.access", data={...}, ...)      # app/auth.py
response = requests.post(SLACK_POST_MESSAGE_URL, headers=headers, json=payload, ...)  # app/sender.py
```

Slack 공식 문서가 정한 모양을 따랐습니다.

- `oauth.v2.exchange`, `oauth.v2.access`: 폼 모양(`application/x-www-form-urlencoded`)
- `chat.postMessage`: JSON을 권장함

**Java 비교**

```java
MultiValueMap<String, String> form = new LinkedMultiValueMap<>();   // data=
restTemplate.postForObject(url, form, Map.class);
restTemplate.postForObject(url, payloadMap, Map.class);              // json= (Jackson이 JSON으로 바꿈)
```

**자주 하는 실수: API가 원하는 모양과 다르게 보낸다**

Slack 문서에는 `invalid_post_type`이라는 오류가 있습니다. "POST로 불렀지만 Content-Type이 맞지 않는다"는 뜻입니다.
API마다 받는 모양이 다르니, 공식 문서의 "Content types"를 먼저 확인해야 합니다.

---

### 2-3. HTTP 헤더와 `Authorization: Bearer`

**설명**

헤더는 요청에 붙이는 "부가 정보" 목록입니다. 이름과 값의 짝이라서 딕셔너리로 넘깁니다.

`Authorization` 헤더에는 누가 보냈는지 증명하는 값을 넣습니다.
Slack은 `"Bearer 토큰"` 모양을 받습니다. `Bearer`는 "이 토큰을 가진 사람"이라는 뜻의 약속된 단어이고, 뒤에 빈칸 하나가 있습니다.

Slack 공식 문서에 따르면 토큰은 반드시 헤더로 보내야 하고, JSON 본문이나 주소 뒤에 넣을 수 없습니다.

**작은 예시** (`auth.test`는 토큰이 맞는지 확인만 하는 Slack 기능입니다)

```python
import requests

no_token = requests.post("https://slack.com/api/auth.test", timeout=10)
print(no_token.status_code, no_token.json())

wrong = requests.post(
    "https://slack.com/api/auth.test",
    headers={"Authorization": "Bearer xoxb-wrong"},
    timeout=10,
)
print(wrong.status_code, wrong.json())
```

결과:

```
200 {'ok': False, 'error': 'not_authed'}
200 {'ok': False, 'error': 'invalid_auth'}
```

- `not_authed`: 토큰을 아예 보내지 않았다.
- `invalid_auth`: 보낸 토큰이 맞지 않는다.

**이 프로젝트 코드** (`app/sender.py`)

```python
headers = {
    "Authorization": f"Bearer {get_access_token()}",
    "Content-Type": "application/json; charset=utf-8",
}
```

`Content-Type` 헤더는 "본문이 어떤 모양인지"를 알려 줍니다. 한글 메시지가 깨지지 않도록 `charset=utf-8`(글자 저장 방식)을 함께 적었습니다.

**Java 비교**

```java
HttpHeaders headers = new HttpHeaders();
headers.setBearerAuth(accessToken);              // "Authorization: Bearer ..."
headers.setContentType(MediaType.APPLICATION_JSON);
```

**자주 하는 실수: `Bearer `를 빠뜨린다**

```python
import requests

response = requests.post(
    "https://slack.com/api/auth.test",
    headers={"Authorization": "xoxb-wrong"},
    timeout=10,
)
print(response.json())
```

결과:

```
{'ok': False, 'error': 'not_authed'}
```

토큰을 넣었는데도 "토큰이 없다"(`not_authed`)고 나옵니다. `Bearer ` 없이는 토큰으로 알아보지 못하기 때문입니다.

---

### 2-4. Slack 응답 모양: `{"ok": ..., "error": ...}`

**설명**

Slack Web API의 응답에는 항상 `ok`가 있습니다. `True`면 성공, `False`면 실패입니다.
실패하면 `error`에 짧은 오류 코드가 들어 있습니다.

**실제로 확인한 것:** 오류일 때도 HTTP 상태 코드는 `200`이었습니다. (2-3 예시) 그래서 `status_code`가 아니라 `ok`를 봐야 합니다.

**작은 예시** (없는 채널로 보내기 — 실제로 전송되지 않음)

```python
from app.sender import post_message

print(post_message("C0000000000", "이 메시지는 없는 채널로 가서 전송되지 않는다"))
```

결과:

```
{'ok': False, 'error': 'channel_not_found'}
```

**이 프로젝트 코드** (`send_lunch_message.py`)

```python
slack_response = post_message(SLACK_CHANNEL_ID, message)
if slack_response["ok"]:
    print("Slack으로 보냈습니다.")
else:
    print("Slack으로 보내지 못했습니다. 오류 코드:", slack_response["error"])
```

| 오류 코드 | 뜻 (Slack 공식 문서) |
| --- | --- |
| `not_authed` | 토큰을 보내지 않았다 |
| `invalid_auth` | 토큰이 맞지 않는다 |
| `token_expired` | 토큰이 만료되었다 |
| `channel_not_found` | 채널 값이 잘못되었다 |
| `not_in_channel` | 봇이 그 채널에 들어가 있지 않다 |
| `missing_scope` | 토큰에 필요한 권한이 없다 |

**Java 비교**

```java
Map<String, Object> body = restTemplate.postForObject(url, request, Map.class);
if (Boolean.TRUE.equals(body.get("ok"))) { ... }
```

Spring의 `RestTemplate`은 HTTP 상태가 4xx, 5xx일 때 예외를 던집니다. Slack은 실패해도 200이라서, Java로 만들어도 `ok`를 직접 확인해야 합니다.

**자주 하는 실수: 상태 코드 200이면 성공이라고 생각한다**

2-3 예시처럼 `200`인데도 `'ok': False`일 수 있습니다.

---

### 2-5. `pathlib`: 파일 경로 다루기

**설명**

`pathlib`은 파일 경로를 다루는 표준 라이브러리입니다. `Path(경로)`로 경로 객체를 만듭니다.

`경로.parent`는 그 경로를 담고 있는 **한 단계 위 폴더**입니다. (속성은 step03 참고)

경로 객체에 `/`와 이름을 쓰면 그 폴더 안의 경로가 됩니다. 나눗셈이 아니라 "폴더 안으로"라는 뜻입니다.

`__file__`은 Python이 자동으로 만들어 주는 변수입니다. **지금 실행 중인 코드 파일의 경로**가 들어 있습니다. `.resolve()`는 그 경로를 완전한 경로로 바꿉니다.

**작은 예시 1**

```python
from pathlib import Path

here = Path("C:/neis_groupware_bot/app/config.py")
print(here.parent)
print(here.parent.parent)
print(here.parent.parent / "secrets" / "slack_tokens.json")
```

결과:

```
C:\neis_groupware_bot\app
C:\neis_groupware_bot
C:\neis_groupware_bot\secrets\slack_tokens.json
```

`/`로 써도 Windows에 맞게 `\`로 바꿔 보여 줍니다.

**작은 예시 2**

```python
from pathlib import Path

print(__file__)
print(Path(__file__).resolve().parent)
```

결과 (예시 파일이 있던 폴더에서 실행):

```
C:\...\examples4\p02_file_var.py
C:\...\examples4
```

**이 프로젝트 코드** (`app/config.py`)

```python
PROJECT_ROOT: Path = Path(__file__).resolve().parent.parent
SLACK_TOKEN_FILE: Path = PROJECT_ROOT / "secrets" / "slack_tokens.json"
```

`config.py`는 `app` 폴더 안에 있습니다. 그래서 `.parent` 두 번이면 프로젝트 최상위 폴더입니다.
어느 폴더에서 실행하든 같은 토큰 파일을 찾을 수 있습니다.

`app/auth.py`, `setup_slack_token.py`에서는 경로 객체의 메서드 두 개를 씁니다.

- `경로.exists()`: 그 파일이 있으면 `True`
- `경로.mkdir(exist_ok=True)`: 폴더를 만든다. `exist_ok=True`는 "이미 있어도 오류 내지 마라"

**Java 비교**

```java
Path root = Paths.get(...).getParent().getParent();
Path tokenFile = root.resolve("secrets").resolve("slack_tokens.json");
Files.exists(tokenFile);
```

**자주 하는 실수: 경로를 문자열 `+`로 붙인다**

```python
root = "C:/neis_groupware_bot"
print(root + "secrets")
```

결과:

```
C:/neis_groupware_botsecrets
```

사이의 `/`를 빠뜨려 엉뚱한 경로가 되었습니다. `Path`와 `/`를 쓰면 이런 실수가 없습니다.

---

### 2-6. `with open(...) as file`: 파일 쓰고 읽기

**설명**

`open(파일경로, 모드, encoding="utf-8")`은 파일을 엽니다.

| 모드 | 뜻 |
| --- | --- |
| `"w"` | 쓰기. 파일이 없으면 만들고, 있으면 **내용을 지우고** 새로 쓴다 |
| `"r"` | 읽기 |

`with open(...) as file:` 아래 블록에서는 열린 파일을 `file`이라는 이름으로 씁니다.
**블록이 끝나면 파일이 자동으로 닫힙니다.** 닫는 것을 잊을 걱정이 없습니다.

`encoding="utf-8"`은 글자를 저장하는 방식입니다. 한글이 깨지지 않게 늘 적습니다.

**작은 예시** (2-7의 `json.dump`, `json.load`와 함께)

```python
import json

data = {"access_token": "예시-토큰", "expires_at": 1793900000.0}
with open("example_tokens.json", "w", encoding="utf-8") as file:
    json.dump(data, file, indent=2, ensure_ascii=False)

with open("example_tokens.json", "r", encoding="utf-8") as file:
    loaded = json.load(file)
print(loaded["expires_at"])
```

결과:

```
1793900000.0
```

**이 프로젝트 코드** (`app/auth.py`)

```python
with open(SLACK_TOKEN_FILE, "w", encoding="utf-8") as file:
    json.dump(tokens, file, indent=2)
```

```python
with open(SLACK_TOKEN_FILE, "r", encoding="utf-8") as file:
    return json.load(file)
```

두 번째 코드처럼 `with` 블록 안에서 `return`해도 파일은 닫힙니다.

**Java 비교**

```java
try (BufferedWriter writer = Files.newBufferedWriter(path, StandardCharsets.UTF_8)) {
    ...
}   // 블록이 끝나면 자동으로 close()
```

Java의 try-with-resources와 같은 역할입니다.

**자주 하는 실수: 없는 파일을 읽으려고 한다**

```python
with open("no_such_tokens.json", "r", encoding="utf-8") as file:
    print(file.read())
```

결과 (마지막 줄):

```
FileNotFoundError: [Errno 2] No such file or directory: 'no_such_tokens.json'
```

이 프로젝트에서는 `setup_slack_token.py`를 실행하기 전에 `send_lunch_message.py`를 실행하면 이런 오류가 납니다. 토큰 파일이 아직 없기 때문입니다.

---

### 2-7. `json.dump`, `json.load`: 파일에 JSON 쓰고 읽기

**설명**

step02의 `json.dumps`, `json.loads`는 **글자**와 Python 값을 서로 바꿨습니다.
이름 끝에 `s`(string)가 없는 `json.dump`, `json.load`는 **파일**에 바로 쓰고 읽습니다.

| 함수 | 하는 일 |
| --- | --- |
| `json.dumps(값)` | 값 → JSON 글자 (step02) |
| `json.loads(글자)` | JSON 글자 → 값 (step02) |
| `json.dump(값, 파일)` | 값 → 파일에 JSON으로 쓰기 |
| `json.load(파일)` | 파일의 JSON → 값 |

작은 예시와 프로젝트 코드는 2-6과 같습니다.

**토큰 파일의 모양** (값은 가림)

```json
{
  "access_token": "***",
  "refresh_token": "***",
  "expires_at": 1793900000.0
}
```

**Java 비교**

```java
mapper.writeValue(file, tokens);                  // json.dump
Map<String, Object> t = mapper.readValue(file, Map.class);   // json.load
```

**자주 하는 실수: `dump`와 `dumps`를 바꿔 쓴다**

`json.dumps(tokens, file)`처럼 쓰면 파일에 쓰지 않습니다. 끝의 `s`가 있으면 글자를 돌려주는 함수입니다.
"파일이면 `s` 없이"라고 기억하면 됩니다.

---

### 2-8. `time.time()`: 지금 시각을 초로

**설명**

`time.time()`은 지금 시각을 **1970년 1월 1일 0시(세계 표준시)부터 지난 초**로 돌려줍니다. 이런 시각 표현을 유닉스 시각이라고 합니다.
숫자 하나라서 더하고 빼고 비교하기 쉽습니다.

**작은 예시**

```python
import time

now = time.time()
print(now)
expires_at = now + 43200
print(expires_at - now)
```

결과 (실행한 순간의 값):

```
1793859853.9861226
43200.0
```

`>=`는 "왼쪽이 오른쪽보다 크거나 같으면 `True`"입니다.

```python
print(10 >= 10)
print(9 >= 10)
print(100000 - 300)
```

결과:

```
True
False
99700
```

**이 프로젝트 코드** (`app/auth.py`)

```python
"expires_at": time.time() + expires_in,                    # save_tokens: 만료되는 시각
...
return now >= expires_at - REFRESH_MARGIN_SECONDS          # needs_refresh
```

Slack은 "43200초 뒤에 만료"(`expires_in`)라고 알려 줍니다.
저장할 때 "지금 + 43200"으로 바꿔 두면, 나중에 지금 시각과 바로 비교할 수 있습니다.

`needs_refresh`는 "지금이 (만료 시각 − 300초) 이후인가"를 봅니다. 만료 5분 전부터 새 토큰을 받습니다.

**Java 비교**

```java
long now = Instant.now().getEpochSecond();
boolean needsRefresh = now >= expiresAt - 300;
```

**자주 하는 실수: 남은 시간(`expires_in`)을 그대로 저장한다**

`43200`만 저장하면, 나중에 파일을 읽었을 때 "언제부터 43200초인지" 알 수 없습니다. 그래서 만료되는 **시각**으로 바꿔 저장합니다.

---

### 2-9. `-> None`: 돌려주는 값이 없는 함수

**설명**

`-> None`은 "이 함수는 일만 하고 돌려주는 값이 없다"는 타입 힌트입니다.
이런 함수의 결과를 변수에 받으면 `None`이 들어갑니다. (`None`은 step01 참고)

**작은 예시**

```python
def say_hello(name: str) -> None:
    print("안녕,", name)


result = say_hello("급식봇")
print(result)
```

결과:

```
안녕, 급식봇
None
```

**이 프로젝트 코드**

```python
def save_tokens(access_token: str, refresh_token: str, expires_in: int) -> None:
def save_token_response(response_body: dict) -> None:
```

파일에 저장하는 일만 하고, 돌려줄 값은 없습니다.

**Java 비교**

Java의 `void` 메서드입니다.

```java
static void saveTokens(String accessToken, String refreshToken, int expiresIn) { ... }
```

**자주 하는 실수: `None`을 돌려주는 함수의 결과를 쓰려고 한다**

step03의 `append`처럼, 일만 하는 함수의 결과를 다시 변수에 넣으면 `None`만 남습니다.

---

## 3. 코드 줄 단위 해설

### 3-1. `app/config.py` (바뀐 부분)

```python
import os
from pathlib import Path
```

`pathlib`에서 `Path`를 가져옵니다. (2-5)

```python
# Slack 앱 정보. 토큰 교환과 재발급(app/auth.py), 메시지 전송(app/sender.py)에 쓴다.
SLACK_BOT_TOKEN: str = os.getenv("SLACK_BOT_TOKEN", "")
SLACK_CLIENT_ID: str = os.getenv("SLACK_CLIENT_ID", "")
SLACK_CLIENT_SECRET: str = os.getenv("SLACK_CLIENT_SECRET", "")
SLACK_CHANNEL_ID: str = os.getenv("SLACK_CHANNEL_ID", "")
```

1단계와 같은 방법으로 `.env`의 Slack 값 네 개를 읽습니다. (step01 3-2)

```python
PROJECT_ROOT: Path = Path(__file__).resolve().parent.parent
SLACK_TOKEN_FILE: Path = PROJECT_ROOT / "secrets" / "slack_tokens.json"
```

| 줄 | 설명 |
| --- | --- |
| 35 | 이 파일(`app/config.py`)에서 두 단계 위 폴더가 프로젝트 최상위입니다. (2-5) |
| 36 | 토큰 파일의 위치입니다. `secrets` 폴더는 `.gitignore`에 들어 있습니다. |

### 3-2. `app/auth.py` (새 파일)

**7~18줄: 가져오기와 상수**

```python
import json
import time

import requests

from app.config import SLACK_CLIENT_ID, SLACK_CLIENT_SECRET, SLACK_TOKEN_FILE

SLACK_API_URL: str = "https://slack.com/api/"
REQUEST_TIMEOUT_SECONDS: int = 10

# 만료되기 이만큼(초) 전에 미리 새 토큰을 받는다. 메시지를 보내는 도중에 만료되는 일을 막으려고 여유를 둔다.
REFRESH_MARGIN_SECONDS: int = 300
```

| 줄 | 설명 |
| --- | --- |
| 7~8 | 표준 라이브러리 `json`(2-7)과 `time`(2-8)을 가져옵니다. |
| 10 | 따로 설치한 `requests`를 가져옵니다. (step02) |
| 12 | 설정값 세 개를 가져옵니다. |
| 14 | Slack Web API 주소의 공통 앞부분입니다. 공식 문서: 모든 기능이 `https://slack.com/api/기능이름`에 있습니다. |
| 18 | 만료 300초(5분) 전부터 새 토큰을 받습니다. |

**21~31줄: `save_tokens` — 토큰을 파일에 저장**

```python
def save_tokens(access_token: str, refresh_token: str, expires_in: int) -> None:
    tokens = {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "expires_at": time.time() + expires_in,
    }
    SLACK_TOKEN_FILE.parent.mkdir(exist_ok=True)
    with open(SLACK_TOKEN_FILE, "w", encoding="utf-8") as file:
        json.dump(tokens, file, indent=2)
```

(주석 줄은 생략했습니다.)

| 코드 | 설명 |
| --- | --- |
| `-> None` | 저장만 하고 돌려주는 값은 없습니다. (2-9) |
| `tokens = {...}` | 저장할 세 값을 딕셔너리로 만듭니다. 남은 초(`expires_in`)를 만료 시각으로 바꿉니다. (2-8) |
| `mkdir(exist_ok=True)` | `secrets` 폴더가 없으면 만듭니다. (2-5) |
| `with open(..., "w", ...)` | 파일을 쓰기 모드로 엽니다. 예전 내용은 지워집니다. (2-6) |
| `json.dump(tokens, file, indent=2)` | 딕셔너리를 JSON으로 파일에 씁니다. (2-7) |

**34~39줄: `save_token_response` — Slack 응답에서 꺼내 저장**

```python
def save_token_response(response_body: dict) -> None:
    save_tokens(
        response_body["access_token"],
        response_body["refresh_token"],
        response_body["expires_in"],
    )
```

Slack 응답 딕셔너리에서 세 값을 꺼내 `save_tokens`에 넘깁니다. 교환할 때와 재발급할 때 응답 모양이 같아서 함께 씁니다.

**42~44줄: `load_tokens` — 파일에서 읽기**

```python
def load_tokens() -> dict:
    with open(SLACK_TOKEN_FILE, "r", encoding="utf-8") as file:
        return json.load(file)
```

파일을 읽기 모드로 열고, JSON을 딕셔너리로 바꿔 바로 돌려줍니다. (2-6, 2-7)

**47~48줄: `needs_refresh` — 새로 받을 때인가?**

```python
def needs_refresh(expires_at: float, now: float) -> bool:
    return now >= expires_at - REFRESH_MARGIN_SECONDS
```

| 코드 | 설명 |
| --- | --- |
| `-> bool` | `True` 또는 `False`를 돌려준다는 타입 힌트입니다. `bool`은 참/거짓 타입입니다. |
| `now >= expires_at - REFRESH_MARGIN_SECONDS` | 지금이 "만료 5분 전" 이후면 `True`입니다. (2-8) |

지금 시각을 함수 안에서 직접 구하지 않고 `now`로 넘겨받습니다. 그래야 테스트에서 원하는 시각을 넣어 확인할 수 있습니다. (`tests/test_auth.py`)

**51~63줄: `exchange_long_lived_token` — 처음 한 번 교환**

```python
def exchange_long_lived_token(long_lived_token: str) -> dict:
    response = requests.post(
        SLACK_API_URL + "oauth.v2.exchange",
        data={
            "client_id": SLACK_CLIENT_ID,
            "client_secret": SLACK_CLIENT_SECRET,
            "token": long_lived_token,
        },
        timeout=REQUEST_TIMEOUT_SECONDS,
    )
    return response.json()
```

Slack 공식 문서의 `oauth.v2.exchange`에 필요한 세 값(`client_id`, `client_secret`, `token`)을 폼 모양으로 보냅니다. (2-2) 응답 딕셔너리를 그대로 돌려줍니다.

**66~78줄: `refresh_access_token` — 새 토큰 받기**

```python
def refresh_access_token(refresh_token: str) -> dict:
    response = requests.post(
        SLACK_API_URL + "oauth.v2.access",
        data={
            "client_id": SLACK_CLIENT_ID,
            "client_secret": SLACK_CLIENT_SECRET,
            "grant_type": "refresh_token",
            "refresh_token": refresh_token,
        },
        timeout=REQUEST_TIMEOUT_SECONDS,
    )
    return response.json()
```

Slack 공식 문서 "Using token rotation"의 재발급 요청 그대로입니다. `grant_type`이 `"refresh_token"`이면 "refresh token으로 새 토큰을 달라"는 뜻입니다.

**81~89줄: `get_access_token` — 지금 쓸 토큰 주기**

```python
def get_access_token() -> str:
    tokens = load_tokens()
    if needs_refresh(tokens["expires_at"], time.time()):
        response_body = refresh_access_token(tokens["refresh_token"])
        save_token_response(response_body)
        return response_body["access_token"]
    return tokens["access_token"]
```

| 줄 | 설명 |
| --- | --- |
| `tokens = load_tokens()` | 파일에서 토큰들을 읽습니다. |
| `if needs_refresh(...)` | 만료 5분 전 이후인지 확인합니다. |
| `response_body = refresh_access_token(...)` | refresh token으로 새 토큰을 받습니다. |
| `save_token_response(response_body)` | 새 access token과 **새 refresh token**을 바로 저장합니다. (2-1) |
| `return response_body["access_token"]` | 새 access token을 돌려줍니다. |
| 마지막 `return` | 아직 여유가 있으면 파일의 토큰을 그대로 돌려줍니다. |

### 3-3. `app/sender.py` (새 파일)

```python
import requests

from app.auth import get_access_token

SLACK_POST_MESSAGE_URL: str = "https://slack.com/api/chat.postMessage"
REQUEST_TIMEOUT_SECONDS: int = 10


def post_message(channel_id: str, text: str) -> dict:
    headers = {
        "Authorization": f"Bearer {get_access_token()}",
        "Content-Type": "application/json; charset=utf-8",
    }
    payload = {
        "channel": channel_id,
        "text": text,
    }
    response = requests.post(
        SLACK_POST_MESSAGE_URL,
        headers=headers,
        json=payload,
        timeout=REQUEST_TIMEOUT_SECONDS,
    )
    return response.json()
```

(주석 줄은 생략했습니다.)

| 코드 | 설명 |
| --- | --- |
| `from app.auth import get_access_token` | 토큰은 `auth.py`가 관리합니다. `sender.py`는 받아서 쓰기만 합니다. |
| `SLACK_POST_MESSAGE_URL` | 메시지 보내기 주소입니다. (Slack 공식 문서 `chat.postMessage`) |
| `headers = {...}` | 토큰과 본문 모양을 알리는 헤더입니다. `get_access_token()`이 f-문자열 안에서 불립니다. (2-3) |
| `payload = {...}` | 보낼 내용입니다. Slack 문서의 필수 인자 `channel`과, 메시지 글자 `text`입니다. |
| `requests.post(..., json=payload, ...)` | 내용을 JSON 본문으로 보냅니다. (2-2) |
| `return response.json()` | `{"ok": True, ...}` 또는 `{"ok": False, "error": ...}`를 돌려줍니다. (2-4) |

### 3-4. `setup_slack_token.py` (새 파일, 처음 한 번만 실행)

```python
from app.auth import exchange_long_lived_token, save_token_response
from app.config import SLACK_BOT_TOKEN, SLACK_TOKEN_FILE

if SLACK_TOKEN_FILE.exists():
    print("토큰 파일이 이미 있어서 다시 바꾸지 않습니다:", SLACK_TOKEN_FILE)
else:
    # 교환은 되돌릴 수 없으므로, 저장할 폴더를 먼저 만들어 두고 교환을 요청한다.
    SLACK_TOKEN_FILE.parent.mkdir(exist_ok=True)
    response_body = exchange_long_lived_token(SLACK_BOT_TOKEN)
    if response_body["ok"]:
        save_token_response(response_body)
        print("토큰을 바꿔 저장했습니다:", SLACK_TOKEN_FILE)
        print("새 토큰은", response_body["expires_in"], "초 뒤에 만료됩니다. 그 전에 프로그램이 알아서 새로 발급받습니다.")
    else:
        print("토큰을 바꾸지 못했습니다. Slack 오류 코드:", response_body["error"])
```

| 부분 | 설명 |
| --- | --- |
| `if SLACK_TOKEN_FILE.exists():` | 이미 교환했으면 아무것도 하지 않습니다. Slack은 같은 토큰을 한 번만 바꿔 주기 때문입니다. |
| `mkdir(...)` | 교환 **전에** 폴더를 만듭니다. 교환에 성공했는데 저장할 곳이 없어 토큰을 잃는 일을 막으려는 것입니다. |
| `if response_body["ok"]:` | 성공하면 저장하고, 실패하면 Slack 오류 코드를 보여 줍니다. (2-4) |
| `if`/`else` 안에 또 `if`/`else` | 들여쓰기가 한 단계 더 깊어집니다. 같은 칸에 있는 `if`와 `else`가 짝입니다. |

### 3-5. `send_lunch_message.py` (새 파일)

```python
from app.config import NEIS_OFFICE_CODE, NEIS_SCHOOL_CODE, SLACK_CHANNEL_ID
from app.formatter import format_lunch_message
from app.neis import fetch_meals
from app.sender import post_message

meal_date = input("날짜를 YYYYMMDD 형식으로 입력하세요 (예: 20261105): ")
result = fetch_meals(NEIS_OFFICE_CODE, NEIS_SCHOOL_CODE, meal_date)
message = format_lunch_message(result, meal_date)
print(message)

slack_response = post_message(SLACK_CHANNEL_ID, message)
if slack_response["ok"]:
    print("Slack으로 보냈습니다.")
else:
    print("Slack으로 보내지 못했습니다. 오류 코드:", slack_response["error"])
```

2~4단계에서 만든 모듈을 차례로 씁니다. CLAUDE.md 구조도의 아래쪽 흐름 그대로입니다.

```
[NEIS 조회] neis.fetch_meals → [데이터 변환] formatter.format_lunch_message → [메시지 전송] sender.post_message
```

### 3-6. `tests/test_auth.py` (새 파일)

```python
EXPIRES_AT = 100000.0


def test_refresh_when_inside_margin():
    assert needs_refresh(EXPIRES_AT, EXPIRES_AT - REFRESH_MARGIN_SECONDS + 1)
```

`needs_refresh`에 "만료 시각"과 "지금 시각"을 직접 넣어 시험합니다.

| 테스트 | 지금 시각 | 기대 |
| --- | --- | --- |
| 시간이 넉넉함 | 만료 1시간 전 | `False` |
| 여유 시간 안 | 만료 299초 전 | `True` |
| 여유 시간 딱 맞음 | 만료 300초 전 | `True` |
| 이미 만료 | 만료 10초 후 | `True` |

Slack에 실제로 요청하는 함수는 테스트하지 않습니다. 테스트할 때마다 진짜 토큰을 쓰게 되기 때문입니다.

---

## 4. 사용한 라이브러리

| 라이브러리 | 종류 | 이번에 쓴 것 | 뜻 |
| --- | --- | --- | --- |
| requests | 따로 설치 | `requests.post(주소, data=..., json=..., headers=..., timeout=...)` | POST 요청을 보냅니다. (2-2, 2-3) |
| pathlib | 표준 라이브러리 | `Path`, `.parent`, `.resolve()`, `/`, `.exists()`, `.mkdir(exist_ok=True)` | 경로를 다룹니다. (2-5) |
| json | 표준 라이브러리 | `json.dump(값, 파일, indent=2)`, `json.load(파일)` | 파일에 JSON을 쓰고 읽습니다. (2-7) |
| time | 표준 라이브러리 | `time.time()` | 지금 시각(유닉스 시각, 초)입니다. (2-8) |
| (기본 기능) | 내장 함수 | `open(경로, "w" 또는 "r", encoding="utf-8")` | 파일을 엽니다. (2-6) |

**Slack Web API**

| 기능 | 주소 | 이번에 한 일 |
| --- | --- | --- |
| `oauth.v2.exchange` | `https://slack.com/api/oauth.v2.exchange` | `xoxb-` 토큰을 만료되는 토큰 + refresh token으로 한 번 바꿈 |
| `oauth.v2.access` | `https://slack.com/api/oauth.v2.access` | refresh token으로 새 토큰 받기 |
| `chat.postMessage` | `https://slack.com/api/chat.postMessage` | 채널에 메시지 보내기 |
| `auth.test` | `https://slack.com/api/auth.test` | 토큰이 맞는지 확인 (확인용, 프로젝트 코드에는 없음) |

---

## 5. 용어 정리

| 용어 | 쉬운 뜻 | 예시 |
| --- | --- | --- |
| 토큰 | 요청한 쪽이 누구인지 증명하는 긴 글자 | `xoxe.xoxb-...` |
| access token | 실제 요청에 쓰는 토큰. 12시간마다 만료 | `Authorization: Bearer ...` |
| refresh token | 새 access token을 받을 때만 쓰는 교환권. 한 번 쓰면 버려짐 | `xoxe-...` |
| 토큰 자동 교체 | access token이 주기적으로 만료되고 새로 발급되게 하는 Slack 설정 | token rotation |
| POST 요청 | 본문에 내용을 담아 "처리해 달라"고 보내는 HTTP 요청 | `requests.post` |
| 본문(body) | 요청에 담아 보내는 내용 | `{"channel": ..., "text": ...}` |
| 헤더 | 요청에 붙이는 부가 정보 | `Authorization`, `Content-Type` |
| Bearer | "이 토큰을 가진 쪽"이라는 뜻의 약속된 단어 | `Bearer 토큰` |
| 경로 객체 | 파일 위치를 다루는 `Path` 값 | `PROJECT_ROOT / "secrets"` |
| `__file__` | 지금 코드 파일의 경로가 든 자동 변수 | `Path(__file__)` |
| 파일 모드 | 파일을 어떻게 열지 정하는 글자 | `"w"`, `"r"` |
| 유닉스 시각 | 1970년 1월 1일부터 지난 초 | `1793859853.98` |
| `bool` | 참/거짓 타입 | `-> bool` |
| `-> None` | 돌려주는 값이 없는 함수라는 표시 | `save_tokens` |
| `FileNotFoundError` | 파일이 없다는 오류 | 토큰 파일 없이 전송 |

---

## 6. 확인 문제

### 문제 1. 코드 읽기: 이 코드의 출력은?

`REFRESH_MARGIN_SECONDS`는 300입니다.

```python
print(needs_refresh(10000.0, 9000.0))
print(needs_refresh(10000.0, 9800.0))
```

<details><summary>정답</summary>

```
False
True
```

- 첫 줄: `9000 >= 10000 - 300` → `9000 >= 9700` → `False`. 아직 1000초 남아서 새로 받지 않습니다.
- 둘째 줄: `9800 >= 9700` → `True`. 만료 200초 전이라 새로 받습니다.

</details>

### 문제 2. 빈칸 채우기

토큰 파일을 읽는 함수입니다. 빈칸을 채우세요.

```python
def load_tokens() -> dict:
    ____ open(SLACK_TOKEN_FILE, "__", encoding="utf-8") __ file:
        return json.____(file)
```

<details><summary>정답</summary>

```python
def load_tokens() -> dict:
    with open(SLACK_TOKEN_FILE, "r", encoding="utf-8") as file:
        return json.load(file)
```

- `with ... as file`: 블록이 끝나면 파일이 자동으로 닫힙니다. (2-6)
- `"r"`: 읽기 모드입니다. `"w"`로 쓰면 파일 내용이 지워집니다.
- `load`: 파일에서 읽으므로 `s`가 없는 `json.load`입니다. (2-7)

</details>

### 문제 3. 작은 수정: Slack이 `not_authed`를 돌려줍니다. 고치세요.

```python
headers = {
    "Authorization": get_access_token(),
    "Content-Type": "application/json; charset=utf-8",
}
```

<details><summary>정답</summary>

```python
headers = {
    "Authorization": f"Bearer {get_access_token()}",
    "Content-Type": "application/json; charset=utf-8",
}
```

Slack은 `Authorization` 헤더 값을 `Bearer 토큰` 모양으로 받습니다.
`Bearer `가 없으면 토큰을 넣어도 "토큰이 없다"(`not_authed`)고 답합니다. 실제로 확인한 결과입니다. (2-3)

</details>

---

## 이번 단계 핵심 정리

1. access token은 12시간마다 만료되고, refresh token(한 번 쓰면 버려짐)으로 새로 받는다. 새 refresh token은 반드시 저장한다.
2. 토큰은 `secrets/slack_tokens.json`에 `with open` + `json.dump`로 저장하고 `json.load`로 읽는다.
3. 경로는 `Path(__file__).resolve().parent`와 `/`로 만든다.
4. Slack에는 `requests.post`로 보내고, 토큰은 `Authorization: Bearer 토큰` 헤더에 넣는다.
5. Slack은 실패해도 HTTP 200을 주므로, 응답의 `ok`와 `error`를 확인한다.
