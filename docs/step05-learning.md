# 5단계 학습 정리: 예외 처리와 로그

## 이 문서를 다 읽으면 할 수 있게 되는 것

1. `try`/`except`로 오류를 잡아, 프로그램이 멈추지 않고 다른 일을 하게 만들 수 있다.
2. `raise`로 직접 만든 오류를 일으키고, 그 오류에 원인을 담아 전달할 수 있다.
3. `logging`으로 시각이 붙은 기록을 파일에 남기고, 그 기록에 비밀값이 섞이지 않게 할 수 있다.

## 읽기 전에

- 코드 예시는 모두 실제로 실행한 결과를 붙였습니다. 긴 파일 경로는 `예시.py`처럼 줄여 적었습니다.
- 앞 단계에서 설명한 것은 "step01 참고"처럼 적었습니다.
- 이번 단계에서 "오류"와 "예외"는 같은 뜻으로 씁니다. Python에서는 실행 중에 생긴 오류를 **예외**(exception)라고 부릅니다.

---

## 1. 이번 단계에서 새로 나온 것

**Python 문법**

1. `try` / `except`: 오류 잡기
2. `raise`와 직접 만든 예외 (`class NeisError(Exception)`)
3. 여러 예외를 한 번에 잡기, `as error`, `type(error).__name__`
4. `raise ... from None`
5. `and`와 단락 평가
6. 리스트에 쓰는 `in`

**라이브러리**

7. `logging`: 로그 파일 남기기
8. `time.sleep`: 잠시 기다리기

**설계**

9. 실패해도 같은 모양으로 돌려주기 (`post_message`)

**앞 단계에서 설명한 것**

- step01: 모듈을 `import`하면 그 파일의 코드가 한 번 실행된다
- step02: 함수, 딕셔너리, `for`, 메서드
- step03: `not`, `in`(딕셔너리 키), f-문자열, `{}`로 "없음" 표시
- step04: `time.time()`, `-> None`, Slack 응답의 `ok`와 `error`

---

## 2. 하나씩 설명

### 2-1. `try` / `except`: 오류 잡기

**설명**

지금까지는 오류가 나면 프로그램이 그 자리에서 멈췄습니다. (step01의 `Traceback`)

`try:` 블록 안에서 오류가 나면, 멈추지 않고 `except` 블록으로 건너뜁니다.
`except` 뒤에는 **어떤 종류의 오류**를 잡을지 적습니다. 다른 종류의 오류는 잡지 않습니다.

`try` 블록 안에서 오류가 난 줄 **다음 줄들은 실행되지 않습니다.**

**비유**

줄타기 아래의 안전망입니다. 떨어져도(오류) 바닥까지 가지 않고(프로그램 멈춤) 안전망(`except`)에 걸립니다.
안전망은 정해 둔 자리(오류 종류)에만 있습니다.

**작은 예시 1**

```python
school = {"SCHUL_NM": "서울고등학교"}
try:
    print(school["SD_SCHUL_CODE"])
except KeyError as error:
    print("없는 키:", error)
print("프로그램은 계속 실행됩니다")
```

결과:

```
없는 키: 'SD_SCHUL_CODE'
프로그램은 계속 실행됩니다
```

step02에서 같은 실수로 프로그램이 멈췄던 `KeyError`를 이번에는 잡았습니다.

**작은 예시 2: 오류 난 줄 다음은 건너뛴다**

```python
try:
    print("1. 요청을 보냈다")
    raise ValueError("응답이 JSON이 아니다")
    print("2. 이 줄은 실행되지 않는다")
except ValueError as error:
    print("3. 오류를 처리했다:", error)
```

결과:

```
1. 요청을 보냈다
3. 오류를 처리했다: 응답이 JSON이 아니다
```

(`raise`는 2-2에서 설명합니다.)

**이 프로젝트 코드** (`app/notifier.py`)

```python
try:
    meal_result = fetch_meals(NEIS_OFFICE_CODE, NEIS_SCHOOL_CODE, meal_date)
except NeisError as error:
    logger.error(f"{meal_date} 급식 알림 실패: {error}")
    notify_admin(f"{meal_date} 급식 정보를 NEIS에서 받지 못했습니다.\n{error}")
    return False
```

NEIS 조회가 실패하면 멈추지 않고 로그를 남긴 뒤, 관리자에게 알리고 `False`를 돌려줍니다.

**Java 비교**

```java
try {
    mealResult = Neis.fetchMeals(officeCode, schoolCode, mealDate);
} catch (NeisException e) {
    log.error(mealDate + " 급식 알림 실패: " + e.getMessage());
    return false;
}
```

Java의 `catch`가 Python의 `except`입니다. Python은 `catch (타입 이름)` 대신 `except 타입 as 이름:`으로 씁니다.

**자주 하는 실수: 다른 종류의 오류를 잡으려고 한다**

```python
class NeisError(Exception):
    pass


try:
    raise NeisError("두 번 모두 실패했습니다")
except ValueError:
    print("여기로 오지 않는다")
```

결과:

