# 7단계 학습 정리: 서명 검증과 명령어 해석

## 이 문서를 다 읽으면 할 수 있게 되는 것

1. "서명"으로 요청이 진짜 Slack에서 왔는지 확인하는 원리를 설명할 수 있다.
2. 사용자가 보낸 말에서 띄어쓰기를 지우고 명령어를 고르는 코드를 설명할 수 있다.
3. 같은 이벤트를 한 번만 처리하고, 봇의 메시지는 무시하는 이유와 방법을 설명할 수 있다.

## 읽기 전에

- 코드 예시는 모두 실제로 실행한 결과를 붙였습니다. 긴 파일 경로는 `예시.py`처럼 줄여 적었습니다.
- 서명 예시에 쓴 Secret(`my-secret`, `8f742231…`)은 연습용·문서용 가짜 값입니다.
- 앞 단계에서 설명한 것은 "step05 참고"처럼 적었습니다.

---

## 1. 이번 단계에서 새로 나온 것

**개념**

1. 서명(HMAC)과 재전송 공격

**Python 문법과 라이브러리**

2. 바이트(`bytes`)와 `encode`
3. `hmac`, `hashlib`: 서명 계산과 안전한 비교
4. `int()`와 `abs()`: 숫자로 바꾸기, 차이의 크기
5. 집합(`set`)
6. `split()` + `join`으로 띄어쓰기 모두 지우기
7. 딕셔너리 타입 힌트 `dict[str, str]`와 명령어 표
8. 응답 상태 코드 정하기: `status_code=401`

**앞 단계에서 설명한 것**

- step02: 딕셔너리, `in`
- step03: `split`, `join`, `isdigit`
- step05: `and`와 단락 평가, `not in`
- step06: `await request.body()`의 친구인 `await request.json()`, `request.headers.get`

---

## 2. 하나씩 설명

### 2-1. 서명(HMAC)과 재전송 공격

**설명**

6단계 서버는 터널 주소를 아는 **누구나** 요청을 보낼 수 있었습니다. 그래서 진짜 Slack이 보낸 요청인지 확인해야 합니다.

Slack과 우리만 아는 비밀값이 **Signing Secret**입니다. Slack은 요청을 보낼 때 이 비밀값과 요청 내용으로 **서명**(짧은 확인용 글자)을 계산해 헤더에 넣어 보냅니다.
우리도 받은 내용과 같은 비밀값으로 서명을 계산해 봅니다. 두 서명이 같으면 진짜입니다.

비밀값이 없으면 맞는 서명을 만들 수 없습니다. 내용을 한 글자만 바꿔도 서명이 완전히 달라집니다.

서명이 맞아도, 예전에 가로챈 진짜 요청을 나중에 그대로 다시 보내는 공격이 있습니다. 이것을 **재전송 공격**이라고 합니다.
그래서 서명에 **시각**도 넣고, 그 시각이 지금과 5분 넘게 차이 나면 거부합니다.

**비유**

봉투에 찍는 도장입니다. 도장(Signing Secret)은 Slack과 우리만 가지고 있습니다. 편지 내용(본문)과 날짜(타임스탬프)를 함께 넣어 찍으므로, 내용을 바꾸거나 옛날 편지를 다시 내면 들통납니다.

**Slack 공식 문서의 순서** (`app/auth.py`가 그대로 따름)

| 순서 | 할 일 |
| --- | --- |
| 1 | 헤더 `X-Slack-Request-Timestamp`(보낸 시각)와 `X-Slack-Signature`(서명)를 꺼낸다 |
| 2 | 보낸 시각이 지금과 5분 넘게 차이 나면 거부한다 |
| 3 | `v0:보낸시각:원래 본문`을 만든다 |
| 4 | 3을 Signing Secret으로 HMAC-SHA256 계산하고, 16진수 결과 앞에 `v0=`을 붙인다 |
| 5 | 4와 헤더의 서명을 hmac 비교 함수로 비교한다 |

**실제로 확인한 것**

