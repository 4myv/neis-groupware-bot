# 6단계 실습 과제: 웹 서버(FastAPI), `dict.get`, 주소 다루기

## 이 문서를 다 풀면 할 수 있게 되는 것

1. 없을 수도 있는 키를 `dict.get`으로 안전하게 꺼낼 수 있다.
2. FastAPI로 작은 서버를 만들고, 다른 창에서 요청을 보내 응답을 확인할 수 있다.
3. 404(주소 없음)와 405(방법이 틀림)가 왜 나는지 설명할 수 있다.

## 시작하기 전에

- 함께 볼 문서: [`step06-learning.md`](step06-learning.md)
- 실습 파일은 `practice\step06\` 폴더에 만듭니다. (`New-Item -ItemType Directory -Force practice\step06`)
- 가상환경을 켜고 프로젝트 맨 위 폴더에서 실행합니다.
- **실습 서버는 8001번 포트**를 씁니다. 8000번은 `main.py`(급식 봇)가 쓰고 있을 수 있기 때문입니다.
- 과제 4~6은 PowerShell 창이 **두 개** 필요합니다. 창 1에서 서버를 켜 두고, 창 2에서 요청을 보냅니다. 두 창 모두 가상환경을 켭니다.
- 결과는 모두 실제로 실행해 확인했습니다. 서버 화면의 `127.0.0.1:60163` 같은 뒤 번호는 매번 다릅니다.

---

## 과제 1. 없을 수도 있는 키 꺼내기 (★)

**다지는 개념**: `dict.get`(2-7)

**할 일**

`practice\step06\p1_dict_get.py`를 만들고, 아래 `payload`에서 값을 꺼내 출력합니다.

```python
payload = {"type": "event_callback", "event": {"type": "message", "text": "오늘 급식"}}
```

1. `type`
2. `challenge` (없는 키, 기본값 없이)
3. `challenge` (없는 키, 기본값 `"없음"`)
4. `event`를 꺼내(없으면 빈 딕셔너리 `{}`) 그 안의 `text` (없으면 `""`)
5. `event` 안의 `bot_id` (없으면 `"사람이 보낸 메시지"`)

**확인 방법**

```
event_callback
None
없음
오늘 급식
사람이 보낸 메시지
```

<details><summary>정답 예시</summary>

```python
# dict.get 연습: 없을 수도 있는 키 꺼내기
payload = {"type": "event_callback", "event": {"type": "message", "text": "오늘 급식"}}

print(payload.get("type"))
print(payload.get("challenge"))
print(payload.get("challenge", "없음"))

event = payload.get("event", {})
print(event.get("text", ""))
print(event.get("bot_id", "사람이 보낸 메시지"))
```

- `payload["challenge"]`로 꺼냈다면 `KeyError`가 났을 것입니다. (step02 실습 과제 2)
- 밖에서 들어오는 요청은 어떤 키가 올지 모르므로, `app/server.py`는 `.get`을 많이 씁니다.

</details>

---

## 과제 2. 주소를 만들고 다시 나누기 (★)

**다지는 개념**: `urlencode`, `urlparse`, `parse_qs`(2-9)

**할 일**

`practice\step06\p2_url.py`를 만듭니다.

1. `{"school": "서울고등학교", "date": "20261105"}`를 `urlencode`로 주소 뒤에 붙일 글자로 만들어 출력합니다.
2. `"https://example.com/meal?"` 뒤에 붙여 주소를 만들고, `urlparse`로 나눕니다.
3. 나눈 결과의 `path`(경로)를 출력합니다.
4. `query`(물음표 뒤)를 `parse_qs`로 딕셔너리로 바꿔 출력합니다.
5. 그 딕셔너리에서 학교 이름 **글자만** 꺼내 출력합니다.

**확인 방법**

```
school=%EC%84%9C%EC%9A%B8%EA%B3%A0%EB%93%B1%ED%95%99%EA%B5%90&date=20261105
/meal
{'school': ['서울고등학교'], 'date': ['20261105']}
서울고등학교
```

- 첫 줄: 주소에는 한글을 그대로 쓸 수 없어서 `%EC%84...` 모양으로 바뀝니다.
- 셋째 줄: `parse_qs`는 값을 **리스트**로 돌려줍니다. 같은 이름이 여러 번 올 수 있기 때문입니다. 그래서 `[0]`으로 꺼냅니다.

<details><summary>정답 예시</summary>

```python
# 주소 만들고 나누기: urlencode, urlparse, parse_qs
from urllib.parse import parse_qs, urlencode, urlparse

query = urlencode({"school": "서울고등학교", "date": "20261105"})
print(query)