```
Traceback (most recent call last):
  File "예시.py", line 6, in <module>
    raise NeisError("두 번 모두 실패했습니다")
NeisError: 두 번 모두 실패했습니다
```

`NeisError`가 났는데 `ValueError`만 잡으려 해서, 안전망을 그냥 지나쳐 프로그램이 멈췄습니다.

---

### 2-2. `raise`와 직접 만든 예외

**설명**

`raise 오류("메시지")`는 오류를 **직접 일으킵니다.** "여기서 더 진행할 수 없다"고 알리는 방법입니다.

필요하면 우리 프로그램만의 오류 종류를 만들 수 있습니다.

```python
class NeisError(Exception):
    pass
```

- `class`는 새로운 종류(타입)를 만드는 문법입니다. 여기서는 오류 종류 하나를 만듭니다.
- `(Exception)`은 "Python의 기본 오류(`Exception`)와 같은 성질을 이어받는다"는 뜻입니다.
- `pass`는 "여기에 더 쓸 내용이 없다"는 표시입니다. 블록을 비워 둘 수 없어서 씁니다.

**비유**

NEIS 문제라는 이름표를 붙인 상자입니다. 받는 쪽은 이름표(`NeisError`)만 보고 "NEIS 문제구나" 하고 골라 잡을 수 있습니다.

**작은 예시**

```python
class NeisError(Exception):
    pass


def fetch():
    raise NeisError("두 번 모두 실패했습니다")


try:
    fetch()
except NeisError as error:
    print("잡은 오류:", error)
```

결과:

```
잡은 오류: 두 번 모두 실패했습니다
```

`raise`할 때 넣은 메시지가 `error`를 출력하면 나옵니다. 그래서 메시지에 **원인**을 담아 전달할 수 있습니다.

**이 프로젝트 코드** (`app/neis.py`)

```python
if result["CODE"] not in USABLE_RESULT_CODES:
    # NEIS가 보낸 결과 코드와 공식 설명을 원인으로 남긴다. 예: ERROR-290 인증키가 유효하지 않습니다.
    raise NeisError(f"{result['CODE']} {result['MESSAGE']}")
```

이 프로젝트가 만든 오류 종류는 두 개입니다.

| 오류 | 파일 | 언제 |
| --- | --- | --- |
| `NeisError` | `app/neis.py` | NEIS에서 쓸 수 있는 응답을 받지 못했을 때 |
| `SlackAuthError` | `app/auth.py` | Slack 토큰을 새로 발급받지 못했을 때 |

f-문자열 안에서 딕셔너리 키를 쓸 때는 바깥 따옴표(`"`)와 다른 따옴표(`'`)를 씁니다. (`result['CODE']`)

**Java 비교**

```java
class NeisException extends Exception {
    NeisException(String message) { super(message); }
}

throw new NeisException(code + " " + message);
```

Java의 `extends Exception`이 Python의 `(Exception)`, `throw new`가 `raise`입니다. Python은 메시지를 받는 생성자를 따로 쓰지 않아도 됩니다.

**자주 하는 실수: 블록을 비워 둔다**

```python
class NeisError(Exception):


print("끝")
```

결과:

```
  File "예시.py", line 4
    print("끝")
    ^^^^^
IndentationError: expected an indented block after class definition on line 1
```

`class` 아래에 들여쓴 줄이 하나도 없어서 오류가 났습니다. 쓸 내용이 없으면 `pass`를 씁니다.

---

### 2-3. 여러 예외를 한 번에 잡기, `as error`, `type(error).__name__`

**설명**

잡을 오류 종류가 여러 개면 괄호로 묶습니다. `except (A, B, C) as error:`

`as error`는 잡은 오류를 `error`라는 이름으로 쓰겠다는 뜻입니다.

`type(error).__name__`은 오류의 **종류 이름**만 꺼냅니다. `type(값)`은 값의 종류를 알려 주는 내장 함수이고, `.__name__`은 그 종류의 이름입니다.

**작은 예시**

```python
try:
    {}["KEY"]
except KeyError as error:
    print(type(error).__name__)
    print(error)
```

결과:

```
KeyError
'KEY'
```

**이 프로젝트 코드** (`app/neis.py`의 `try_neis_once`)

```python
except (requests.RequestException, ValueError, KeyError, IndexError) as error:
    raise NeisError(f"응답을 받지 못함({type(error).__name__})") from None
```

| 잡는 오류 | 언제 나는가 |
| --- | --- |
| `requests.RequestException` | 인터넷 연결 실패, 시간 초과 등 요청 자체가 실패 |
| `ValueError` | 응답이 JSON이 아님 (step02의 `JSONDecodeError`도 여기에 속함) |
| `KeyError`, `IndexError` | 응답 모양이 예상과 달라 값을 꺼내지 못함 |

**왜 메시지 대신 종류 이름만 쓰나요? (보안)**