- 공식 문서의 계산 예시(문서용 Secret, 시각 `1531420618`)로 계산했더니 문서의 정답 `v0=a2114d57…`과 정확히 같았습니다. (테스트 `test_signature_matches_official_example`)
- 로컬 서버에 서명이 없는 요청, 틀린 Secret, 6분 지난 요청, 서명 후 본문을 바꾼 요청을 보냈더니 모두 `401`로 거부되었습니다. (개발 기록 4번)

**Java 비교**

```java
Mac mac = Mac.getInstance("HmacSHA256");
mac.init(new SecretKeySpec(signingSecret.getBytes(StandardCharsets.UTF_8), "HmacSHA256"));
String digest = HexFormat.of().formatHex(mac.doFinal(basestring));
boolean same = MessageDigest.isEqual(expected.getBytes(), signature.getBytes());
```

**자주 하는 실수: JSON으로 바꾼 뒤의 내용으로 서명을 계산한다**

공식 문서: "Use the raw request body ... before it has been deserialized"(JSON으로 바꾸기 전의 원래 본문을 쓴다).
딕셔너리로 바꿨다가 다시 글자로 만들면 띄어쓰기나 순서가 달라져 서명이 맞지 않습니다. 그래서 서버는 `await request.body()`로 원래 바이트를 먼저 읽습니다. (3-1)

---

### 2-2. 바이트(`bytes`)와 `encode`

**설명**

컴퓨터는 글자를 숫자(바이트)로 저장합니다. Python에서 바이트 묶음은 `bytes`라는 별도의 타입이고, 앞에 `b`를 붙여 `b"..."`로 씁니다.

`문자열.encode("utf-8")`은 문자열을 UTF-8 방식의 바이트로 바꿉니다. 한글 한 글자는 바이트 3개가 됩니다.

서명 계산(HMAC)은 문자열이 아니라 바이트를 받습니다.

**작은 예시**

```python
text = "v0:1531420618:"
data = text.encode("utf-8")
print(data)
print("급식".encode("utf-8"))
print(data + b"token=abc")
```

결과:

```
b'v0:1531420618:'
b'\xea\xb8\x89\xec\x8b\x9d'
b'v0:1531420618:token=abc'
```

**이 프로젝트 코드** (`app/auth.py` 146줄)

```python
basestring = f"{SIGNATURE_VERSION}:{timestamp}:".encode("utf-8") + body
```

`body`는 `await request.body()`로 읽은 바이트입니다. 앞부분도 바이트로 바꿔 이어 붙입니다.

**Java 비교**

Java의 `byte[]`와 `"text".getBytes(StandardCharsets.UTF_8)`입니다.

**자주 하는 실수: 바이트와 문자열을 이어 붙인다**

```python
print(b"v0:1531420618:" + "token=abc")
```

결과 (마지막 줄):

```
TypeError: can't concat str to bytes
```

둘 다 바이트이거나 둘 다 문자열이어야 이어 붙일 수 있습니다.

---

### 2-3. `hmac`, `hashlib`: 서명 계산과 안전한 비교

**설명**

`hmac.new(비밀값, 내용, hashlib.sha256)`은 비밀값으로 내용의 HMAC-SHA256 서명을 계산합니다. `.hexdigest()`는 결과를 16진수 글자(0~9, a~f)로 돌려줍니다.

`hmac.compare_digest(A, B)`는 두 글자가 같은지 비교합니다. `==`와 결과는 같습니다.
다른 점은, 어디서 달라지든 **비교에 걸리는 시간이 같다**는 것입니다.

**작은 예시**

```python
import hashlib
import hmac

digest = hmac.new(b"my-secret", b"hello", hashlib.sha256).hexdigest()
print(digest)
print(hmac.new(b"my-secret", b"hellO", hashlib.sha256).hexdigest())
print(hmac.compare_digest(digest, digest))
```

결과:

```
7c1ce32402750db1149385ac20603beeaca8909906d1e81c08f4f5c7db8fbe94
479b21fcf840653d2cf2c4c4c2f61298339ee45f8968b660d6338362821eb540
True
```

`hello`의 마지막 글자 하나만 대문자로 바꿨는데 서명이 완전히 달라졌습니다.

