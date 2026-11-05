# 5단계 실습 과제: 예외 처리, 재시도, 로그

## 이 문서를 다 풀면 할 수 있게 되는 것

1. `try` / `except`로 오류를 잡고, 직접 만든 예외를 `raise`할 수 있다.
2. "한 번 실패하면 잠시 기다렸다 다시 시도"하는 코드를 만들 수 있다.
3. 로그 파일을 남기고, 오류 메시지에 비밀값이 새지 않게 할 수 있다.

## 시작하기 전에

- 함께 볼 문서: [`step05-learning.md`](step05-learning.md)
- 실습 파일은 `practice\step05\` 폴더에 만듭니다. (`New-Item -ItemType Directory -Force practice\step05`)
- 가상환경을 켜고 프로젝트 맨 위 폴더에서 `python practice\step05\파일.py`로 실행합니다. 이번 과제는 `app`을 가져오지 않습니다.
- 결과는 모두 실제로 실행해 확인했습니다. 오류 화면의 긴 파일 경로는 `...`로 줄였습니다.

---

## 과제 1. 숫자로 바꾸지 못하면 `-1` (★)

**다지는 개념**: `try` / `except`(2-1)

**할 일**

`practice\step05\p1_to_number.py`를 만듭니다.

1. 함수 `to_number(text: str) -> int`: `int(text)`의 결과를 돌려줍니다. 숫자로 바꾸지 못해 `ValueError`가 나면 `-1`을 돌려줍니다.
2. `"12"`, `" 7 "`, `"열둘"`로 확인합니다.

**확인 방법**

```
12
7
-1
```

둘째 줄: `int`는 앞뒤 빈칸은 알아서 무시합니다. 하지만 글자가 섞이면 바꾸지 못합니다.

<details><summary>정답 예시</summary>

```python
# try / except 연습: 숫자로 바꾸지 못하면 -1
def to_number(text: str) -> int:
    try:
        return int(text)
    except ValueError:
        return -1


print(to_number("12"))
print(to_number(" 7 "))
print(to_number("열둘"))
```

- 잡을 오류를 `ValueError`처럼 **정해서** 잡습니다. 다른 종류의 오류는 잡지 않고 그대로 보이게 둡니다.

</details>

---

## 과제 2. 내 예외 만들고 일으키기 (★★)

**다지는 개념**: `raise`와 직접 만든 예외(2-2), `as error`(2-3)

**할 일**

`practice\step05\p2_custom_error.py`를 만듭니다.

1. 예외 `MenuError`를 만듭니다. (`Exception`을 바탕으로, 내용은 비워 둠)
2. 함수 `check_menu(menu: str) -> str`: 앞뒤 빈칸을 지운 메뉴가 비어 있으면 `MenuError("메뉴가 비어 있습니다")`를 일으키고, 아니면 다듬은 메뉴를 돌려줍니다.
3. `["부대찌개", "   ", "백김치"]`를 하나씩 확인합니다. 성공하면 `확인:`, `MenuError`면 `오류:`와 오류 내용을 출력합니다.

**확인 방법**

```
확인: 부대찌개
오류: 메뉴가 비어 있습니다
확인: 백김치
```

둘째 메뉴에서 오류가 나도 반복이 멈추지 않고 셋째 메뉴로 갑니다. `try`가 `for` **안에** 있기 때문입니다.

<details><summary>정답 예시</summary>

```python
# 직접 만든 예외와 raise 연습
class MenuError(Exception):
    pass


def check_menu(menu: str) -> str:
    if menu.strip() == "":
        raise MenuError("메뉴가 비어 있습니다")
    return menu.strip()


for menu in ["부대찌개", "   ", "백김치"]:
    try:
        print("확인:", check_menu(menu))
    except MenuError as error:
        print("오류:", error)