`requests`의 오류 메시지에는 요청 주소 전체가 들어 있습니다. NEIS 요청 주소에는 `KEY=인증키`가 붙어 있습니다.
5단계에서 실제로 확인했더니, 연결 실패 오류의 메시지 안에 인증키가 **들어 있었습니다**(`True`). 메시지를 그대로 로그나 알림에 쓰면 인증키가 새어 나갑니다.

**Java 비교**

```java
} catch (RestClientException | JsonProcessingException e) {
    throw new NeisException("응답을 받지 못함(" + e.getClass().getSimpleName() + ")");
}
```

Java의 `catch (A | B e)`와 `e.getClass().getSimpleName()`입니다.

**자주 하는 실수: 오류 메시지를 그대로 로그에 쓴다**

`logger.warning(f"실패: {error}")`처럼 쓰면 편하지만, 위 이유로 인증키가 로그 파일에 남을 수 있습니다.
외부 요청에서 난 오류는 메시지에 무엇이 들었는지 모르므로, 종류 이름만 쓰는 편이 안전합니다.

---

### 2-4. `raise ... from None`

**설명**

`except` 블록 안에서 새 오류를 일으키면, Python은 오류 화면에 **원래 오류도 함께** 보여 줍니다. ("During handling of the above exception, another exception occurred")

`raise 새오류 from None`은 원래 오류를 함께 보여 주지 않게 합니다.

**이 프로젝트에서 실제로 확인한 것**

없는 주소로 요청하게 만들고, `NeisError`를 일부러 처리하지 않아 화면에 오류가 나오게 했습니다.

```
  File "C:\neis_groupware_bot\app\neis.py", line 90, in call_neis_api
    raise NeisError(f"NEIS {service_name} 호출이 두 번 모두 실패했습니다. 원인: {error}") from None
app.neis.NeisError: NEIS mealServiceDietInfo 호출이 두 번 모두 실패했습니다. 원인: 응답을 받지 못함(ConnectionError)
```

- 오류 화면 어디에도 인증키가 없었습니다. (검사 결과 `False`)
- "During handling ..." 문구도 없었습니다.

`from None`이 없으면 원래 오류(인증키가 든 주소가 섞인 메시지)가 화면에 함께 나옵니다. 화면에 나온 것은 캡처나 복사로 쉽게 퍼집니다.

**Java 비교**

Java는 `throw new NeisException(msg)`처럼 원인(`cause`)을 넘기지 않으면 원래 오류가 함께 출력되지 않습니다. Python은 반대로, 따로 막지 않으면 함께 출력됩니다.

**자주 하는 실수: 내 메시지만 안전하면 된다고 생각한다**

새 오류의 메시지를 안전하게 만들어도, `from None`이 없으면 원래 오류가 함께 보입니다. 두 가지를 모두 챙겨야 합니다.

---

### 2-5. `and`와 단락 평가

**설명**

`A and B`는 A와 B가 **둘 다** 참일 때만 `True`입니다.

Python은 A가 거짓이면 B를 **아예 계산하지 않습니다.** 이미 결과가 거짓으로 정해졌기 때문입니다. 이것을 단락 평가라고 합니다.

**작은 예시**

```python
response_body = {"ok": True}
print(not response_body["ok"] and response_body["error"] == "token_expired")
```

결과:

```
False
```

성공 응답에는 `error` 키가 없습니다. 그런데도 오류가 나지 않았습니다. `not True`가 `False`라서 `and` 뒤쪽을 계산하지 않았기 때문입니다.

**이 프로젝트 코드** (`app/sender.py`)

```python
def needs_new_token(response_body: dict) -> bool:
    return not response_body["ok"] and response_body["error"] in TOKEN_ERROR_CODES
```

"실패했고(`not ok`), 그 이유가 토큰 오류이면" 새 토큰이 필요합니다.

**Java 비교**

Java의 `&&`와 같습니다. Java도 앞이 `false`면 뒤를 계산하지 않습니다.

**자주 하는 실수: 순서를 바꾼다**

```python
response_body = {"ok": True}
print(response_body["error"] == "token_expired" and not response_body["ok"])
```

결과:

```
Traceback (most recent call last):
  File "예시.py", line 2, in <module>
    print(response_body["error"] == "token_expired" and not response_body["ok"])
          ~~~~~~~~~~~~~^^^^^^^^^
KeyError: 'error'
```

앞쪽에서 없는 키를 먼저 꺼내다가 오류가 났습니다. 안전한 확인을 앞에 둬야 합니다.

---

### 2-6. 리스트에 쓰는 `in`

**설명**

step03에서는 `in`으로 딕셔너리에 **키**가 있는지 봤습니다.
리스트에 `in`을 쓰면 그 **값**이 리스트 안에 있는지 봅니다.

**작은 예시**

```python
USABLE_RESULT_CODES = ["INFO-000", "INFO-200"]
print("INFO-200" in USABLE_RESULT_CODES)
print("ERROR-290" not in USABLE_RESULT_CODES)
```

결과:

```
True
True
```

**이 프로젝트 코드**