**이 프로젝트 코드** (`app/auth.py`)

```python
digest = hmac.new(signing_secret.encode("utf-8"), basestring, hashlib.sha256).hexdigest()
return f"{SIGNATURE_VERSION}={digest}"
...
return hmac.compare_digest(expected, signature)
```

**왜 `==` 대신 `compare_digest`인가요?**

`==`는 앞에서부터 비교하다가 다른 글자를 만나면 바로 멈춥니다. 그래서 앞부분이 많이 맞을수록 아주 조금 더 오래 걸립니다.
공격자가 이 시간 차이를 재면 서명을 한 글자씩 맞혀 갈 수 있습니다. Slack 공식 문서도 hmac 비교 함수를 쓰라고 권합니다.

**Java 비교**

`MessageDigest.isEqual(a, b)`가 같은 역할입니다.

**자주 하는 실수: `hexdigest` 대신 `digest`를 쓴다**

```python
raw = hmac.new(b"my-secret", b"hello", hashlib.sha256).digest()
print(type(raw))
print(raw[:6])
```

결과:

```
<class 'bytes'>
b'|\x1c\xe3$\x02u'
```

`digest()`는 바이트를 돌려줍니다. 헤더의 서명은 16진수 글자라서 `hexdigest()`를 써야 비교할 수 있습니다.

---

### 2-4. `int()`와 `abs()`

**설명**

`int(글자)`는 숫자 모양의 글자를 정수로 바꿉니다. 헤더 값은 늘 글자라서, 시각을 계산하려면 숫자로 바꿔야 합니다.

`abs(숫자)`는 숫자의 크기(절댓값)입니다. 빼기 결과가 음수여도 양수로 돌려줍니다. "차이가 얼마인지"만 볼 때 씁니다.

**작은 예시**

```python
now = 1531420900.5
timestamp = "1531420618"
print(int(timestamp))
print(now - int(timestamp))
print(abs(1531420618 - now))
```

결과:

```
1531420618
282.5
282.5
```

**이 프로젝트 코드** (`app/auth.py` 153~156줄)

```python
if not timestamp.isdigit():
    return False
if abs(now - int(timestamp)) > MAX_REQUEST_AGE_SECONDS:
    return False
```

보낸 시각이 5분 전이든 5분 뒤든(컴퓨터 시계가 어긋난 경우) 차이의 크기만 봅니다.

**Java 비교**

`Long.parseLong(timestamp)`, `Math.abs(...)`입니다.

**자주 하는 실수: 숫자가 아닌 글자를 `int`로 바꾼다**

```python
print("12a".isdigit())
print(int("12a"))
```

결과:

```
False
...
ValueError: invalid literal for int() with base 10: '12a'
```

헤더는 가짜 요청이 마음대로 보낼 수 있는 값입니다. 그래서 `int()` 전에 `isdigit()`로 먼저 확인합니다. 헤더가 없으면 빈 글자(`""`)인데, `"".isdigit()`도 `False`라서 함께 걸러집니다. (step03 참고)

---

### 2-5. 집합(`set`)

**설명**

집합은 **겹치지 않는** 값을 모아 두는 상자입니다. 같은 값을 여러 번 넣어도 하나만 남습니다. 순서는 정해져 있지 않습니다.

- `set()`: 빈 집합
- `집합.add(값)`: 넣기
- `값 in 집합`: 들어 있는지 확인. 리스트보다 훨씬 빨리 찾습니다.

**비유**

출석부의 도장 칸입니다. 이미 도장이 찍힌 사람(처리한 이벤트)인지 바로 알 수 있습니다.

**작은 예시**

```python
seen = set()
seen.add("Ev001")
seen.add("Ev001")
seen.add("Ev002")
print(seen)
print("Ev001" in seen)
print(len(seen))
```

결과:

```
{'Ev001', 'Ev002'}
True
2
```

`len`은 개수를 세는 내장 함수입니다. `Ev001`을 두 번 넣었지만 하나만 남았습니다.

**이 프로젝트 코드** (`app/server.py` 27~34줄)

