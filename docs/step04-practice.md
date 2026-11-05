# 4단계 실습 과제: 파일 경로, 파일 읽고 쓰기, 토큰과 HTTP 헤더

## 이 문서를 다 풀면 할 수 있게 되는 것

1. `pathlib`로 "이 파일 기준" 경로를 만들고, 파일이 있는지 확인할 수 있다.
2. 딕셔너리를 JSON 파일로 저장하고 다시 읽어 올 수 있다.
3. `Authorization: Bearer` 헤더를 만들고, Slack의 `{"ok": ..., "error": ...}` 응답을 읽을 수 있다.

## 시작하기 전에

- 함께 볼 문서: [`step04-learning.md`](step04-learning.md)
- 실습 파일은 `practice\step04\` 폴더에 만듭니다. (`New-Item -ItemType Directory -Force practice\step04`)
- 가상환경을 켜고 프로젝트 맨 위 폴더에서 실행합니다.
  - 보통 파일: `python practice\step04\파일.py`
  - `app`을 가져오는 파일: `python -m practice.step04.파일`
- **이번 실습은 진짜 Slack 토큰을 쓰지 않습니다.** 과제 6도 일부러 만든 가짜 토큰만 씁니다. 실제 채널로 메시지가 가지 않습니다.
- 결과는 모두 실제로 실행해 확인했습니다. 경로는 프로젝트가 `C:\neis_groupware_bot`에 있을 때의 모양입니다.

---

## 과제 1. 이 파일을 기준으로 경로 만들기 (★)

**다지는 개념**: `pathlib`(2-5): `Path`, `__file__`, `.resolve()`, `.parent`, `/`

**할 일**

`practice\step04\p1_path.py`를 만듭니다.

1. 이 파일이 들어 있는 폴더를 `PRACTICE_DIR`에 넣습니다.
2. 그 폴더의 두 단계 위(프로젝트 맨 위 폴더)를 `PROJECT_ROOT`에 넣습니다.
3. 아래 네 가지를 출력합니다.
   - `PRACTICE_DIR`
   - `PROJECT_ROOT` 아래 `requirements.txt`의 경로
   - 그 파일이 있는지 (`.exists()`)
   - `PROJECT_ROOT` 아래 `no_such_file.txt`가 있는지

**확인 방법**

```
C:\neis_groupware_bot\practice\step04
C:\neis_groupware_bot\requirements.txt
True
False
```

**더 해 보기**: PowerShell에서 `cd practice`로 폴더를 옮긴 뒤 `python step04\p1_path.py`로 실행해 보세요. 결과가 같게 나옵니다. 실행한 폴더가 아니라 **파일의 위치**를 기준으로 경로를 만들었기 때문입니다. (끝나면 `cd ..`)

<details><summary>정답 예시</summary>

```python
# pathlib 연습: 이 파일의 위치를 기준으로 경로 만들기
from pathlib import Path

PRACTICE_DIR: Path = Path(__file__).resolve().parent
PROJECT_ROOT: Path = PRACTICE_DIR.parent.parent

print(PRACTICE_DIR)
print(PROJECT_ROOT / "requirements.txt")
print((PROJECT_ROOT / "requirements.txt").exists())
print((PROJECT_ROOT / "no_such_file.txt").exists())
```

- 한 단계씩 올라갑니다.

  | 코드 | 가리키는 곳 |
  | --- | --- |
  | `Path(__file__).resolve()` | `...\practice\step04\p1_path.py` (이 파일) |
  | `PRACTICE_DIR` (위의 `.parent`) | `...\practice\step04` |
  | `PRACTICE_DIR.parent` | `...\practice` |
  | `PRACTICE_DIR.parent.parent` | 프로젝트 맨 위 폴더 |
- `app/config.py`의 `PROJECT_ROOT`도 같은 방법입니다: `app\config.py` → `app` → 프로젝트 맨 위.

</details>

---

## 과제 2. 딕셔너리를 JSON 파일로 저장하고 다시 읽기 (★★)

**다지는 개념**: `with open(...) as file`(2-6), `json.dump`, `json.load`(2-7)

**할 일**

`practice\step04\p2_json_file.py`를 만듭니다.

1. 저장할 파일 경로 `MEMO_FILE`: 이 파일과 같은 폴더의 `memo.json`
2. 딕셔너리 `memo = {"school": "서울고등학교", "favorite": ["부대찌개", "고등어구이"]}`를 `MEMO_FILE`에 **쓰기 모드**로 저장합니다. 한글이 그대로 보이게, 두 칸 들여쓰기로 저장합니다.
3. 같은 파일을 **읽기 모드**로 열어 `loaded`에 읽어 옵니다.
4. `loaded["favorite"]`과, `loaded == memo`의 결과를 출력합니다.
5. 실행한 뒤 `practice\step04\memo.json`을 VS Code나 메모장으로 열어 내용을 봅니다.

**확인 방법**

화면:

```
['부대찌개', '고등어구이']
True
```

`memo.json` 내용:

```json
{
  "school": "서울고등학교",
  "favorite": [
    "부대찌개",
    "고등어구이"
  ]
}
```

**더 해 보기**: `ensure_ascii=False`를 지우고 다시 실행한 뒤 `memo.json`을 열어 보세요. 한글이 `\uc11c\uc6b8...` 모양으로 바뀝니다. 읽어 오면(`loaded == memo`) 여전히 `True`입니다.

<details><summary>정답 예시</summary>

```python
# with open과 json.dump / json.load 연습
import json
from pathlib import Path

