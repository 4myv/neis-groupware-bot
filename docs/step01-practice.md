# 1단계 실습 과제: Python 파일 실행, 변수, `if`, 환경 변수

## 이 문서를 다 풀면 할 수 있게 되는 것

1. Python 파일을 직접 만들고 `python 파일명.py`로 실행할 수 있다.
2. 오류 메시지를 읽고, 콜론·들여쓰기·따옴표·`==` 실수를 스스로 고칠 수 있다.
3. 환경 변수와 `.env` 값을 읽고, 값이 없을 때(`""`, `None`)를 구별할 수 있다.

## 시작하기 전에

- 함께 볼 문서: [`step01-learning.md`](step01-learning.md)
- 실습 파일은 프로젝트 맨 위 폴더 아래 `practice\step01\` 폴더에 만듭니다. 프로젝트 코드(`app\` 폴더)는 고치지 않습니다.
  - 폴더 만들기(PowerShell): `New-Item -ItemType Directory -Force practice\step01`
- 실행은 늘 **가상환경을 켠 상태**에서, **프로젝트 맨 위 폴더**(`C:\neis_groupware_bot`)에서 합니다.
  ```powershell
  cd C:\neis_groupware_bot
  .venv\Scripts\Activate.ps1
  python practice\step01\p1_hello.py
  ```
- 각 과제의 **확인 방법**에 적힌 결과와 똑같이 나오면 성공입니다. 결과는 모두 실제로 실행해 확인했습니다.
- 힌트와 정답은 접어 두었습니다. 먼저 직접 해 보고 펼쳐 보세요.
- 인증키 같은 비밀값은 실습에서도 화면에 출력하지 않습니다.

---

## 과제 1. 내 첫 Python 파일 (★)

**다지는 개념**: Python 파일과 실행(2-1), `print`(2-6), 주석(2-7)

**할 일**

1. `practice\step01\p1_hello.py` 파일을 만듭니다.
2. 맨 위에 주석 한 줄을 씁니다. (무슨 파일인지)
3. 아래 결과가 나오도록 `print`를 세 번 씁니다. 두 번째와 세 번째 줄은 **쉼표**로 값 두 개를 넣어 출력합니다.
4. `python practice\step01\p1_hello.py`로 실행합니다.

**확인 방법**

```
안녕하세요
이름: 급식봇
단계: 1
```

<details><summary>힌트</summary>

- `print`에 쉼표로 값을 두 개 넣으면, 사이에 빈칸이 하나 들어갑니다.
- `1`은 숫자라서 따옴표 없이 써도 됩니다.

</details>

<details><summary>정답 예시</summary>

```python
# 내가 만든 첫 실습 파일
print("안녕하세요")
print("이름:", "급식봇")
print("단계:", 1)
```

- `#` 뒤는 주석이라 실행되지 않습니다.
- 문장 끝에 세미콜론 `;`을 쓰지 않습니다.

</details>

---

## 과제 2. 가상환경과 pip 확인하기 (★)

**다지는 개념**: 가상환경(2-2), pip(2-3), requirements.txt(2-4)

**할 일**

1. 가상환경을 켠 뒤 `python check_setup.py`를 실행합니다. `Python 위치:` 줄에 `.venv`가 들어 있는지 봅니다.
2. `python -m pip show requests`를 실행합니다. `Version:` 줄을 찾습니다.
3. `requirements.txt`를 열어 `requests==` 뒤의 숫자와 2의 버전이 같은지 비교합니다.
4. 가상환경을 끄고(`deactivate`) 1을 다시 실행해 봅니다. `Python 위치:`가 어떻게 바뀌는지 봅니다. 끝나면 다시 켭니다.

**확인 방법** (이 프로젝트의 컴퓨터에서 실행한 결과)

1의 결과:

```
Python 버전: 3.13.16 (tags/v3.13.16:cbc944f, Sep 30 2026, 19:17:50) [MSC v.1944 64 bit (AMD64)]
Python 위치: C:\neis_groupware_bot\.venv\Scripts\python.exe
NEIS_API_KEY: 입력됨
```

2의 결과 (앞 두 줄):

```
Name: requests
Version: 2.34.2
```

- `requirements.txt`의 `requests==2.34.2`와 같습니다.
- 4에서는 `python` 명령이 동작하지 않거나(1단계 개발 기록 문제 1), `.venv`가 없는 위치가 나옵니다.

<details><summary>정답 설명</summary>

- 가상환경을 켜면 `python`이 `.venv\Scripts\python.exe`를 가리킵니다. 그래서 프로젝트 전용 라이브러리를 씁니다.
- `pip show 이름`은 설치된 라이브러리의 이름, 버전, 설명을 보여 줍니다.
- `requirements.txt`에 버전을 고정해 두었기 때문에, 언제 설치해도 같은 버전이 깔립니다.

</details>

---

## 과제 3. 상수, 변수, 타입 힌트, `if` / `else` (★★)

**다지는 개념**: 변수(2-8), 타입 힌트(2-9), `if` / `else`(2-10), `==`(2-11), 상수(2-15)

**할 일**