```

- `app/neis.py`의 `NeisError`가 같은 모양입니다. 직접 만든 예외는 "NEIS 문제"처럼 **어떤 종류의 실패인지** 이름으로 알려 줍니다.

</details>

---

## 과제 3. 여러 예외를 한 번에, 그리고 `and`의 순서 (★★)

**다지는 개념**: 여러 예외 한 번에 잡기, `type(error).__name__`(2-3), `and`와 단락 평가(2-5)

**할 일**

`practice\step05\p3_many_errors.py`를 만듭니다.

1. 함수 `get_first_dish(meal: dict) -> str`: `meal["dishes"][0]`을 돌려줍니다.
2. 아래 세 경우를 확인합니다. `KeyError`와 `IndexError`를 **한 `except`로** 잡고, 오류의 **종류 이름만** 출력합니다.
   ```python
   [{"dishes": ["흑미밥"]}, {"dishes": []}, {"menu": ["흑미밥"]}]
   ```
3. 함수 `has_menu(meal: dict) -> bool`: `"DDISH_NM"` 키가 있고, 그 값이 빈 글자가 아니면 `True`. `and` 한 줄로 씁니다.
4. `{}`, `{"DDISH_NM": ""}`, `{"DDISH_NM": "흑미밥"}`으로 확인합니다.

**확인 방법**

```
첫 메뉴: 흑미밥
꺼내지 못함: IndexError
꺼내지 못함: KeyError
False
False
True
```

**더 해 보기**: `has_menu`에서 `and` 양쪽의 순서를 바꿔 `meal["DDISH_NM"] != "" and "DDISH_NM" in meal`로 쓰고 `has_menu({})`를 실행해 보세요.

<details><summary>정답 예시</summary>

```python
# 여러 예외를 한 번에 잡고 종류 이름만 출력하기
def get_first_dish(meal: dict) -> str:
    return meal["dishes"][0]


for meal in [{"dishes": ["흑미밥"]}, {"dishes": []}, {"menu": ["흑미밥"]}]:
    try:
        print("첫 메뉴:", get_first_dish(meal))
    except (KeyError, IndexError) as error:
        print("꺼내지 못함:", type(error).__name__)


def has_menu(meal: dict) -> bool:
    return "DDISH_NM" in meal and meal["DDISH_NM"] != ""


print(has_menu({}))
print(has_menu({"DDISH_NM": ""}))
print(has_menu({"DDISH_NM": "흑미밥"}))
```

**더 해 보기**의 결과 (맨 아래 줄):

```
KeyError: 'DDISH_NM'
```

`and`는 왼쪽이 `False`면 오른쪽을 아예 보지 않습니다. 그래서 **안전한 확인(키가 있는가?)을 왼쪽에** 둡니다. 순서를 바꾸면 없는 키를 먼저 꺼내다 오류가 납니다.

</details>

---

## 과제 4. 로그 파일 남기기 (★★)

**다지는 개념**: `logging`(2-7)

**할 일**

`practice\step05\p4_logging.py`를 만듭니다.

1. 이 파일과 같은 폴더의 `practice.log`에 기록하는 logger를 만듭니다.
   - 이름은 `"practice"`, 등급은 `INFO` 이상
   - 한 줄 모양: `시각 [등급] 내용`
2. `info`, `warning`, `error`, `debug`로 한 줄씩 남깁니다.
3. 실행한 뒤 `practice\step05\practice.log`를 엽니다.
4. 한 번 더 실행하고 다시 열어 봅니다.

**확인 방법**

화면:

```
로그를 남겼습니다: C:\neis_groupware_bot\practice\step05\practice.log
```

`practice.log` (시각은 실행할 때마다 다릅니다):

```
2026-11-05 20:55:03,924 [INFO] 실습 시작
2026-11-05 20:55:03,924 [WARNING] 메뉴가 비어 있습니다
2026-11-05 20:55:03,924 [ERROR] NEIS 응답을 받지 못했습니다
```

- `debug` 줄은 남지 않습니다. 등급을 `INFO` 이상으로 정했기 때문입니다.
- 두 번째 실행 뒤에는 세 줄이 **더 붙습니다.** 로그 파일은 지우지 않고 뒤에 이어 씁니다.

<details><summary>정답 예시</summary>

```python
# logging으로 파일에 기록 남기기
import logging
from pathlib import Path