MEMO_FILE: Path = Path(__file__).resolve().parent / "memo.json"

memo = {"school": "서울고등학교", "favorite": ["부대찌개", "고등어구이"]}

with open(MEMO_FILE, "w", encoding="utf-8") as file:
    json.dump(memo, file, ensure_ascii=False, indent=2)

with open(MEMO_FILE, "r", encoding="utf-8") as file:
    loaded = json.load(file)

print(loaded["favorite"])
print(loaded == memo)
```

- `"w"`는 파일 내용을 **지우고** 새로 씁니다. 읽기만 할 때는 꼭 `"r"`을 씁니다.
- `app/auth.py`의 `save_tokens`, `load_tokens`가 같은 방법으로 토큰 파일을 쓰고 읽습니다.

</details>

---

## 과제 3. 토큰을 새로 받을 때인가? (★★)

**다지는 개념**: `time.time()`(2-8), 토큰과 만료(2-1), 프로젝트 함수 `needs_refresh`

**할 일**

`practice\step04\p3_needs_refresh.py`를 만듭니다.

1. `time`과, `app.auth`의 `needs_refresh`를 가져옵니다.
2. 지금 시각(`time.time()`)을 `now`에, 그 1시간(3600초) 뒤를 `expires_at`(만료 시각)에 넣습니다.
3. 세 시각에서 `needs_refresh(expires_at, 시각)`을 출력합니다: 지금, 3000초 뒤, 3400초 뒤
4. 결과를 **실행 전에 먼저 예상해** 적어 봅니다. (`REFRESH_MARGIN_SECONDS`는 300초)
5. `python -m practice.step04.p3_needs_refresh`로 실행합니다.

**확인 방법**

```
False
False
True
```

<details><summary>정답 예시</summary>

```python
# time.time()과 프로젝트의 needs_refresh 연습
import time

from app.auth import needs_refresh

now = time.time()
expires_at = now + 3600

print(needs_refresh(expires_at, now))
print(needs_refresh(expires_at, now + 3000))
print(needs_refresh(expires_at, now + 3400))
```

- 만료 300초 **전**부터 새로 받습니다. 기준은 `3600 - 300 = 3300`초 뒤입니다.
- 3000초 뒤는 아직 300초 넘게 남아서 `False`, 3400초 뒤는 남은 시간이 200초라서 `True`입니다.

</details>

---

## 과제 4. `Authorization` 헤더 만들기 (★)

**다지는 개념**: HTTP 헤더와 `Authorization: Bearer`(2-3), f-문자열(step03)

**할 일**

`practice\step04\p4_headers.py`를 만듭니다.

1. 함수 `make_headers(access_token: str) -> dict`: 아래 두 헤더가 든 딕셔너리를 돌려줍니다.
   - `Authorization`: `Bearer ` + 토큰 (Bearer 뒤에 빈칸 하나)
   - `Content-Type`: `application/json; charset=utf-8`
2. `make_headers("TEST-TOKEN")`을 출력합니다.

**확인 방법**

```
{'Authorization': 'Bearer TEST-TOKEN', 'Content-Type': 'application/json; charset=utf-8'}
```

<details><summary>정답 예시</summary>

```python
def make_headers(access_token: str) -> dict:
    return {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json; charset=utf-8",
    }


