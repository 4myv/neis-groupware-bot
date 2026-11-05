# 7단계 실습 과제: 바이트, HMAC 서명, 집합, 명령어 표

## 이 문서를 다 풀면 할 수 있게 되는 것

1. 문자열과 바이트의 차이를 알고, HMAC 서명을 직접 계산할 수 있다.
2. 서명이 맞지 않거나 오래된 요청을 거부하는 서버를 만들 수 있다.
3. 집합으로 중복을 거르고, 딕셔너리로 명령어 표를 만들 수 있다.

## 시작하기 전에

- 함께 볼 문서: [`step07-learning.md`](step07-learning.md)
- 실습 파일은 `practice\step07\` 폴더에 만듭니다. (`New-Item -ItemType Directory -Force practice\step07`)
- 가상환경을 켜고 프로젝트 맨 위 폴더에서 실행합니다.
  - 보통 파일: `python practice\step07\파일.py`
  - `app`을 가져오는 파일: `python -m practice.step07.파일`
- **실습용 Secret은 `practice-secret`(가짜 값)** 을 씁니다. `.env`의 진짜 Signing Secret은 쓰지 않습니다.
- 과제 6은 PowerShell 창 두 개가 필요합니다. (서버는 8001번 포트)
- 결과는 모두 실제로 실행해 확인했습니다.

---

## 과제 1. 문자열과 바이트 (★)

**다지는 개념**: 바이트와 `encode`(2-2), `len()`

**할 일**

`practice\step07\p1_bytes.py`를 만듭니다.

1. `text = "급식"`을 UTF-8 바이트로 바꿔 `data`에 넣고 출력합니다.
2. `text`의 길이와 `data`의 길이를 `len()`으로 출력합니다.
3. 바이트 `b"v0:"` 뒤에 `data`를 이어 붙여 출력합니다.

**확인 방법**

```
b'\xea\xb8\x89\xec\x8b\x9d'
2
6
b'v0:\xea\xb8\x89\xec\x8b\x9d'
```

- 글자는 2개지만, 바이트는 6개입니다. UTF-8에서 한글 한 글자는 바이트 3개입니다.
- 바이트는 앞에 `b`가 붙고, 한글은 `\xea` 같은 16진수로 보입니다.

**더 해 보기**: `print("v0:" + "급식".encode("utf-8"))`를 실행해 보세요.

<details><summary>정답 예시</summary>

```python
# 문자열과 바이트 연습
text = "급식"
data = text.encode("utf-8")

print(data)
print(len(text))
print(len(data))
print(b"v0:" + data)
```

**더 해 보기**의 결과 (맨 아래 줄):

```
TypeError: can only concatenate str (not "bytes") to str
```

문자열과 바이트는 바로 이어 붙일 수 없습니다. 둘 다 바이트로 맞춥니다: `"v0:".encode("utf-8") + data`. `app/auth.py`의 `make_slack_signature`가 이렇게 합니다.

</details>

---

## 과제 2. HMAC 서명 직접 계산하기 (★★)

**다지는 개념**: 서명(HMAC)(2-1), `hmac`, `hashlib`(2-3), f-문자열(step03)

**할 일**

`practice\step07\p2_hmac.py`를 만듭니다.

1. 아래 값으로 시작합니다.
   ```python
   SECRET = "practice-secret"
   timestamp = "1700000000"
   body = b'{"text":"hello"}'
   ```
2. Slack 방식대로 서명을 **직접** 계산합니다.
   - 서명할 내용: `v0:` + 시각 + `:` + 본문 (바이트)
   - `hmac.new(Secret 바이트, 서명할 내용, hashlib.sha256).hexdigest()` 앞에 `v0=`을 붙입니다.
3. 직접 계산한 서명을 출력하고, 프로젝트 함수 `make_slack_signature(SECRET, timestamp, body)`의 결과와 같은지 출력합니다.
4. 본문에서 **한 글자만** 바꾼 `b'{"text":"hellO"}'`의 서명도 출력합니다.
5. `python -m practice.step07.p2_hmac`로 실행합니다.

**확인 방법**

```
v0=f90ab086bfa2caba7094fec98401b47535ab20f25634e8ae4ac114d118fbeaef
True
v0=293fdd3dd444af9f72490844db2f4f26f84e2951dbb813741520ad8b821aa0bd
```

`o` 한 글자를 `O`로 바꿨을 뿐인데 서명이 완전히 달라졌습니다. 그래서 중간에서 본문을 바꾸면 들통납니다.

<details><summary>정답 예시</summary>

```python
# HMAC 서명을 직접 계산하고, 프로젝트 함수의 결과와 비교하기
import hashlib
import hmac