```python
processed_event_ids: set[str] = set()


def is_duplicate_event(event_id: str) -> bool:
    if event_id in processed_event_ids:
        return True
    processed_event_ids.add(event_id)
    return False
```

처음 본 이벤트 ID면 기억해 두고 `False`, 이미 본 것이면 `True`를 돌려줍니다.
CLAUDE.md 예외 처리: "콜백 중복 수신 → 응답을 바로 돌려주고, 같은 메시지는 한 번만 처리"

**Java 비교**

`Set<String> processed = new HashSet<>();`, `processed.add(id)`, `processed.contains(id)`입니다.

**자주 하는 실수: `{}`로 빈 집합을 만든다**

```python
seen = {}
print(type(seen))
seen.add("Ev001")
```

결과:

```
<class 'dict'>
...
AttributeError: 'dict' object has no attribute 'add'
```

`{}`는 빈 **딕셔너리**입니다. 빈 집합은 `set()`으로 만듭니다.

---

### 2-6. `split()` + `join`으로 띄어쓰기 모두 지우기

**설명**

`문자열.split()`처럼 괄호 안을 비우면 빈칸, 탭, 줄바꿈을 **모두** 기준으로 자르고, 빈 조각은 버립니다. (step03에서는 `<br/>`처럼 구분자를 정해서 잘랐습니다.)

그 조각들을 `"".join(...)`으로 사이에 아무것도 넣지 않고 이으면, 띄어쓰기가 모두 사라집니다.

**작은 예시**

```python
text = "  내일   급식 \n"
print(text.split())
print("".join(text.split()))
```

결과:

```
['내일', '급식']
내일급식
```

**이 프로젝트 코드** (`app/commands.py`)

```python
def remove_spaces(text: str) -> str:
    return "".join(text.split())
```

CLAUDE.md 규칙 "앞뒤 공백과 띄어쓰기 차이는 무시한다(`내일급식` = `내일 급식`)"를 이 한 줄로 지킵니다.

**Java 비교**

`text.replaceAll("\\s+", "")`과 같은 결과입니다.

**자주 하는 실수: `replace(" ", "")`만 쓴다**

```python
text = "내일\t급식\n"
print(repr(text.replace(" ", "")))
print(repr("".join(text.split())))
```

결과:

```
'내일\t급식\n'
'내일급식'
```

`replace(" ", "")`는 빈칸만 지웁니다. 탭(`\t`)과 줄바꿈(`\n`)은 남습니다. `repr`은 이런 보이지 않는 글자까지 보여 주는 내장 함수입니다. 이 예시에서만 씁니다.

---

### 2-7. 딕셔너리 타입 힌트 `dict[str, str]`와 명령어 표

**설명**

`dict[str, str]`은 "키도 문자열, 값도 문자열인 딕셔너리"라는 타입 힌트입니다. (`list[str]`은 step03 참고)

명령어는 "사용자가 보내는 말 → 명령어 이름"을 표로 만들어 두고, 표에서 찾습니다.

**작은 예시**

```python
COMMANDS: dict[str, str] = {"오늘급식": "today_lunch", "내일급식": "tomorrow_lunch"}
print(COMMANDS["내일급식"])
print("모레급식" in COMMANDS)
```

결과:

```
tomorrow_lunch
False
```

**이 프로젝트 코드** (`app/commands.py`)

```python
COMMANDS: dict[str, str] = {
    "오늘급식": TODAY_LUNCH,
    "내일급식": TOMORROW_LUNCH,
    "이번주일정": THIS_WEEK_SCHEDULE,
    "도움말": HELP,
}


def parse_command(text: str) -> str:
    key = remove_spaces(text)
    if key in COMMANDS:
        return COMMANDS[key]
    # 목록에 없는 말은 도움말로 답한다. (CLAUDE.md: "도움말 또는 그 밖의 말")
    return HELP
```

- 표의 키는 **띄어쓰기를 지운 모양**으로 적어 둡니다. 들어온 말도 띄어쓰기를 지운 뒤 찾으므로 서로 맞습니다.
- 명령어 이름(`TODAY_LUNCH` 등)은 상수로 만들어 둡니다. `"today_lunch"`를 여러 곳에 직접 쓰다가 오타가 나는 일을 막습니다.