```python
USABLE_RESULT_CODES: list[str] = ["INFO-000", "INFO-200"]     # app/neis.py
if result["CODE"] not in USABLE_RESULT_CODES:

TOKEN_ERROR_CODES: list[str] = ["token_expired", "invalid_auth"]  # app/sender.py
... response_body["error"] in TOKEN_ERROR_CODES
```

`INFO-200`(데이터 없음)도 쓸 수 있는 응답에 넣었습니다. 주말·방학에 급식이 없는 것은 오류가 아니기 때문입니다. (CLAUDE.md)

**Java 비교**

```java
List.of("INFO-000", "INFO-200").contains(code);
```

**자주 하는 실수: 대소문자나 글자를 조금 다르게 쓴다**

`"info-200" in USABLE_RESULT_CODES`는 `False`입니다. 리스트에 든 값과 **글자 하나까지 같아야** 찾습니다.

---

### 2-7. `logging`: 로그 파일 남기기

**설명**

로그는 프로그램이 한 일을 시각과 함께 적어 두는 기록입니다. 문제가 생긴 뒤에 "언제, 무엇이" 일어났는지 볼 수 있습니다.

`logging`은 로그를 남기는 표준 라이브러리입니다. 세 가지를 짝지어 씁니다.

| 이름 | 하는 일 |
| --- | --- |
| logger | 로그를 받는 창구. `logger.info(...)`처럼 쓴다 |
| handler | 로그를 어디에 쓸지. 파일(`FileHandler`), 화면(`StreamHandler`) |
| formatter | 한 줄을 어떤 모양으로 쓸지. 시각, 등급, 내용 |

로그에는 중요도 **등급**이 있습니다.

| 등급 | 쓰는 때 |
| --- | --- |
| `info` | 정상적으로 한 일 (호출 성공, 전송 성공) |
| `warning` | 문제가 있었지만 계속 진행함 (첫 시도 실패 → 재시도) |
| `error` | 하려던 일을 끝내 못 함 (알림 실패) |
| `debug` | 아주 자세한 기록. 이 프로젝트는 `INFO`부터 남기도록 해서 기록되지 않음 |

**작은 예시** (파일 대신 화면에 출력)

```python
import logging

logger = logging.getLogger("demo")
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s"))
logger.addHandler(handler)

logger.info("NEIS 호출 성공")
logger.warning("NEIS 호출 실패: ConnectionError")
logger.error("급식 알림 실패")
logger.debug("이 줄은 INFO보다 낮아서 나오지 않는다")
```

결과:

```
2026-11-05 15:49:56,230 [INFO] NEIS 호출 성공
2026-11-05 15:49:56,230 [WARNING] NEIS 호출 실패: ConnectionError
2026-11-05 15:49:56,230 [ERROR] 급식 알림 실패
```

`%(asctime)s`(시각), `%(levelname)s`(등급), `%(message)s`(내용)는 `logging`이 정한 자리 표시입니다.

**이 프로젝트 코드** (`app/log.py`)

```python
LOG_FILE: Path = PROJECT_ROOT / "logs" / "bot.log"
LOG_FILE.parent.mkdir(exist_ok=True)

logger = logging.getLogger("lunch_bot")
logger.setLevel(logging.INFO)

file_handler = logging.FileHandler(LOG_FILE, encoding="utf-8")
file_handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s"))
logger.addHandler(file_handler)
```

다른 파일은 `from app.log import logger`로 가져와 씁니다.
처음 `import`될 때 이 설정 코드가 한 번 실행됩니다. (step01: import하면 그 파일의 코드가 한 번 실행된다)

**Java 비교**

```java
private static final Logger log = LoggerFactory.getLogger("lunch_bot");   // SLF4J
log.info("NEIS 호출 성공");
log.warn("NEIS 호출 실패: {}", errorType);
```

Spring Boot에서는 `application.properties`의 `logging.file.name`으로 파일을 정합니다. Python은 handler를 코드로 붙입니다.

**자주 하는 실수: 비밀값을 로그에 쓴다**

로그 파일은 오래 남고, 문제를 물어볼 때 남에게 보여 주기도 합니다. 그래서 이 프로젝트는 다음을 지킵니다.

- 인증키가 붙은 요청 주소(`response.url`)는 쓰지 않는다. (step02)
- 외부 요청 오류는 종류 이름만 쓴다. (2-3)
- 토큰은 쓰지 않는다. 쓰는 것은 "새로 발급받아 저장했습니다" 같은 사실뿐이다.

실제로 로그 파일 전체를 검사해 인증키, Client Secret, Signing Secret, 토큰이 하나도 없는 것을 확인했습니다. (개발 기록 4번)

---

### 2-8. `time.sleep`: 잠시 기다리기

**설명**

`time.sleep(초)`는 그 시간만큼 프로그램을 멈추고 기다립니다.

**작은 예시**

```python
import time

start = time.time()
time.sleep(1)
print(round(time.time() - start))
```

결과:

```
1
```

`round`는 소수를 가장 가까운 정수로 반올림하는 내장 함수입니다. 이 예시에서만 씁니다.

**이 프로젝트 코드** (`app/neis.py`)