LOG_FILE: Path = Path(__file__).resolve().parent / "practice.log"

logger = logging.getLogger("practice")
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler(LOG_FILE, encoding="utf-8")
file_handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s"))
logger.addHandler(file_handler)

logger.info("실습 시작")
logger.warning("메뉴가 비어 있습니다")
logger.error("NEIS 응답을 받지 못했습니다")
logger.debug("이 줄은 남지 않습니다")
print("로그를 남겼습니다:", LOG_FILE)
```

`app/log.py`와 거의 같은 모양입니다. 이름(`"practice"`)과 파일만 다릅니다.

</details>

---

## 과제 5. 한 번 실패하면 다시 시도하기 (★★★)

**다지는 개념**: `try` / `except`(2-1), `time.sleep`(2-8), 재시도 흐름(`app/neis.py`의 `call_neis_api`)

**할 일**

`practice\step05\p5_retry.py`를 만듭니다.

1. 가짜 요청 함수 `flaky_request(attempt: int) -> str`: `attempt`가 1이면 `ConnectionError("연결 실패")`를 일으키고, 아니면 `"응답 받음"`을 돌려줍니다. (첫 시도만 실패하는 요청 흉내)
2. 함수 `call_with_retry() -> str`
   - `flaky_request(1)`을 시도합니다.
   - `ConnectionError`가 나면 `1번째 시도 실패: ConnectionError → 1초 뒤 다시 시도`를 출력하고 1초 기다립니다.
   - 그다음 `flaky_request(2)`의 결과를 돌려줍니다.
3. 결과를 출력합니다.

**확인 방법** (둘째 줄은 1초 뒤에 나옵니다)

```
1번째 시도 실패: ConnectionError → 1초 뒤 다시 시도
응답 받음
```

<details><summary>정답 예시</summary>

```python
# 한 번 실패하면 잠시 기다렸다가 다시 시도하기
import time


def flaky_request(attempt: int) -> str:
    # 첫 번째 시도만 실패하는 가짜 요청
    if attempt == 1:
        raise ConnectionError("연결 실패")
    return "응답 받음"


def call_with_retry() -> str:
    try:
        return flaky_request(1)
    except ConnectionError as error:
        print("1번째 시도 실패:", type(error).__name__, "→ 1초 뒤 다시 시도")
        time.sleep(1)
    return flaky_request(2)


print(call_with_retry())
```

- 첫 시도가 성공하면 `try` 안의 `return`에서 함수가 끝납니다. 실패했을 때만 아래 줄(두 번째 시도)까지 내려옵니다.

</details>

---

## 과제 6. 도전: 두 번 다 실패하면 — 비밀값을 숨기는 `from None` (★★★)

**다지는 개념**: `raise ... from None`(2-4), 오류 메시지에 인증키가 들어가는 문제(5단계 개발 기록 문제 1)

**할 일**

`practice\step05\p6_from_none.py`를 만듭니다.

1. 예외 `RetryError`를 만듭니다.
2. 늘 실패하는 가짜 요청 `always_fail(attempt: int) -> str`: 아래 오류를 일으킵니다. 메시지 안의 `KEY=SECRET-VALUE`는 인증키 흉내입니다.
   ```python
   raise ConnectionError("https://example.invalid/hub?KEY=SECRET-VALUE 에 연결하지 못함")
   ```
3. 함수 `call_twice() -> str`
   - 첫 시도가 실패하면 `1번째 시도 실패: ConnectionError`를 출력하고 1초 기다립니다.
   - 두 번째 시도도 실패하면 `RetryError("두 번 모두 실패했습니다. 원인: ConnectionError")`를 일으킵니다. 종류 이름은 `type(error).__name__`으로 넣고, 끝에 `from None`을 붙입니다.
4. 맨 아래에서 `call_twice()`를 `try` 없이 부릅니다. 오류 화면이 나오는 것이 정상입니다.
5. `from None`을 지우고 다시 실행해 두 화면을 비교합니다.

**확인 방법**

`from None`이 있을 때:

```
1번째 시도 실패: ConnectionError
Traceback (most recent call last):
  File "...\p6_from_none.py", line 25, in <module>
    call_twice()
    ~~~~~~~~~~^^
  File "...\p6_from_none.py", line 22, in call_twice
    raise RetryError(f"두 번 모두 실패했습니다. 원인: {type(error).__name__}") from None