url = "https://example.com/meal?" + query
parts = urlparse(url)
print(parts.path)
print(parse_qs(parts.query))
print(parse_qs(parts.query)["school"][0])
```

`reinstall_slack_app.py`가 Slack 허락 화면 주소를 만들고(`urlencode`), 돌아온 주소에서 `code`를 꺼낼 때(`parse_qs`) 같은 방법을 씁니다.

</details>

---

## 과제 3. 짐작할 수 없는 값 만들기 (★)

**다지는 개념**: `secrets`(2-10)

**할 일**

`practice\step06\p3_secrets.py`를 만듭니다.

1. `secrets.token_urlsafe(16)`으로 무작위 글자를 두 번 만들어 각각 출력합니다.
2. 두 값이 같은지 출력합니다.
3. 두세 번 실행해 봅니다.

**확인 방법** (앞 두 줄은 실행할 때마다 다릅니다)

```
SHkj2pw--erot-GgV1LmUg
lCxkRBGnlXy5DI2CTPzSSQ
False
```

<details><summary>정답 예시</summary>

```python
# secrets 연습: 짐작할 수 없는 무작위 값
import secrets

first = secrets.token_urlsafe(16)
second = secrets.token_urlsafe(16)
print(first)
print(second)
print(first == second)
```

- `reinstall_slack_app.py`는 이 값을 `state`로 씁니다. 허락 화면에서 돌아온 요청이 **우리가 시작한 요청**인지 확인하려는 것입니다. 남이 짐작할 수 없어야 하므로 `secrets`를 씁니다.

</details>

---

## 과제 4. 내 첫 FastAPI 서버 (★★)

**다지는 개념**: FastAPI와 `@app.post`(2-4), `async def`와 `await`(2-5), `Request`(2-6), Uvicorn(2-8)

**할 일**

1. `practice\step06\mini_server.py`를 만듭니다.
   - FastAPI 앱 `app`을 만듭니다.
   - `POST /echo` 창구를 만듭니다. 요청 본문(JSON)을 딕셔너리로 읽고, `text` 값을 꺼냅니다(없으면 `""`).
   - 서버 화면에 `[받은 글]`과 그 글을 출력합니다.
   - `받은 글: (글)`을 글자 응답(`PlainTextResponse`)으로 돌려줍니다.
2. **창 1**에서 서버를 켭니다.
   ```powershell
   python -m uvicorn practice.step06.mini_server:app --port 8001
   ```
3. `practice\step06\p4_client.py`를 만들어 **창 2**에서 실행합니다.
   - `http://127.0.0.1:8001/echo`에 `json={"text": "오늘 급식"}`으로 POST
   - `json={}`(빈 본문)으로 한 번 더 POST
   - 각각 상태 코드와 응답 글자를 출력합니다. (`timeout=5`)

**확인 방법**

창 2:

```
200 받은 글: 오늘 급식
200 받은 글: 
```

창 1:

```
[받은 글] 오늘 급식
INFO:     127.0.0.1:60163 - "POST /echo HTTP/1.1" 200 OK
[받은 글] 
INFO:     127.0.0.1:60164 - "POST /echo HTTP/1.1" 200 OK
```

서버를 끌 때는 창 1에서 Ctrl+C를 누릅니다.

<details><summary>정답 예시</summary>

`practice\step06\mini_server.py`:

```python
# 실습용 작은 서버. 실행: python -m uvicorn practice.step06.mini_server:app --port 8001
from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse

app = FastAPI()


@app.post("/echo")
async def echo(request: Request) -> PlainTextResponse:
    payload = await request.json()
    text = payload.get("text", "")
    print("[받은 글]", text)
    return PlainTextResponse("받은 글: " + text)
```

`practice\step06\p4_client.py`:

```python
# 실습용 서버에 요청 보내기 (서버를 먼저 켜 둔다)
import requests

BASE_URL = "http://127.0.0.1:8001"

response = requests.post(BASE_URL + "/echo", json={"text": "오늘 급식"}, timeout=5)
print(response.status_code, response.text)

response = requests.post(BASE_URL + "/echo", json={}, timeout=5)
print(response.status_code, response.text)
```

- 4단계에서는 우리가 Slack에 요청을 **보냈습니다.** 이번에는 우리가 요청을 **받는 쪽**입니다. 6단계의 Slack 이벤트 수신과 같은 방향입니다.
- `await`를 빠뜨리면 `payload`가 딕셔너리가 아니라서 `.get`에서 오류가 납니다. (step06 확인 문제 2)

</details>

---

## 과제 5. Slack의 주소 확인 요청 흉내 내기 (★★★)

**다지는 개념**: Slack Events API의 주소 확인(2-3), `dict.get`(2-7)

**할 일**

1. `mini_server.py`에 `POST /slack-like` 창구를 더합니다.
   - 본문의 `type`이 `"url_verification"`이면 `challenge` 값을 **그대로** 글자로 돌려줍니다.
   - 아니면 `ok`를 돌려줍니다.