```python
time.sleep(RETRY_WAIT_SECONDS)     # RETRY_WAIT_SECONDS = 3
```

CLAUDE.md 규칙 "잠시 후 한 번 재시도"입니다. 서버가 잠깐 바쁜 경우에는 조금 기다렸다 다시 부르면 성공할 수 있습니다.

**Java 비교**

```java
Thread.sleep(3000);   // 밀리초 단위
```

Python은 **초** 단위, Java는 **밀리초** 단위입니다.

**자주 하는 실수: Java처럼 밀리초로 쓴다**

`time.sleep(3000)`이라고 쓰면 3초가 아니라 3000초(50분)를 기다립니다.

---

### 2-9. 실패해도 같은 모양으로 돌려주기

**설명**

`post_message`는 성공하든 실패하든 **늘 `{"ok": ..., "error": ...}` 모양의 딕셔너리**를 돌려줍니다. 오류를 일으키지 않습니다.

그래서 부르는 쪽은 `try`/`except` 없이 `ok`만 확인하면 됩니다.

| 상황 | 돌려주는 것 |
| --- | --- |
| 성공 | Slack 응답 (`{"ok": True, ...}`) |
| Slack이 거절 | Slack 응답 (`{"ok": False, "error": "channel_not_found"}` 등) |
| 인터넷 연결 실패 | `{"ok": False, "error": "request_failed"}` (우리가 만든 코드) |
| 토큰 파일이 없거나 재발급 실패 | `{"ok": False, "error": "token_unavailable"}` (우리가 만든 코드) |

반대로 `fetch_meals`는 실패하면 `NeisError`를 **일으킵니다.** 실패하면 메시지를 만들 수 없으니, 부르는 쪽이 반드시 알아채야 하기 때문입니다.

**이 프로젝트 코드** (`app/notifier.py`)

```python
response_body = post_message(SLACK_CHANNEL_ID, message)
if not response_body["ok"]:
    notify_admin(f"{meal_date} 급식 알림을 Slack으로 보내지 못했습니다. (오류 코드: {response_body['error']})")
    return False
```

**Java 비교**

Java에서 결과 객체(`Result<T>`나 `ResponseEntity`)를 돌려주고 `isSuccess()`를 확인하는 방식과 같습니다.

**자주 하는 실수: 두 방식을 섞어 기대한다**

`post_message`를 `try`/`except`로 감싸도 실패는 잡히지 않습니다. 오류를 일으키지 않고 `ok: False`를 돌려주기 때문입니다. 함수마다 실패를 어떻게 알리는지 확인하고 써야 합니다.

---

## 3. 코드 줄 단위 해설

### 3-1. `app/log.py` (새 파일)

| 줄 | 코드 | 설명 |
| --- | --- | --- |
| 12 | `LOG_FILE: Path = PROJECT_ROOT / "logs" / "bot.log"` | 로그 파일 위치입니다. `logs/`는 `.gitignore`에 있습니다. (step04 `Path`) |
| 13 | `LOG_FILE.parent.mkdir(exist_ok=True)` | `logs` 폴더가 없으면 만듭니다. |
| 15 | `logger = logging.getLogger("lunch_bot")` | 이 프로젝트의 logger를 가져옵니다. 이름이 같으면 어디서 불러도 같은 logger입니다. |
| 16 | `logger.setLevel(logging.INFO)` | `info` 이상의 등급만 남깁니다. |
| 19 | `file_handler = logging.FileHandler(LOG_FILE, encoding="utf-8")` | 로그를 파일에 씁니다. 한글이 깨지지 않게 utf-8로 씁니다. |
| 20 | `file_handler.setFormatter(...)` | 한 줄의 모양을 "시각 [등급] 내용"으로 정합니다. |
| 21 | `logger.addHandler(file_handler)` | logger에 파일 handler를 붙입니다. |

### 3-2. `app/neis.py` (바뀐 부분)

**22~31줄: 상수와 오류 종류**

```python
RETRY_WAIT_SECONDS: int = 3
USABLE_RESULT_CODES: list[str] = ["INFO-000", "INFO-200"]


class NeisError(Exception):
    # NEIS에서 쓸 수 있는 응답을 받지 못했을 때 일으키는 오류. 메시지에 실패 원인을 담는다.
    pass
```

재시도 전 대기 시간, 쓸 수 있는 결과 코드(2-6), 오류 종류(2-2)입니다.

**34~40줄: `get_result` — 결과 코드와 설명 꺼내기**

```python
def get_result(response_body: dict, service_name: str) -> dict:
    if "RESULT" in response_body:
        return response_body["RESULT"]
    return response_body[service_name][0]["head"][1]["RESULT"]
```

NEIS 응답은 두 가지 모양입니다. (step02 개발 기록 6번)

- 데이터가 없거나 오류일 때는 맨 바깥에 `RESULT`가 있습니다.
- 정상일 때는 `head` 안 두 번째 칸에 `RESULT`가 있습니다.

어느 쪽이든 `{"CODE": ..., "MESSAGE": ...}`를 돌려줍니다.