RetryError: 두 번 모두 실패했습니다. 원인: ConnectionError
```

`from None`을 지웠을 때 (앞부분):

```
1번째 시도 실패: ConnectionError
Traceback (most recent call last):
  File "...\p6_from_none.py", line 20, in call_twice
    return always_fail(2)
  File "...\p6_from_none.py", line 10, in always_fail
    raise ConnectionError("https://example.invalid/hub?KEY=SECRET-VALUE 에 연결하지 못함")
ConnectionError: https://example.invalid/hub?KEY=SECRET-VALUE 에 연결하지 못함

During handling of the above exception, another exception occurred:
...
RetryError: 두 번 모두 실패했습니다. 원인: ConnectionError
```

`from None`이 없으면 원래 오류의 메시지(`KEY=SECRET-VALUE`)가 화면에 함께 나옵니다. 진짜 인증키였다면 그대로 노출됐을 것입니다.

<details><summary>정답 예시</summary>

```python
# 두 번 모두 실패하면 새 예외로 알리기. 원래 오류 메시지(비밀값 포함)는 숨긴다.
import time


class RetryError(Exception):
    pass


def always_fail(attempt: int) -> str:
    raise ConnectionError("https://example.invalid/hub?KEY=SECRET-VALUE 에 연결하지 못함")


def call_twice() -> str:
    try:
        return always_fail(1)
    except ConnectionError as error:
        print("1번째 시도 실패:", type(error).__name__)
        time.sleep(1)
    try:
        return always_fail(2)
    except ConnectionError as error:
        raise RetryError(f"두 번 모두 실패했습니다. 원인: {type(error).__name__}") from None


call_twice()
```

- `app/neis.py`의 `try_neis_once`와 `call_neis_api`가 이 방법을 씁니다. requests의 오류 메시지에는 요청 주소 전체(인증키 포함)가 들어 있기 때문입니다.
- 실제 프로그램은 `RetryError`(프로젝트에서는 `NeisError`)를 위에서 잡아 관리자에게 알립니다. 이 과제에서는 `from None`의 효과를 보려고 일부러 잡지 않았습니다.

</details>

---

## 다 풀었다면

- [ ] 잡을 오류를 정해서 `except 종류:`로 잡을 수 있다.
- [ ] `class 이름(Exception): pass`로 예외를 만들고 `raise`할 수 있다.
- [ ] 오류를 기록할 때 메시지 대신 `type(error).__name__`을 쓰는 이유를 말할 수 있다.

## 이번 단계 핵심 정리

1. `try` 안에서 오류가 나면 바로 `except`로 간다. 잡을 종류를 정해서 잡는다.
2. 직접 만든 예외는 `class 이름(Exception): pass`로 만들고 `raise 이름("내용")`으로 일으킨다.
3. `and`는 왼쪽이 `False`면 오른쪽을 보지 않으므로, 안전한 확인을 왼쪽에 둔다.
4. 재시도는 "시도 → 실패하면 기다림 → 한 번 더"이고, 두 번째도 실패하면 위로 알린다.
5. 외부 요청 오류는 종류 이름만 남기고, `from None`으로 원래 메시지(비밀값)를 숨긴다.