print(make_headers("TEST-TOKEN"))
```

`app/sender.py`의 `send_once`가 같은 헤더를 만듭니다. 이 함수는 과제 6에서 다시 씁니다.

</details>

---

## 과제 5. 돌려주는 값이 없는 함수로 응답 설명하기 (★★)

**다지는 개념**: `-> None`(2-9), Slack 응답 모양(2-4)

**할 일**

과제 4의 파일에 이어서 씁니다.

1. 함수 `describe_response(response_body: dict) -> None`
   - `ok`가 `True`면 `성공`을 출력합니다.
   - 아니면 `실패:`와 `error` 값을 출력합니다.
   - 아무것도 돌려주지 않습니다.
2. 아래를 실행합니다.
   ```python
   describe_response({"ok": True, "channel": "C0000000000"})
   describe_response({"ok": False, "error": "channel_not_found"})
   result = describe_response({"ok": True})
   print(result)
   ```

**확인 방법**

```
성공
실패: channel_not_found
성공
None
```

마지막 줄: 돌려주는 값이 없는 함수의 결과를 변수에 넣으면 `None`입니다.

<details><summary>정답 예시</summary>

```python
def describe_response(response_body: dict) -> None:
    if response_body["ok"]:
        print("성공")
    else:
        print("실패:", response_body["error"])
```

- `if response_body["ok"]:`는 `if response_body["ok"] == True:`와 같은 뜻입니다.
- `C0000000000`은 일부러 만든 가짜 채널 ID입니다.

</details>

---

## 과제 6. 도전: 가짜 토큰으로 Slack에 직접 물어보기 (★★★)

**다지는 개념**: `requests.post`(2-2), 헤더(2-3), Slack 응답 모양(2-4)

**할 일**

과제 4·5의 파일에 이어서 씁니다.

1. `requests`를 가져옵니다.
2. Slack의 `auth.test`(토큰이 맞는지 확인해 주는 기능)에 POST 요청을 두 번 보냅니다. 주소는 `https://slack.com/api/auth.test`입니다.
   - 첫 번째: `headers=make_headers("xoxb-FAKE-TOKEN-FOR-PRACTICE")` (가짜 토큰)
   - 두 번째: 헤더 없이
   - 둘 다 `timeout=10`
3. 각 응답을 `.json()`으로 바꿔 `describe_response`에 넣습니다.

**확인 방법**

```
실패: invalid_auth
실패: not_authed
```

- `invalid_auth`: 토큰을 보냈지만 맞지 않는 토큰이다.
- `not_authed`: 토큰을 아예 보내지 않았다.
- 둘 다 HTTP 상태 코드는 200입니다. Slack은 성공·실패를 상태 코드가 아니라 본문의 `ok`로 알려 줍니다. 그래서 `app/sender.py`는 `ok`를 봅니다.

<details><summary>정답 예시</summary>

```python
import requests


def make_headers(access_token: str) -> dict:
    return {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json; charset=utf-8",
    }


def describe_response(response_body: dict) -> None:
    if response_body["ok"]:
        print("성공")
    else:
        print("실패:", response_body["error"])


response = requests.post("https://slack.com/api/auth.test", headers=make_headers("xoxb-FAKE-TOKEN-FOR-PRACTICE"), timeout=10)
describe_response(response.json())
response = requests.post("https://slack.com/api/auth.test", timeout=10)
describe_response(response.json())
```

- 진짜 토큰(`secrets\slack_tokens.json`)으로 해 보고 싶어도, 실습 파일에 토큰을 **복사해 붙이지 않습니다.** 필요하면 `app.auth`의 `get_access_token()`으로 꺼내 쓰고, 토큰 자체는 출력하지 않습니다.

</details>

---

## 다 풀었다면

- [ ] `Path(__file__).resolve().parent`가 무엇을 가리키는지 말할 수 있다.
- [ ] `"w"`와 `"r"`, `json.dump`와 `json.load`의 차이를 말할 수 있다.
- [ ] Slack 응답에서 성공·실패를 `ok`로 확인하는 이유를 말할 수 있다.

## 이번 단계 핵심 정리

1. `Path(__file__).resolve().parent`는 "이 파일이 있는 폴더"이고, `/`로 경로를 잇는다.
2. `with open(경로, "w" 또는 "r", encoding="utf-8") as file:`은 블록이 끝나면 파일을 자동으로 닫는다.
3. `json.dump(값, 파일)`은 저장, `json.load(파일)`은 읽기다. 한글은 `ensure_ascii=False`.
4. 토큰은 `Authorization: Bearer 토큰` 헤더로 보내고, 만료 300초 전부터 새로 받는다.
5. Slack은 실패해도 상태 코드 200을 주므로, 본문의 `ok`와 `error`를 확인한다.