**Java 비교**

```java
static final Map<String, String> COMMANDS = Map.of("오늘급식", TODAY_LUNCH, ...);
return COMMANDS.getOrDefault(removeSpaces(text), HELP);
```

**자주 하는 실수: 표의 키에 띄어쓰기를 넣는다**

`{"오늘 급식": TODAY_LUNCH}`처럼 적으면, 띄어쓰기를 지운 `"오늘급식"`으로 찾을 때 찾지 못하고 늘 도움말이 나옵니다. 표와 찾는 값을 같은 모양으로 맞춰야 합니다.

---

### 2-8. 응답 상태 코드 정하기: `status_code=401`

**설명**

`PlainTextResponse("글자", status_code=번호)`로 응답의 상태 코드를 정합니다. 정하지 않으면 200(정상)입니다.

`401`은 "인증되지 않음"이라는 뜻입니다. 서명이 맞지 않는 요청에 돌려줍니다. Slack 공식 문서는 거부할 때 어떤 번호를 쓸지는 정하지 않았습니다. 그래서 뜻이 가장 가까운 401을 골랐습니다.

**이 프로젝트 코드** (`app/server.py` 50~53줄)

```python
if not is_valid_slack_request(SLACK_SIGNING_SECRET, timestamp, signature, body, time.time()):
    # CLAUDE.md 규칙: 서명이 맞지 않는 콜백은 거부하고 로그에 기록한다.
    logger.warning("서명이 맞지 않는 요청을 거부했습니다.")
    return PlainTextResponse("invalid signature", status_code=401)
```

**Java 비교**

`ResponseEntity.status(HttpStatus.UNAUTHORIZED).body("invalid signature")`입니다.

**자주 하는 실수: 거부하면서 200을 돌려준다**

200을 돌려주면 받은 쪽은 성공으로 압니다. 거부했다면 그 뜻의 상태 코드를 돌려줘야, 나중에 기록을 볼 때도 바로 구별됩니다.

---

## 3. 코드 줄 단위 해설

### 3-1. `app/server.py` (바뀐 부분)

**27~34줄: 중복 확인** — 2-5 참고.

**37~41줄: 사람이 보낸 새 메시지인가?**

```python
def is_user_message(event: dict) -> bool:
    return event.get("type") == "message" and "bot_id" not in event and "subtype" not in event
```

| 조건 | 이유 (Slack 공식 문서) |
| --- | --- |
| `type`이 `"message"` | 메시지 이벤트만 다룬다 |
| `bot_id`가 없다 | 요즘 앱이 보낸 메시지에는 `bot_id`가 붙는다. 8단계에서 봇이 답장하면 그 답장도 이벤트로 올 수 있다. 무시하지 않으면 봇이 자기 답장에 또 답하며 끝없이 반복한다 |
| `subtype`이 없다 | 메시지 수정(`message_changed`), 삭제(`message_deleted`) 등에는 `subtype`이 붙는다 |

공식 문서에 "subtype이 없으면 사람 메시지"라고 그대로 쓰여 있지는 않습니다. 문서의 subtype 목록과 봇 메시지 설명을 바탕으로 이 프로젝트가 정한 기준입니다.

**44~53줄: 서명 확인을 가장 먼저**

| 줄 | 설명 |
| --- | --- |
| 47 | `await request.body()`로 원래 본문을 **바이트**로 읽습니다. (2-1, 2-2) |
| 48~49 | 보낸 시각과 서명 헤더를 꺼냅니다. 없으면 빈 글자입니다. |
| 50~53 | 서명이 맞지 않으면 로그를 남기고 401로 거부합니다. 아래 코드는 실행되지 않습니다. (2-8) |

주소 확인 요청(`url_verification`)도 서명을 확인한 **뒤에** 처리합니다. Slack 공식 문서도 "요청이 진짜인지 확인한 뒤 challenge로 응답하라"고 합니다.