from app.auth import make_slack_signature

SECRET = "practice-secret"
timestamp = "1700000000"
body = b'{"text":"hello"}'

basestring = f"v0:{timestamp}:".encode("utf-8") + body
my_signature = "v0=" + hmac.new(SECRET.encode("utf-8"), basestring, hashlib.sha256).hexdigest()

print(my_signature)
print(my_signature == make_slack_signature(SECRET, timestamp, body))
print(make_slack_signature(SECRET, timestamp, b'{"text":"hellO"}'))
```

- 여기서는 결과를 보려고 `==`로 비교했습니다. 진짜 검증에서는 `hmac.compare_digest`를 씁니다. (2-3)

</details>

---

## 과제 3. 오래된 요청과 틀린 Secret 거르기 (★★)

**다지는 개념**: 재전송 공격(2-1), `int()`와 `abs()`(2-4), 프로젝트 함수 `is_valid_slack_request`

**할 일**

`practice\step07\p3_replay.py`를 만듭니다. 과제 2의 값으로 서명(`signature`)을 만든 뒤, `is_valid_slack_request(Secret, 시각, 서명, 본문, 지금)`의 결과를 출력합니다.

1. 올바른 Secret, 지금 = `1700000060` (보낸 지 60초 뒤)
2. 올바른 Secret, 지금 = `1700000400` (400초 뒤)
3. Secret을 `"wrong-secret"`으로, 지금 = `1700000060`
4. 시각을 `"abc"`로, 지금 = `1700000060`
5. 마지막으로 `abs(1700000060 - int(timestamp))`를 출력합니다.

**먼저 예상해 적어 보고** 실행합니다. (허용 시간은 5분 = 300초)

**확인 방법**

```
True
False
False
False
60
```

<details><summary>정답 예시</summary>

```python
# 시각과 Secret을 바꿔 가며 서명 검증 결과 보기
from app.auth import is_valid_slack_request, make_slack_signature

SECRET = "practice-secret"
timestamp = "1700000000"
body = b'{"text":"hello"}'
signature = make_slack_signature(SECRET, timestamp, body)

print(is_valid_slack_request(SECRET, timestamp, signature, body, 1700000060))
print(is_valid_slack_request(SECRET, timestamp, signature, body, 1700000400))
print(is_valid_slack_request("wrong-secret", timestamp, signature, body, 1700000060))
print(is_valid_slack_request(SECRET, "abc", signature, body, 1700000060))
print(abs(1700000060 - int(timestamp)))
```

| 줄 | 결과 | 이유 |
| --- | --- | --- |
| 1 | `True` | 서명이 맞고 60초 차이 |
| 2 | `False` | 서명은 맞지만 400초 차이 → 5분 넘은 요청(재전송 공격 방지) |
| 3 | `False` | Secret이 다르면 같은 서명이 나오지 않음 |
| 4 | `False` | 시각이 숫자가 아니면 `int()` 전에 거름 |

`now`(지금 시각)를 매개변수로 받게 만들어 두었기 때문에, 이렇게 원하는 시각을 넣어 시험할 수 있습니다.

</details>

---

## 과제 4. 같은 이벤트는 한 번만 (★)

**다지는 개념**: 집합(`set`)(2-5), `len()`

**할 일**

`practice\step07\p4_set.py`를 만듭니다.

1. 빈 집합 `processed`를 만듭니다.
2. `["Ev1", "Ev2", "Ev1", "Ev3", "Ev2"]`를 차례로 보며, 이미 집합에 있으면 `이미 처리해서 건너뜀`, 없으면 집합에 넣고 `처리`를 출력합니다.
3. 마지막에 처리한 이벤트 수를 출력합니다.

**확인 방법**

```
Ev1 처리
Ev2 처리
Ev1 이미 처리해서 건너뜀
Ev3 처리
Ev2 이미 처리해서 건너뜀
처리한 이벤트 수: 3
```

<details><summary>정답 예시</summary>

```python
# 집합으로 같은 이벤트를 한 번만 처리하기
processed = set()