`practice\step01\p3_dishes.py`를 만듭니다.

1. 바뀌지 않는 값 `MAX_DISHES`(정수 7)를 **상수 이름 관례**로 만듭니다.
2. 변수 `school_name`(문자열 `"서울고등학교"`)과 `dish_count`(정수 6)를 만듭니다.
3. 세 이름 모두 **타입 힌트**를 붙입니다.
4. 학교와 메뉴 수를 출력합니다.
5. `dish_count`가 `MAX_DISHES`와 같으면 `메뉴가 가득 찼습니다`, 아니면 `메뉴를 더 넣을 수 있습니다`를 출력합니다.

**확인 방법**

```
학교: 서울고등학교
메뉴 수: 6
메뉴를 더 넣을 수 있습니다
```

**더 해 보기**: `dish_count`를 7로 바꾸면 마지막 줄이 `메뉴가 가득 찼습니다`로 바뀌는지 확인합니다.

<details><summary>힌트</summary>

- 상수는 이름을 모두 대문자로 씁니다.
- 타입 힌트: 문자열은 `str`, 정수는 `int`입니다. 모양은 `이름: 타입 = 값`입니다.
- 비교는 `==`(등호 두 개), 값 넣기는 `=`(등호 하나)입니다.

</details>

<details><summary>정답 예시</summary>

```python
# 상수, 변수, 타입 힌트, if / else 연습
MAX_DISHES: int = 7

school_name: str = "서울고등학교"
dish_count: int = 6

print("학교:", school_name)
print("메뉴 수:", dish_count)
if dish_count == MAX_DISHES:
    print("메뉴가 가득 찼습니다")
else:
    print("메뉴를 더 넣을 수 있습니다")
```

- `if` 줄과 `else` 줄 끝에는 콜론 `:`이 있습니다.
- `if`, `else` 아래 줄은 빈칸 4개로 들여씁니다. Python은 중괄호 `{}` 대신 들여쓰기로 블록을 나눕니다.

</details>

---

## 과제 4. 오류 메시지를 읽고 고치기 (★★)

**다지는 개념**: `if` / `else`와 들여쓰기(2-10), `==`(2-11), 문자열(2-6)

**할 일**

아래 코드를 `practice\step01\p4_fix.py`로 저장하고 실행합니다. 실수가 **네 군데** 있습니다.

```python
school_code = "7010083"
if school_code = "7010083"
    print(학교 코드가 맞습니다)
else:
print("학교 코드가 다릅니다")
```

Python은 오류를 **한 번에 하나씩** 알려 줍니다. 오류 메시지 맨 아래 줄을 읽고 → 한 곳을 고치고 → 다시 실행하기를 반복합니다.

**확인 방법**

고치는 동안 차례로 만나는 오류 (실제 실행 결과, 파일 경로는 줄임):

```
  File "practice\step01\p4_fix.py", line 2
    if school_code = "7010083"
       ^^^^^^^^^^^^^^^^^^^^^^^
SyntaxError: invalid syntax. Maybe you meant '==' or ':=' instead of '='?
```

```
  File "practice\step01\p4_fix.py", line 2
    if school_code == "7010083"
                               ^
SyntaxError: expected ':'
```

```
  File "practice\step01\p4_fix.py", line 3
    print(학교 코드가 맞습니다)
          ^^^^^^
SyntaxError: invalid syntax. Perhaps you forgot a comma?
```

```
  File "practice\step01\p4_fix.py", line 5
    print("학교 코드가 다릅니다")
    ^^^^^
IndentationError: expected an indented block after 'else' statement on line 4
```

모두 고치면:

```
학교 코드가 맞습니다
```

<details><summary>정답 예시</summary>

```python
school_code = "7010083"
if school_code == "7010083":
    print("학교 코드가 맞습니다")
else:
    print("학교 코드가 다릅니다")
```

| 줄 | 실수 | 고친 것 |
| --- | --- | --- |
| 2 | 비교에 `=`를 씀 | `==` |
| 2 | 끝에 콜론이 없음 | `:` |
| 3 | 글자에 따옴표가 없음 | `"학교 코드가 맞습니다"` |
| 5 | `else` 아래 줄을 들여쓰지 않음 | 빈칸 4개 |

- 3번째 오류는 "쉼표를 잊었나요?"라고 묻지만, 진짜 원인은 따옴표가 없는 것입니다. 오류 메시지는 **힌트**이지 정답이 아닐 때도 있습니다.

</details>

---

## 과제 5. 환경 변수와 `None` (★★★)

**다지는 개념**: `.env`와 환경 변수(2-5), `import`(2-12), `None`(2-14)

**할 일**

`practice\step01\p5_env.py`를 만듭니다.

1. `os`를 가져옵니다.
2. 환경 변수 `PRACTICE_NAME`을 **기본값 `""`** 으로 읽어 `PRACTICE_NAME` 상수에 넣습니다. (타입 힌트 포함)
3. 비어 있으면 `PRACTICE_NAME이 비어 있습니다`, 아니면 `PRACTICE_NAME: (값)`을 출력합니다.
4. 마지막 줄에 `기본값 없이 읽으면:`과 함께, 같은 환경 변수를 **기본값 없이** 읽은 값을 출력합니다.
5. 두 번 실행합니다.
   - 처음: 그대로 실행
   - 두 번째: PowerShell에서 `$env:PRACTICE_NAME = "급식봇"`을 먼저 입력한 뒤 실행