2. 코드를 고쳤으니 창 1에서 Ctrl+C로 끄고 다시 켭니다.
3. `practice\step06\p5_client.py`를 만들어 창 2에서 실행합니다.
   - `{"type": "url_verification", "challenge": "practice-123"}`
   - `{"type": "event_callback", "event": {"type": "message"}}`

**확인 방법**

```
200 practice-123
200 ok
```

Slack이 Request URL을 등록할 때 보내는 요청과 같은 모양입니다. 첫 응답처럼 `challenge`를 그대로 돌려주면 Slack 화면에 **Verified**가 뜹니다.

<details><summary>정답 예시</summary>

`mini_server.py`에 더할 부분:

```python
@app.post("/slack-like")
async def slack_like(request: Request) -> PlainTextResponse:
    payload = await request.json()
    if payload.get("type") == "url_verification":
        return PlainTextResponse(payload.get("challenge", ""))
    return PlainTextResponse("ok")
```

`p5_client.py`:

```python
import requests

BASE_URL = "http://127.0.0.1:8001"

response = requests.post(BASE_URL + "/slack-like", json={"type": "url_verification", "challenge": "practice-123"}, timeout=5)
print(response.status_code, response.text)

response = requests.post(BASE_URL + "/slack-like", json={"type": "event_callback", "event": {"type": "message"}}, timeout=5)
print(response.status_code, response.text)
```

- 진짜 `app/server.py`는 이 처리 **전에** 서명부터 확인합니다. 서명은 7단계에서 배웁니다.

</details>

---

## 과제 6. 도전: 404와 405 직접 만나 보기 (★★★)

**다지는 개념**: 엔드포인트와 주소(2-1), `@app.post`(2-4), 6단계 개발 기록 문제 5

**할 일**

`practice\step06\p6_client.py`를 만들어, 서버가 켜진 상태에서 창 2에서 실행합니다.

1. 만들지 않은 주소 `http://127.0.0.1:8001/`에 POST를 보냅니다. (과제 5의 주소 확인 요청 본문 그대로)
2. `http://127.0.0.1:8001/echo`에 **GET**을 보냅니다. (`requests.get`)
3. 각각 상태 코드와 응답 글자를 출력합니다.
4. 창 1의 서버 화면도 봅니다.

**확인 방법**

창 2:

```
404 {"detail":"Not Found"}
405 {"detail":"Method Not Allowed"}
```

창 1:

```
INFO:     127.0.0.1:60170 - "POST / HTTP/1.1" 404 Not Found
INFO:     127.0.0.1:60171 - "GET /echo HTTP/1.1" 405 Method Not Allowed
```

<details><summary>정답 예시</summary>

```python
import requests

BASE_URL = "http://127.0.0.1:8001"

response = requests.post(BASE_URL + "/", json={"type": "url_verification", "challenge": "practice-123"}, timeout=5)
print(response.status_code, response.text)

response = requests.get(BASE_URL + "/echo", timeout=5)
print(response.status_code, response.text)
```

- **404**: 그런 주소(창구)가 없다. 6단계에서 Request URL 끝에 `/slack/events`를 빠뜨렸을 때 서버 기록이 바로 `"POST / HTTP/1.1" 404 Not Found`였습니다. 그래서 Slack이 `challenge`를 받지 못해 확인에 실패했습니다.
- **405**: 주소는 있지만 그 방법(GET)으로는 받지 않는다. `@app.post`로 만든 창구는 POST만 받습니다.
- 서버 화면의 기록을 보면 어느 주소로 어떤 방법이 왔는지 바로 알 수 있습니다. 문제가 생기면 먼저 이 줄을 봅니다.

</details>

---

## 다 풀었다면

- [ ] `d["키"]`와 `d.get("키", 기본값)`의 차이를 말할 수 있다.
- [ ] `@app.post("/주소")`, `async def`, `await request.json()`으로 요청을 받는 창구를 만들 수 있다.
- [ ] 서버 기록의 404, 405를 보고 무엇이 잘못됐는지 말할 수 있다.

## 이번 단계 핵심 정리

1. `dict.get("키", 기본값)`은 키가 없어도 오류 없이 기본값을 준다. 밖에서 온 자료에 쓴다.
2. FastAPI는 `@app.post("/주소")`로 창구를 만들고, `await request.json()`으로 본문을 읽는다.
3. 서버는 `python -m uvicorn 파일위치:app --port 번호`로 켜고 Ctrl+C로 끈다. 코드를 고치면 다시 켠다.
4. 404는 주소가 없음, 405는 방법(GET/POST)이 틀림이다.
5. 주소에 값을 붙일 때는 `urlencode`, 나눌 때는 `urlparse`와 `parse_qs`를 쓴다.