for event_id in ["Ev1", "Ev2", "Ev1", "Ev3", "Ev2"]:
    if event_id in processed:
        print(event_id, "이미 처리해서 건너뜀")
    else:
        processed.add(event_id)
        print(event_id, "처리")

print("처리한 이벤트 수:", len(processed))
```

- 빈 집합은 `set()`으로 만듭니다. `{}`는 빈 **딕셔너리**입니다.
- `app/server.py`의 `is_duplicate_event`가 이 방법으로 Slack의 재전송을 거릅니다.

</details>

---

## 과제 5. 내 명령어 표 만들기 (★★)

**다지는 개념**: `split()` + `join`으로 띄어쓰기 지우기(2-6), `dict[str, str]`(2-7)

**할 일**

`practice\step07\p5_commands.py`를 만듭니다.

1. 명령어 표 `MY_COMMANDS: dict[str, str]`를 만듭니다. 키는 **띄어쓰기를 지운 모양**입니다.
   - `"급식"`, `"오늘급식"` → `"today_lunch"`
   - `"내일급식"` → `"tomorrow_lunch"`
   - `"일정"` → `"this_week_schedule"`
2. 함수 `remove_spaces(text: str) -> str`: 빈칸·탭·줄바꿈을 모두 지웁니다.
3. 함수 `parse(text: str) -> str`: 띄어쓰기를 지운 뒤 표에 있으면 그 이름, 없으면 `"help"`.
4. 아래로 확인합니다. (`repr`은 보이지 않는 글자까지 보여 줍니다. step07 2-6 참고)
   ```python
   for text in ["급식", " 오늘 급식", "내일\t급식", "일 정\n", "점심 뭐야"]:
       print(repr(text), "→", parse(text))
   ```

**확인 방법**

```
'급식' → today_lunch
' 오늘 급식' → today_lunch
'내일\t급식' → tomorrow_lunch
'일 정\n' → this_week_schedule
'점심 뭐야' → help
```

<details><summary>정답 예시</summary>

```python
# 내 명령어 표 만들기: 띄어쓰기를 지우고 표에서 찾기
MY_COMMANDS: dict[str, str] = {
    "급식": "today_lunch",
    "오늘급식": "today_lunch",
    "내일급식": "tomorrow_lunch",
    "일정": "this_week_schedule",
}


def remove_spaces(text: str) -> str:
    return "".join(text.split())


def parse(text: str) -> str:
    key = remove_spaces(text)
    if key in MY_COMMANDS:
        return MY_COMMANDS[key]
    return "help"


for text in ["급식", " 오늘 급식", "내일\t급식", "일 정\n", "점심 뭐야"]:
    print(repr(text), "→", parse(text))
```

- 한 명령어에 여러 표현(`급식`, `오늘급식`)을 연결하려면 표에 줄만 더하면 됩니다. 코드는 그대로입니다.

</details>

---

## 과제 6. 도전: 서명이 맞는 요청만 받는 서버 (★★★)

**다지는 개념**: 서명 검증 전체 흐름(2-1~2-4), 응답 상태 코드 `401`(2-8), 원래 본문(바이트) 읽기

**할 일**

1. `practice\step07\sign_server.py`를 만듭니다.
   - `POST /signed` 창구
   - 원래 본문을 **바이트로** 읽습니다. (`await request.body()`)
   - 헤더 `x-practice-timestamp`, `x-practice-signature`를 꺼냅니다. (없으면 `""`)
   - `is_valid_slack_request(PRACTICE_SECRET, 시각, 서명, 본문, time.time())`이 `False`면 `invalid signature`를 **상태 코드 401**로 돌려줍니다.
   - 맞으면 `ok`를 돌려줍니다.
2. 창 1에서 켭니다: `python -m uvicorn practice.step07.sign_server:app --port 8001`
3. `practice\step07\p6_client.py`를 만들어 창 2에서 `python -m practice.step07.p6_client`로 실행합니다. 세 요청을 보냅니다.
   - **서명한 요청**: 본문 `'{"text":"오늘 급식"}'`(UTF-8 바이트), 지금 시각, 그 서명을 헤더에 넣음
   - **본문을 바꾼 요청**: 헤더는 그대로, 본문만 `'{"text":"내일 급식"}'`
   - **서명 없는 요청**: 헤더 없이 본문만

**확인 방법**

창 2:

```
서명한 요청: 200 ok
본문을 바꾼 요청: 401 invalid signature
서명 없는 요청: 401 invalid signature
```

창 1:

```
INFO:     127.0.0.1:60182 - "POST /signed HTTP/1.1" 200 OK
INFO:     127.0.0.1:60183 - "POST /signed HTTP/1.1" 401 Unauthorized
INFO:     127.0.0.1:60184 - "POST /signed HTTP/1.1" 401 Unauthorized
```

<details><summary>힌트</summary>

- 바이트 본문은 `requests.post(주소, data=본문, headers=헤더)`로 보냅니다. `json=`을 쓰면 requests가 본문을 다시 만들어서, 서명한 바이트와 달라질 수 있습니다.
- 지금 시각(초, 정수 글자): `str(int(time.time()))`

</details>

<details><summary>정답 예시</summary>

`practice\step07\sign_server.py`:

```python
# 서명이 맞는 요청만 받는 실습 서버. 실행: python -m uvicorn practice.step07.sign_server:app --port 8001
import time