**확인 방법**

처음:

```
PRACTICE_NAME이 비어 있습니다
기본값 없이 읽으면: None
```

`$env:PRACTICE_NAME = "급식봇"` 뒤:

```
PRACTICE_NAME: 급식봇
기본값 없이 읽으면: 급식봇
```

`$env:...`로 넣은 값은 **그 PowerShell 창에서만** 유지됩니다. 창을 닫으면 사라집니다. `.env` 파일은 이 값을 파일에 적어 두고 프로그램이 시작할 때 읽어 오는 방법입니다.

<details><summary>힌트</summary>

- `os.getenv("이름", "")`: 없으면 `""`
- `os.getenv("이름")`: 없으면 `None`

</details>

<details><summary>정답 예시</summary>

```python
# 환경 변수 읽기와 None 연습
import os

PRACTICE_NAME: str = os.getenv("PRACTICE_NAME", "")

if PRACTICE_NAME == "":
    print("PRACTICE_NAME이 비어 있습니다")
else:
    print("PRACTICE_NAME:", PRACTICE_NAME)

print("기본값 없이 읽으면:", os.getenv("PRACTICE_NAME"))
```

- `app/config.py`가 늘 기본값 `""`를 주는 이유: `None`에 문자열을 이어 붙이면 오류가 나기 때문입니다. (2-14 자주 하는 실수)

</details>

---

## 과제 6. 도전: 프로젝트 설정을 안전하게 확인하기 (★★★)

**다지는 개념**: `from ... import`(2-12), 패키지(2-13), 비밀값을 출력하지 않기

**할 일**

`practice\step01\p6_config_check.py`를 만듭니다.

1. `app.config`에서 `NEIS_API_KEY`와 `NEIS_SCHOOL_CODE`를 가져옵니다.
2. 각각 비어 있으면 `비어 있음`, 아니면 `입력됨`을 출력합니다. **값 자체는 출력하지 않습니다.**
3. 이 파일은 `app` 패키지를 가져오므로, 아래처럼 `-m`으로 실행합니다. (`.py`를 붙이지 않고, `\` 대신 `.`을 씁니다)
   ```powershell
   python -m practice.step01.p6_config_check
   ```

**확인 방법** (`.env`를 채운 컴퓨터에서)

```
NEIS_API_KEY: 입력됨
NEIS_SCHOOL_CODE: 입력됨
```

**왜 `-m`으로 실행하나요?**

- `python practice\step01\파일.py`로 실행하면, Python은 **그 파일이 있는 폴더**(`practice\step01`)에서 `app`을 찾습니다. 거기에는 `app`이 없어서 `ModuleNotFoundError: No module named 'app'`이 납니다.
- `python -m practice.step01.파일`로 실행하면 **지금 폴더**(프로젝트 맨 위)에서 찾기 시작합니다. 그래서 `app`을 찾습니다.
- `python -m pytest`가 `tests` 폴더에서 `app`을 찾을 수 있는 것과 같은 이유입니다. (3단계)

<details><summary>정답 예시</summary>

```python
# .env의 값이 들어갔는지 확인한다. 값 자체는 화면에 보이지 않게 한다.
from app.config import NEIS_API_KEY, NEIS_SCHOOL_CODE

if NEIS_API_KEY == "":
    print("NEIS_API_KEY: 비어 있음")
else:
    print("NEIS_API_KEY: 입력됨")

if NEIS_SCHOOL_CODE == "":
    print("NEIS_SCHOOL_CODE: 비어 있음")
else:
    print("NEIS_SCHOOL_CODE: 입력됨")
```

- 화면에 키를 출력하면 캡처나 기록으로 새어 나갈 수 있습니다. 그래서 `check_setup.py`도 "입력됨"만 보여 줍니다.

</details>

---

## 다 풀었다면

- [ ] 파일을 만들고 `python 파일.py`로 실행할 수 있다.
- [ ] 오류 메시지의 맨 아래 줄과 줄 번호를 보고 고칠 곳을 찾을 수 있다.
- [ ] `os.getenv("이름", "")`와 `os.getenv("이름")`의 차이를 말할 수 있다.

## 이번 단계 핵심 정리

1. Python 파일은 `python 파일명.py`로, `app`을 가져오는 파일은 `python -m 폴더.파일`로 실행한다.
2. `if`·`else` 줄 끝에는 `:`, 그 아래 줄은 빈칸 4개로 들여쓴다. 비교는 `==`다.
3. 오류는 한 번에 하나씩 나온다. 맨 아래 줄을 읽고 한 곳씩 고친다.
4. 환경 변수는 없을 때 `None`이 오므로, 기본값 `""`를 주고 읽는다.
5. 비밀값은 "입력됨/비어 있음"처럼 상태만 출력한다.