**55줄: `payload = json.loads(body)`**

6단계의 `await request.json()` 대신, 이미 읽은 바이트를 `json.loads`로 딕셔너리로 바꿉니다. (step02 참고)

**66~80줄: 이벤트 처리**

| 줄 | 설명 |
| --- | --- |
| 67~68 | 이벤트와 이벤트 ID를 꺼냅니다. |
| 69~72 | 이미 처리한 이벤트면 로그만 남기고 바로 200을 돌려줍니다. |
| 74~78 | 사람이 보낸 새 메시지면 명령어로 해석해 출력하고, 로그에는 명령어 이름만 남깁니다. |
| 79~80 | 그 밖의 메시지(봇, 수정 등)는 건너뛰었다고 로그에 남깁니다. |

### 3-2. `app/auth.py` (추가된 부분)

| 줄 | 코드 | 설명 |
| --- | --- | --- |
| 33 | `SIGNATURE_VERSION: str = "v0"` | 서명 방식의 버전. 공식 문서가 정한 값입니다. |
| 36 | `MAX_REQUEST_AGE_SECONDS: int = 60 * 5` | 5분(300초). `60 * 5`로 써서 "5분"이 바로 보이게 했습니다. |
| 143~148 | `make_slack_signature` | `v0:시각:본문`을 만들어 서명을 계산합니다. (2-2, 2-3) |
| 151~160 | `is_valid_slack_request` | 시각 확인(2-4) → 서명 계산 → 안전한 비교(2-3) 순서입니다. |

두 함수 모두 Signing Secret과 지금 시각을 **매개변수로 받습니다.** 그래서 테스트에서 공식 문서의 예시 Secret과 예시 시각을 넣어 정답과 비교할 수 있습니다.

### 3-3. `app/commands.py` (새 파일)

| 줄 | 설명 |
| --- | --- |
| 7~10 | 명령어 이름 상수 네 개입니다. (2-7) |
| 13~18 | "띄어쓰기 없는 말 → 명령어 이름" 표입니다. |
| 21~23 | `remove_spaces`: 띄어쓰기를 모두 지웁니다. (2-6) |
| 26~31 | `parse_command`: 표에 있으면 그 명령어, 없으면 도움말입니다. |

### 3-4. 테스트 (새 파일 두 개, 15개)

- `tests/test_signature.py` (6개)
  - 공식 문서 예시와 정답이 같은지 확인합니다.
  - 정상 요청은 통과하는지 확인합니다.
  - 본문 변경, 틀린 Secret, 5분 넘게 지난 요청, 헤더 없음은 거부하는지 확인합니다.
- `tests/test_commands.py` (9개)
  - 명령어 해석: 띄어쓰기, 줄바꿈, 그 밖의 말을 확인합니다.
  - 사람 메시지와 봇·수정 메시지를 구별하는지 확인합니다.
  - 같은 이벤트 ID는 두 번째부터 중복으로 보는지 확인합니다.

---

## 4. 사용한 라이브러리

| 라이브러리 | 종류 | 이번에 쓴 것 | 뜻 |
| --- | --- | --- | --- |
| hmac | 표준 | `hmac.new(비밀값, 내용, hashlib.sha256)`, `.hexdigest()`, `hmac.compare_digest(A, B)` | 서명을 계산하고 안전하게 비교합니다. |
| hashlib | 표준 | `hashlib.sha256` | 서명 계산에 쓸 방식(SHA-256)입니다. |
| json | 표준 | `json.loads(바이트)` | 원래 본문을 딕셔너리로 바꿉니다. |
| time | 표준 | `time.time()` | 지금 시각입니다. 서명 시각과 비교합니다. |
| FastAPI | 따로 설치 | `await request.body()`, `PlainTextResponse(..., status_code=401)` | 원래 본문 읽기, 상태 코드 정하기 |
| (기본 기능) | 내장 | `int()`, `abs()`, `set()`, `len()`, `repr()` | 정수로 바꾸기, 절댓값, 집합, 개수, 보이지 않는 글자까지 보이기 |

---

## 5. 용어 정리