from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse

from app.auth import is_valid_slack_request

PRACTICE_SECRET = "practice-secret"

app = FastAPI()


@app.post("/signed")
async def signed(request: Request) -> PlainTextResponse:
    body = await request.body()
    timestamp = request.headers.get("x-practice-timestamp", "")
    signature = request.headers.get("x-practice-signature", "")
    if not is_valid_slack_request(PRACTICE_SECRET, timestamp, signature, body, time.time()):
        return PlainTextResponse("invalid signature", status_code=401)
    return PlainTextResponse("ok")
```

`practice\step07\p6_client.py`:

```python
# 서명한 요청, 본문을 바꾼 요청, 서명 없는 요청 보내기
import time

import requests

from app.auth import make_slack_signature

PRACTICE_SECRET = "practice-secret"
URL = "http://127.0.0.1:8001/signed"

body = '{"text":"오늘 급식"}'.encode("utf-8")
timestamp = str(int(time.time()))
headers = {
    "Content-Type": "application/json",
    "X-Practice-Timestamp": timestamp,
    "X-Practice-Signature": make_slack_signature(PRACTICE_SECRET, timestamp, body),
}

response = requests.post(URL, data=body, headers=headers, timeout=5)
print("서명한 요청:", response.status_code, response.text)

changed_body = '{"text":"내일 급식"}'.encode("utf-8")
response = requests.post(URL, data=changed_body, headers=headers, timeout=5)
print("본문을 바꾼 요청:", response.status_code, response.text)

response = requests.post(URL, data=body, timeout=5)
print("서명 없는 요청:", response.status_code, response.text)
```

- 헤더 이름은 대문자로 보내도 서버에서 소문자로 꺼낼 수 있습니다. HTTP 헤더 이름은 대소문자를 가리지 않습니다.
- 진짜 `app/server.py`와 같은 구조입니다. 다른 점은 헤더 이름(`x-slack-...`)과 Secret(`.env`의 값)뿐입니다.

</details>

---

## 다 풀었다면

- [ ] 문자열과 바이트를 이어 붙일 때 왜 `encode`가 필요한지 말할 수 있다.
- [ ] 서명에 시각을 넣고 5분 넘은 요청을 거부하는 이유를 말할 수 있다.
- [ ] 서명이 틀린 요청에 401을 돌려주는 서버를 만들 수 있다.

## 이번 단계 핵심 정리

1. 서명은 바이트로 계산한다. 문자열은 `.encode("utf-8")`로 바이트로 바꾼다.
2. `hmac.new(Secret, v0:시각:본문, hashlib.sha256).hexdigest()` 앞에 `v0=`을 붙이면 Slack 방식 서명이다.
3. 본문이 한 글자만 달라도 서명이 완전히 바뀌고, Secret이 없으면 맞는 서명을 만들 수 없다.
4. 집합(`set()`)은 이미 본 값을 기억해 중복을 거를 때 쓴다.
5. 명령어 표는 띄어쓰기를 지운 키로 만들고, 찾는 말도 띄어쓰기를 지워 찾는다.