**43~62줄: `try_neis_once` — 한 번 불러 보기**

| 줄 | 설명 |
| --- | --- |
| 45~52 | 요청, JSON 읽기, 결과 꺼내기를 `try` 안에서 합니다. |
| 53 | 요청 실패, JSON 아님, 모양이 다름 중 하나면 잡습니다. (2-3) |
| 57 | 종류 이름만 담은 `NeisError`를 일으킵니다. `from None`으로 원래 오류를 숨깁니다. (2-4) |
| 58~60 | 결과 코드가 쓸 수 없는 것이면 NEIS의 코드와 공식 설명을 담아 `NeisError`를 일으킵니다. |
| 61~62 | 성공을 로그에 남기고 응답을 돌려줍니다. |

**79~90줄: `call_neis_api` — 실패하면 한 번 더**

```python
    try:
        return try_neis_once(service_name, params)
    except NeisError as error:
        # 잠시 기다렸다가 한 번만 다시 시도한다. (CLAUDE.md 예외 처리 규칙)
        logger.warning(f"NEIS {service_name} 호출 실패: {error} → {RETRY_WAIT_SECONDS}초 뒤 다시 시도")
        time.sleep(RETRY_WAIT_SECONDS)

    try:
        return try_neis_once(service_name, params)
    except NeisError as error:
        logger.warning(f"NEIS {service_name} 다시 시도도 실패: {error}")
        raise NeisError(f"NEIS {service_name} 호출이 두 번 모두 실패했습니다. 원인: {error}") from None
```

| 줄 | 설명 |
| --- | --- |
| 79~80 | 첫 시도입니다. 성공하면 바로 돌려주고 함수가 끝납니다. |
| 81~84 | 실패하면 원인을 경고로 남기고 3초 기다립니다. (2-7, 2-8) |
| 86~87 | 두 번째 시도입니다. 성공하면 돌려줍니다. |
| 88~90 | 또 실패하면 두 번째 원인을 담아 `NeisError`를 일으킵니다. 부르는 쪽(`notifier`)이 잡습니다. |

### 3-3. `app/auth.py` (바뀐 부분)

```python
class SlackAuthError(Exception):
    # Slack 토큰을 새로 발급받지 못했을 때 일으키는 오류
    pass
```

```python
def refresh_and_save() -> str:
    tokens = load_tokens()
    response_body = refresh_access_token(tokens["refresh_token"])
    if not response_body["ok"]:
        logger.error(f"Slack 토큰 재발급 실패: 오류 코드 {response_body['error']}")
        raise SlackAuthError("Slack 토큰을 새로 발급받지 못했습니다.")
    save_token_response(response_body)
    logger.info("Slack 토큰을 새로 발급받아 저장했습니다.")
    return response_body["access_token"]
```

| 부분 | 설명 |
| --- | --- |
| 함수로 분리 | 4단계에서는 `get_access_token` 안에 있던 재발급 코드입니다. 보내다가 토큰 오류가 났을 때(`sender.py`)도 쓰려고 함수로 뺐습니다. |
| `if not response_body["ok"]:` | 재발급이 실패하면 오류 코드를 로그에 남기고 `SlackAuthError`를 일으킵니다. 그러면 망가진 응답으로 토큰 파일을 덮어쓰지 않습니다. |
| `logger.info(...)` | 토큰 값은 쓰지 않고 "발급받았다"는 사실만 남깁니다. |

`get_access_token`은 만료가 가까우면 `return refresh_and_save()`를 합니다.

### 3-4. `app/sender.py` (바뀐 부분)

**`send_once` — 한 번 보내 보기**

4단계의 `post_message` 내용을 옮기고, 요청을 `try`로 감쌌습니다.
인터넷 연결 실패 등으로 요청이 안 되면 `{"ok": False, "error": "request_failed"}`를 돌려줍니다. (2-9)

**`needs_new_token`** — 2-5 참고.

**`post_message` — 토큰 오류면 새 토큰으로 한 번 더**

```python
    try:
        response_body = send_once(channel_id, text, get_access_token())
        if needs_new_token(response_body):
            logger.warning(f"Slack 토큰 오류({response_body['error']}): 새 토큰으로 다시 보냅니다.")
            response_body = send_once(channel_id, text, refresh_and_save())
    except (SlackAuthError, OSError, requests.RequestException, ValueError, KeyError) as error:
        logger.error(f"Slack 토큰을 준비하지 못했습니다: {type(error).__name__}")
        return {"ok": False, "error": "token_unavailable"}

    if response_body["ok"]:
        logger.info(f"Slack 전송 성공: 채널 {channel_id}")
    else:
        logger.error(f"Slack 전송 실패: 채널 {channel_id}, 오류 코드 {response_body['error']}")
    return response_body
```