| 용어 | 쉬운 뜻 | 예시 |
| --- | --- | --- |
| 서명 | 비밀값과 내용으로 계산한 확인용 글자 | `v0=a2114d57…` |
| HMAC | 비밀값을 넣어 서명을 계산하는 방법 | HMAC-SHA256 |
| Signing Secret | Slack과 우리만 아는 서명용 비밀값 | `.env`의 `SLACK_SIGNING_SECRET` |
| 재전송 공격 | 예전의 진짜 요청을 가로채 나중에 다시 보내는 공격 | 5분 넘은 요청 거부로 막음 |
| 바이트 | 컴퓨터가 글자를 저장하는 숫자 묶음 | `b"v0:"` |
| 인코딩 | 문자열을 바이트로 바꾸는 방식 | `encode("utf-8")` |
| 16진수 | 0~9와 a~f로 쓰는 숫자 표기 | `7c1ce324…` |
| 절댓값 | 음수든 양수든 크기만 본 값 | `abs(-282.5)` → `282.5` |
| 집합 | 겹치지 않는 값을 모으는 상자 | `set()` |
| 중복 수신 | 같은 이벤트를 여러 번 받는 것 | Slack 재전송 |
| 401 | "인증되지 않음" 상태 코드 | 서명이 틀린 요청 |

---

## 6. 확인 문제

### 문제 1. 코드 읽기: 출력은?

```python
print(parse_command(" 오늘  급식 "))
print(parse_command("오늘의 급식"))
print(parse_command("이번 주일정"))
```

<details><summary>정답</summary>

```
today_lunch
help
this_week_schedule
```

- 띄어쓰기를 모두 지우면 `오늘급식`, `오늘의급식`, `이번주일정`이 됩니다.
- `오늘의급식`은 표에 없어서 도움말(`help`)입니다. 띄어쓰기만 무시할 뿐, 글자가 다르면 다른 말입니다.

</details>

### 문제 2. 빈칸 채우기

```python
def is_valid_slack_request(signing_secret: str, timestamp: str, signature: str, body: bytes, now: float) -> bool:
    if not timestamp.isdigit():
        return False
    if ___(now - int(timestamp)) > MAX_REQUEST_AGE_SECONDS:
        return False
    expected = make_slack_signature(signing_secret, timestamp, body)
    return hmac.______________(expected, signature)
```

<details><summary>정답</summary>

- `abs`: 시각 차이의 크기만 봅니다. (2-4)
- `compare_digest`: 비교 시간이 일정한 안전한 비교입니다. `==`를 쓰면 결과는 같아도 시간 차이로 공격받을 수 있습니다. (2-3)

</details>

### 문제 3. 작은 수정: 이 코드는 서명이 늘 맞지 않습니다. 고치세요.

```python
@app.post("/slack/events")
async def receive_slack_event(request: Request) -> PlainTextResponse:
    payload = await request.json()
    body = json.dumps(payload).encode("utf-8")
    ...
```

<details><summary>정답</summary>

```python
    body = await request.body()
    ...
    payload = json.loads(body)
```

서명은 Slack이 보낸 **원래 본문 그대로**로 계산해야 합니다. 딕셔너리로 바꿨다가 `json.dumps`로 다시 만들면 띄어쓰기, 한글 표현(`\uXXXX`) 등이 달라져 서명이 맞지 않습니다. (2-1)

</details>

---

## 이번 단계 핵심 정리

1. Slack의 서명(`v0=` + HMAC-SHA256)을 원래 본문으로 다시 계산해 비교하고, 다르면 401로 거부한다.
2. 보낸 시각이 5분 넘게 차이 나면 서명이 맞아도 거부한다(재전송 공격 방지).
3. 서명은 바이트로 계산하고(`encode`), `hmac.compare_digest`로 안전하게 비교한다.
4. 같은 `event_id`는 집합(`set`)에 기억해 한 번만 처리하고, 봇·수정 메시지는 무시한다.
5. 명령어는 띄어쓰기를 모두 지운 뒤 표(`dict[str, str]`)에서 찾고, 없으면 도움말이다.