| 부분 | 설명 |
| --- | --- |
| 첫 `send_once` | 지금 토큰으로 보냅니다. |
| `if needs_new_token(...)` | 토큰 오류(`token_expired`, `invalid_auth`)면 새 토큰을 받아 한 번 더 보냅니다. CLAUDE.md "Access Token 만료 → 새 토큰을 발급받아 요청을 다시 보냄" |
| `except (...)` | 토큰 파일이 없거나(`FileNotFoundError`는 `OSError`의 한 종류), 재발급이 실패하면 여기로 옵니다. |
| 마지막 `if`/`else` | 결과를 로그에 남깁니다. 채널 ID는 비밀값이 아니라서 남깁니다. |

### 3-5. `app/notifier.py` (새 파일)

**`notify_admin` — 관리자 채널로 알리기**

```python
def notify_admin(problem: str) -> None:
    response_body = post_message(SLACK_ADMIN_CHANNEL_ID, ADMIN_ALERT_TITLE + "\n" + problem)
    if not response_body["ok"]:
        # 관리자 채널로도 보내지 못하면 로그 파일이 유일한 기록이다.
        logger.error("관리자 오류 알림도 보내지 못했습니다. 로그 파일을 확인하세요.")
```

**`send_lunch_notification` — 급식 알림 한 번 전체**

| 순서 | 하는 일 | 실패하면 |
| --- | --- | --- |
| 1 | `fetch_meals`로 NEIS 조회 (안에서 실패 시 한 번 재시도) | `NeisError`를 잡아 로그 → 관리자 알림 → `False` |
| 2 | `format_lunch_message`로 메시지 만들기 | (3단계, 실패할 일 없음) |
| 3 | `post_message`로 급식 알림 채널에 보내기 (안에서 토큰 오류 시 한 번 재전송) | `ok`가 `False`면 관리자 알림 → `False` |
| 4 | 성공을 로그에 남기고 `True` | |

정기 알림(9단계 스케줄러)과 `send_lunch_message.py`가 이 함수를 함께 씁니다.

### 3-6. `send_lunch_message.py` (바뀜)

```python
from app.notifier import send_lunch_notification

meal_date = input("날짜를 YYYYMMDD 형식으로 입력하세요 (예: 20261105): ")
if send_lunch_notification(meal_date):
    print("급식 알림을 보냈습니다.")
else:
    print("급식 알림을 보내지 못했습니다. 관리자 채널과 logs/bot.log를 확인하세요.")
```

4단계에서 직접 하던 조회·변환·전송을 `send_lunch_notification` 하나로 바꿨습니다.

### 3-7. 테스트 (새 파일 두 개)

- `tests/test_neis.py`: 세 가지 응답 모양(정상, 데이터 없음, 인증키 오류)에서 `get_result`가 결과를 바르게 꺼내는지 봅니다. `INFO-200`은 쓸 수 있고 `ERROR-290`은 쓸 수 없는지도 확인합니다.
- `tests/test_sender.py`: `needs_new_token`이 토큰 오류에서만 `True`인지 봅니다. 성공 응답(`error` 키 없음)에서도 오류가 나지 않는지 확인합니다. (2-5)

---

## 4. 사용한 라이브러리

| 라이브러리 | 이번에 쓴 것 | 뜻 |
| --- | --- | --- |
| logging (표준) | `getLogger(이름)`, `setLevel(logging.INFO)`, `FileHandler(파일, encoding=)`, `Formatter(모양)`, `addHandler`, `info`/`warning`/`error` | 로그를 파일에 남깁니다. (2-7) |
| time (표준) | `time.sleep(초)` | 기다립니다. (2-8) |
| requests | `requests.RequestException` | requests에서 나는 오류들의 공통 종류입니다. 연결 실패(`ConnectionError`), 시간 초과(`Timeout`)가 모두 여기에 속합니다. |
| (기본 기능) | `type(값)`, `.__name__` | 값의 종류와 그 이름입니다. (2-3) |

---

## 5. 용어 정리

| 용어 | 쉬운 뜻 | 예시 |
| --- | --- | --- |
| 예외 | 실행 중에 생긴 오류 | `KeyError`, `NeisError` |
| `try`/`except` | 오류가 나도 멈추지 않고 정해 둔 처리를 하게 하는 문법 | 2-1 |
| `raise` | 오류를 직접 일으키는 문법 | `raise NeisError(...)` |
| `class` | 새로운 종류(타입)를 만드는 문법 | `class NeisError(Exception):` |
| `pass` | 비워 둘 수 없는 블록에 "내용 없음"을 표시 | `pass` |
| `from None` | 원래 오류를 함께 보여 주지 않게 함 | 2-4 |
| 단락 평가 | `and` 앞이 거짓이면 뒤를 계산하지 않는 것 | 2-5 |
| 로그 | 프로그램이 한 일을 시각과 함께 적은 기록 | `logs/bot.log` |
| 로그 등급 | 기록의 중요도 | `INFO`, `WARNING`, `ERROR` |
| 재시도 | 실패하면 한 번 더 해 보는 것 | NEIS 3초 뒤 재시도 |
| `OSError` | 파일 같은 운영체제 작업의 오류. `FileNotFoundError`가 여기에 속함 | 토큰 파일 없음 |

---

## 6. 개발자 질문

**질문: 급식 불러오기 실패한 이유가 뭐야?** (관리자 채널에 오류 알림이 온 것을 보고)

그 알림은 에이전트가 **일부러 만든 시험** 때문에 갔습니다.

- 5단계 시험 B에서 "NEIS가 오류를 돌려줄 때 관리자에게 알림이 가는지" 확인하려고, **그 한 번의 실행에만** 인증키를 틀린 값으로 바꿨습니다. `.env`의 진짜 인증키는 바꾸지 않았습니다.
- NEIS는 두 번 모두 `ERROR-290`(인증키가 유효하지 않습니다)을 돌려줬습니다. 그래서 3초 뒤 재시도한 뒤 관리자 채널로 알림을 보냈습니다.
- 바로 앞의 시험 A는 진짜 인증키로 실행했고 성공했습니다. 진짜 설정은 정상입니다.

**이 질문으로 고친 것**

그때 알림에는 "원인은 logs/bot.log에 있습니다"라고만 적혀 있었습니다. 그래서 원인을 알려면 로그 파일을 열어야 했습니다.

그래서 `NeisError`가 원인을 담아 전달되도록 고쳤습니다. (2-2) 지금은 알림에 원인이 바로 보입니다.

```
[급식 봇 오류 알림]
20261106 급식 정보를 NEIS에서 받지 못했습니다.
NEIS mealServiceDietInfo 호출이 두 번 모두 실패했습니다. 원인: ERROR-290 인증키가 유효하지 않습니다. 인증키가 없는 경우, 홈페이지에서 인증키를 신청하십시오.
```

알림에 오류 코드가 보이면 개발 기록 2단계의 결과 코드 표(`docs/step02-devlog.md` 6번)에서 뜻을 찾을 수 있습니다.

---

## 7. 확인 문제

### 문제 1. 코드 읽기: 이 코드의 출력은?

```python
def check(code: str) -> str:
    try:
        if code not in ["INFO-000", "INFO-200"]:
            raise ValueError(code)
        return "정상"
    except ValueError as error:
        return "오류: " + str(error)


print(check("INFO-200"))
print(check("ERROR-290"))
```

`str(값)`은 값을 문자열로 바꾸는 내장 함수입니다.

<details><summary>정답</summary>

```
정상
오류: ERROR-290
```

- `INFO-200`은 리스트 안에 있어서 `raise`하지 않고 `"정상"`을 돌려줍니다.
- `ERROR-290`은 리스트에 없어서 `ValueError`를 일으킵니다. 다음 줄 `return "정상"`은 건너뛰고 `except`로 가서 `"오류: ERROR-290"`을 돌려줍니다. (2-1)

</details>

### 문제 2. 빈칸 채우기

로그 파일 설정입니다. 빈칸을 채우세요.

```python
logger = logging.getLogger("lunch_bot")
logger.setLevel(logging.____)
file_handler = logging.____________(LOG_FILE, encoding="utf-8")
file_handler.setFormatter(logging.Formatter("%(________)s [%(levelname)s] %(message)s"))
logger.addHandler(file_handler)
```

<details><summary>정답</summary>

```python
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler(LOG_FILE, encoding="utf-8")
file_handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s"))
```

- `INFO`: info 이상 등급만 남깁니다.
- `FileHandler`: 파일에 씁니다. (화면이면 `StreamHandler`)
- `asctime`: 로그를 남긴 시각입니다. CLAUDE.md "시각과 함께"를 지키는 부분입니다.

</details>

### 문제 3. 작은 수정: 이 코드에는 보안 문제가 있습니다. 고치세요.

```python
except requests.RequestException as error:
    logger.warning(f"NEIS 호출 실패: {error}")
```

<details><summary>정답</summary>

```python
except requests.RequestException as error:
    logger.warning(f"NEIS 호출 실패: {type(error).__name__}")
```

`requests`의 오류 메시지(`{error}`)에는 인증키가 붙은 요청 주소가 들어 있습니다. 5단계에서 실제로 확인했습니다. 그대로 쓰면 인증키가 로그 파일에 남습니다.
종류 이름(`ConnectionError` 등)만 남기면 원인은 알 수 있고 인증키는 새지 않습니다. (2-3)

</details>

---

## 이번 단계 핵심 정리

1. `try`/`except 종류 as error:`로 오류를 잡으면 프로그램이 멈추지 않고 정해 둔 처리를 한다.
2. `raise NeisError("원인")`으로 직접 만든 오류를 일으켜, 원인을 부르는 쪽(관리자 알림)까지 전달한다.
3. NEIS가 실패하면 3초 뒤 한 번 다시 부르고, Slack 토큰 오류면 새 토큰으로 한 번 다시 보낸다.
4. 모든 요청과 오류를 `logging`으로 `logs/bot.log`에 시각과 함께 남긴다.
5. 외부 오류 메시지에는 인증키가 섞일 수 있으니, 종류 이름만 남기고 `from None`으로 원래 오류를 숨긴다.
