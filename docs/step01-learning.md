# 1단계 학습 정리: Python 실행과 개발 환경

## 이 문서를 다 읽으면 할 수 있게 되는 것

1. Python 파일을 만들고 `python 파일명.py`로 실행하는 방법을 설명할 수 있다.
2. 가상환경, pip, requirements.txt, .env가 각각 왜 필요한지 말할 수 있다.
3. 이번 단계 코드(`app/config.py`, `check_setup.py`)를 한 줄도 빠짐없이 설명할 수 있다.

## 읽기 전에

- 코드 예시는 모두 실제로 실행한 결과를 붙였습니다.
- 오류 메시지의 긴 파일 경로는 `예시.py`처럼 짧게 줄여 적었습니다.
- "Java 비교"는 이해를 돕는 참고용입니다. 건너뛰어도 Python 설명만으로 이해할 수 있습니다.

---

## 1. 이번 단계에서 새로 나온 것

1단계라서 모두 처음 나온 것입니다.

**개발 환경**

1. Python 파일과 실행
2. 가상환경
3. pip
4. requirements.txt
5. .env와 환경 변수

**Python 문법**

6. `print`와 문자열
7. 주석 `#`
8. 변수와 `=`
9. 타입 힌트
10. `if` / `else`와 들여쓰기
11. `==` 비교와 `True` / `False`
12. `import`와 `from ... import`
13. 패키지와 `__init__.py`
14. `None`
15. 대문자 이름 (상수 관례)

---

## 2. 하나씩 설명

### 2-1. Python 파일과 실행

**설명**

Python 코드는 `.py`로 끝나는 글자 파일에 적습니다.

터미널에서 `python 파일명.py`라고 치면 실행됩니다.
Python은 파일을 맨 위 줄부터 아래로 한 줄씩 읽으며 바로 실행합니다.

Java처럼 컴파일 명령(사람이 쓴 코드를 실행용 파일로 미리 바꾸는 명령)을 따로 치지 않습니다.

**작은 예시**

`hello.py` 파일에 한 줄을 적습니다.

```python
print("안녕하세요")
```

실행 명령:

```powershell
python hello.py
```

결과:

```
안녕하세요
```

**이 프로젝트에서**

```powershell
python check_setup.py
```

**Java 비교**

```java
// Hello.java
public class Hello {
    public static void main(String[] args) {
        System.out.println("안녕하세요");
    }
}
```

```
javac Hello.java   ← 컴파일
java Hello         ← 실행
```

Python에는 클래스와 `main` 메서드가 꼭 있어야 하는 규칙이 없습니다. 파일의 첫 줄부터 실행됩니다.

**자주 하는 실수: 이 컴퓨터에서 가상환경 없이 `python`을 친다**

이 컴퓨터는 Python을 설치할 때 `python` 명령이 등록되지 않았습니다.
그래서 가상환경 밖에서 `python --version`을 치면 아래처럼 나옵니다. (실제 결과)

```
Python was not found; run without arguments to install from the Microsoft Store, or disable this shortcut from Settings > Apps > Advanced app settings > App execution aliases.
```

가상환경을 켜면 `python`이 정상으로 동작합니다. (2-2 참고)
가상환경 밖에서는 `py` 명령을 씁니다.

---

### 2-2. 가상환경 (venv)

**설명**

가상환경은 이 프로젝트만 쓰는 Python 작업 공간입니다.

**비유**

프로젝트마다 따로 쓰는 공구함입니다.
이 프로젝트에 필요한 라이브러리(남이 만들어 둔 코드 묶음)는 이 공구함에만 넣습니다.
그래서 다른 프로젝트와 섞이지 않습니다.

**만든 명령**

```powershell
py -3.13 -m venv .venv
```

- `py -3.13`: 3.13 버전 Python을 실행합니다.
- `-m venv`: Python에 들어 있는 `venv` 도구를 실행합니다. `-m`은 "이 이름의 모듈(Python 코드 파일)을 프로그램처럼 실행하라"는 뜻입니다.
- `.venv`: 가상환경을 만들 폴더 이름입니다.

결과: 아무것도 출력되지 않으면 성공입니다. `.venv` 폴더가 생깁니다.

```
.venv\
├── Scripts\python.exe     ← 이 프로젝트 전용 Python
├── Scripts\Activate.ps1   ← 가상환경을 켜는 스크립트
├── Lib\site-packages\     ← 설치한 라이브러리가 들어가는 곳
└── pyvenv.cfg             ← 어떤 Python으로 만들었는지 적힌 설정 파일
```

**켜기와 끄기**

```powershell
.venv\Scripts\Activate.ps1   # 켜기
deactivate                   # 끄기
```

켜면 줄 맨 앞에 `(.venv)`가 붙습니다.

켜기 전과 켠 뒤에 `python`이 가리키는 파일을 확인했습니다. (실제 결과)

```
켜기 전: C:\Users\...\AppData\Local\Microsoft\WindowsApps\python.exe   ← Microsoft Store 안내용
켠 뒤:   C:\neis_groupware_bot\.venv\Scripts\python.exe               ← 이 프로젝트 전용 Python
```

**Java 비교**

Java는 JDK 하나를 여러 프로젝트가 함께 씁니다.
라이브러리는 Maven이나 Gradle이 공용 저장소(`~/.m2` 등)에 버전별로 따로 내려받아 둡니다.
그래서 프로젝트마다 다른 버전을 골라 써도 충돌하지 않습니다.

Python은 한 Python에 같은 라이브러리를 한 버전만 설치할 수 있습니다.
그래서 프로젝트마다 가상환경을 따로 만들어 충돌을 피합니다.

**자주 하는 실수: 가상환경을 켜지 않고 실행한다**

라이브러리는 가상환경 안에만 설치되어 있습니다.
가상환경 밖의 Python으로 실행하면 라이브러리를 찾지 못합니다.
`py check_setup.py`로 실행했을 때의 실제 결과입니다.

```
Traceback (most recent call last):
  File "C:\neis_groupware_bot\check_setup.py", line 6, in <module>
    from app.config import NEIS_API_KEY
  File "C:\neis_groupware_bot\app\config.py", line 9, in <module>
    from dotenv import load_dotenv
ModuleNotFoundError: No module named 'dotenv'
```

`Traceback`은 오류가 어디를 거쳐 났는지 보여 주는 기록입니다. **맨 아래 줄이 진짜 원인**입니다.
`ModuleNotFoundError`(모듈을 찾지 못했다)가 보이면, 먼저 줄 앞에 `(.venv)`가 있는지 확인하세요.

---

### 2-3. pip

**설명**

pip는 라이브러리를 인터넷에서 내려받아 설치하는 프로그램입니다.

라이브러리는 PyPI(파이피아이)라는 Python 라이브러리 공개 저장소에서 가져옵니다.

**이번에 실행한 명령과 실제 결과**

```powershell
python -m pip install python-dotenv
```

```
Collecting python-dotenv
  Downloading python_dotenv-1.2.4-py3-none-any.whl.metadata (29 kB)
Downloading python_dotenv-1.2.4-py3-none-any.whl (23 kB)
Installing collected packages: python-dotenv
Successfully installed python-dotenv-1.2.4

[notice] A new release of pip is available: 26.2.1 -> 26.3
```

- `Successfully installed`는 설치에 성공했다는 뜻입니다.
- `[notice]`는 pip 새 버전이 나왔다는 알림입니다. 오류가 아니라서 무시해도 됩니다.

설치된 목록 보기:

```powershell
python -m pip freeze
```

```
python-dotenv==1.2.4
```

**`pip install` 대신 `python -m pip install`을 쓰는 이유**

"지금 이 `python`에 설치하라"는 뜻이 분명해집니다.
가상환경을 켰다면 `.venv` 안의 Python에 설치됩니다.

**Java 비교**

| Python | Java |
| --- | --- |
| PyPI | Maven Central |
| pip | Maven/Gradle의 의존성 내려받기 |

Maven은 빌드할 때 필요한 라이브러리를 자동으로 내려받습니다.
pip는 설치 명령을 직접 실행해야 합니다.

**자주 하는 실수: 가상환경을 켜지 않고 설치한다**

그러면 컴퓨터 전체에서 쓰는 Python에 설치됩니다.
설치는 성공했는데, 가상환경에서 실행하면 `No module named ...` 오류가 납니다.
설치 전에 줄 앞의 `(.venv)`를 확인하세요.

---

### 2-4. requirements.txt

**설명**

이 프로젝트에 필요한 라이브러리와 버전을 적어 둔 목록 파일입니다.
다른 컴퓨터에서도 이 목록 하나로 똑같이 설치할 수 있습니다.

**이 프로젝트 파일**

```
# .env 파일을 읽어 오는 라이브러리 (1단계부터 사용)
python-dotenv==1.2.4
```

- `==1.2.4`: 정확히 1.2.4 버전을 설치하라는 뜻입니다.
- `#`로 시작하는 줄은 설명이라서 pip가 무시합니다.

**설치 명령과 실제 결과** (이미 설치된 상태에서 실행)

```powershell
python -m pip install -r requirements.txt
```

```
Requirement already satisfied: python-dotenv==1.2.4 in .\.venv\Lib\site-packages (from -r requirements.txt (line 7)) (1.2.4)
```

- `-r`은 "이 파일에 적힌 목록을 읽어서 설치하라"는 뜻입니다.
- `already satisfied`는 "이미 설치되어 있다"는 뜻입니다.

**Java 비교**

`pom.xml`의 `<dependencies>`나 `build.gradle`의 `dependencies { }`와 같은 역할입니다.

```xml
<dependency>
    <groupId>그룹이름</groupId>
    <artifactId>라이브러리이름</artifactId>
    <version>1.2.4</version>
</dependency>
```

**자주 하는 실수: 설치만 하고 목록에 적지 않는다**

내 컴퓨터에서는 잘 돌아갑니다.
그런데 다른 컴퓨터에서는 `ModuleNotFoundError`가 납니다.
라이브러리를 설치했으면 바로 requirements.txt에 한 줄 추가하세요.

---

### 2-5. .env와 환경 변수

**설명**

환경 변수는 운영체제(Windows 같은 기본 프로그램)가 들고 있는 "이름=값" 쌍입니다.
프로그램은 코드 밖에 있는 이 값을 읽어 쓸 수 있습니다.

`.env`는 환경 변수로 쓸 값을 적어 두는 글자 파일입니다.
python-dotenv 라이브러리가 이 파일을 읽어 환경 변수로 등록해 줍니다.

**왜 쓰나요?**

인증키를 코드에 직접 쓰면, 코드를 GitHub에 올릴 때 키도 같이 올라갑니다.
그래서 키는 `.env`에만 적고, `.env`는 `.gitignore`로 올라가지 않게 막습니다.

**비유**

집 열쇠(인증키)를 설계도(코드)에 붙여 두지 않고, 내 서랍(`.env`)에 따로 넣어 두는 것입니다.

**두 파일의 차이**

| 파일 | 들어 있는 것 | GitHub에 올리나? |
| --- | --- | --- |
| `.env.example` | 항목 이름만 (`NEIS_API_KEY=`) | 올린다 |
| `.env` | 실제 값 | 올리지 않는다 |

**실제 확인 결과**

`.env`가 없을 때 `check_setup.py`의 마지막 줄:

```
NEIS_API_KEY: 비어 있음 (.env 파일을 확인하세요)
```

시험용 가짜 값을 넣은 `.env`를 만들었을 때:

```
NEIS_API_KEY: 입력됨
```

(시험용 `.env`는 확인 직후 지웠습니다.)

**Java 비교**

Spring Boot에서 `application.properties`에 `neis.api-key=${NEIS_API_KEY}`처럼 적고, 실제 값은 환경 변수로 넣는 것과 같은 목적입니다.
Java에서 환경 변수를 읽는 코드는 `System.getenv("NEIS_API_KEY")`입니다.

**자주 하는 실수: 메모장이 이름을 `.env.txt`로 저장한다**

그러면 python-dotenv가 파일을 찾지 못합니다.
`Copy-Item .env.example .env`로 만들면 이름이 정확히 `.env`가 됩니다.
혹시 `.env.txt`가 생겨도 GitHub에 올라가지 않도록, `.gitignore`에 `.env.*` 규칙을 넣어 두었습니다.

---

### 2-6. `print`와 문자열

**설명**

`print(...)`는 괄호 안의 값을 화면에 출력합니다.
`print`처럼 이름을 부르면 정해진 일을 하는 코드 묶음을 **함수**라고 합니다.

문자열은 글자들의 묶음입니다. 큰따옴표 `"..."`나 작은따옴표 `'...'`로 감쌉니다.

`print`에 쉼표로 값을 여러 개 넣으면, 값 사이에 빈칸 하나를 넣어 출력합니다.

**작은 예시**

```python
print("Python 버전:", "3.13")
print("점심", "메뉴", "알림")
```

결과:

```
Python 버전: 3.13
점심 메뉴 알림
```

**이 프로젝트 코드**

```python
print("Python 버전:", sys.version)
```

**Java 비교**

```java
System.out.println("Python 버전: " + version);
```

Java는 `+`로 이어 붙입니다. Python도 `+`를 쓸 수 있지만, 쉼표가 더 간단합니다.

**자주 하는 실수: 따옴표를 빠뜨린다**

```python
print(안녕하세요)
```

결과:

```
Traceback (most recent call last):
  File "예시.py", line 1, in <module>
    print(안녕하세요)
          ^^^^^^^^^^
NameError: name '안녕하세요' is not defined
```

따옴표가 없으면 Python은 `안녕하세요`를 변수 이름으로 생각합니다.
그런 이름의 변수가 없어서 `NameError`(그런 이름이 없다는 오류)가 납니다.

---

### 2-7. 주석 `#`

**설명**

`#` 뒤에 적은 글은 Python이 무시합니다. 사람이 읽으라고 남기는 메모입니다.
줄 끝에 붙여 쓸 수도 있습니다.

**작은 예시**

```python
# 이 줄은 주석이라 실행되지 않는다
print("급식 알림 봇")  # 줄 끝에도 주석을 붙일 수 있다
```

결과:

```
급식 알림 봇
```

**이 프로젝트 코드** (`app/config.py`)

```python
# .env 파일의 내용을 환경 변수로 등록한다.
# .env 파일이 없어도 오류를 내지 않으므로, 값이 비었는지는 쓰는 쪽에서 확인해야 한다.
load_dotenv()
```

이 프로젝트의 주석은 "무엇을 하는지"보다 **"왜 이렇게 했는지"**를 적습니다.

**Java 비교**

Java는 `//`(한 줄)과 `/* ... */`(여러 줄)를 씁니다. Python은 `#` 하나만 씁니다.

**자주 하는 실수: Java 습관으로 `//`를 쓴다**

```python
// 자바식 주석
print("급식 알림 봇")
```

결과:

```
  File "예시.py", line 1
    // 자바식 주석
    ^^
SyntaxError: invalid syntax
```

`SyntaxError`는 "문법이 틀렸다"는 오류입니다. 이 오류가 나면 파일이 한 줄도 실행되지 않습니다.

---

### 2-8. 변수와 `=`

**설명**

변수는 값에 붙이는 이름표입니다. `이름 = 값` 모양으로 만듭니다.
같은 이름에 다시 `=`를 쓰면 새 값으로 바뀝니다.

**비유**

상자에 이름표를 붙이고 물건을 넣는 것입니다. 같은 상자에 새 물건을 넣으면 예전 물건은 빠집니다.

**작은 예시**

```python
bot_name = "급식봇"
print(bot_name)
bot_name = "학사일정봇"
print(bot_name)
```

결과:

```
급식봇
학사일정봇
```

**이름 짓는 관례**

Python은 단어 사이에 밑줄을 넣습니다. (`bot_name`)
Java는 두 번째 단어부터 대문자로 씁니다. (`botName`)

**Java 비교**

```java
String botName = "급식봇";
```

- Java는 변수 앞에 타입(`String`)을 꼭 씁니다. Python은 쓰지 않아도 됩니다.
- Java는 문장 끝에 `;`를 꼭 씁니다. Python은 쓰지 않습니다.

Python에서 `;`를 붙여도 오류는 나지 않지만, Python답지 않은 코드입니다.

```python
print("세미콜론 없이도")
print("줄이 끝난다");
```

결과:

```
세미콜론 없이도
줄이 끝난다
```

**자주 하는 실수: 이름에 오타를 낸다**

```python
bot_name = "급식봇"
print(botname)
```

결과:

```
Traceback (most recent call last):
  File "예시.py", line 2, in <module>
    print(botname)
          ^^^^^^^
NameError: name 'botname' is not defined. Did you mean: 'bot_name'?
```

마지막 줄의 `Did you mean: 'bot_name'?`은 "혹시 `bot_name`을 쓰려던 것인가요?"라는 힌트입니다.

---

### 2-9. 타입 힌트

**설명**

타입 힌트는 변수에 어떤 종류의 값을 넣을지 적어 두는 표시입니다.
`이름: 타입 = 값` 모양입니다.

| 타입 | 뜻 | 예 |
| --- | --- | --- |
| `str` | 문자열 | `"급식봇"` |
| `int` | 정수 | `3` |

중요한 점: **Python은 실행할 때 타입 힌트를 검사하지 않습니다.**
타입 힌트는 사람과 편집기(VS Code 같은 코드 작성 프로그램)를 위한 표시입니다.

**작은 예시**

```python
count: int = 3
print(count)
```

결과:

```
3
```

**이 프로젝트 코드** (`app/config.py`)

```python
NEIS_API_KEY: str = os.getenv("NEIS_API_KEY", "")
```

"`NEIS_API_KEY`에는 문자열이 들어간다"고 적어 둔 것입니다.

**Java 비교**

```java
int count = 3;
```

Java는 컴파일러가 타입을 검사합니다. `int count = "셋";`이라고 쓰면 컴파일이 되지 않습니다.

**자주 하는 실수: 타입 힌트가 틀린 값을 막아 준다고 생각한다**

```python
count: int = "셋"
print(count)
```

결과:

```
셋
```

`int`라고 적었는데 문자열을 넣어도 오류 없이 실행됩니다. 힌트는 약속일 뿐, 강제하지 않습니다.

---

### 2-10. `if` / `else`와 들여쓰기

**설명**

`if` 뒤의 조건이 참이면 바로 아래 블록(한 덩어리로 실행되는 줄들)을 실행합니다.
조건이 거짓이면 `else` 아래 블록을 실행합니다.

Python은 중괄호 `{}` 대신 **들여쓰기**(줄 앞의 빈칸)로 블록을 구분합니다.
같은 블록에 속한 줄은 같은 칸 수만큼 들여씁니다. 보통 4칸을 씁니다.

`if`와 `else` 줄 끝에는 콜론 `:`을 꼭 붙입니다. "여기부터 블록이 시작된다"는 표시입니다.

**작은 예시**

```python
key = ""
if key == "":
    print("비어 있음")
else:
    print("입력됨")
```

결과:

```
비어 있음
```

**이 프로젝트 코드** (`check_setup.py`)

```python
if NEIS_API_KEY == "":
    print("NEIS_API_KEY: 비어 있음 (.env 파일을 확인하세요)")
else:
    print("NEIS_API_KEY: 입력됨")
```

**Java 비교**

```java
if (neisApiKey.isEmpty()) {
    System.out.println("NEIS_API_KEY: 비어 있음");
} else {
    System.out.println("NEIS_API_KEY: 입력됨");
}
```

| Java | Python |
| --- | --- |
| 조건을 `( )`로 감싼다 | 감싸지 않아도 된다 |
| 블록을 `{ }`로 감싼다 | 콜론 `:`과 들여쓰기로 표시한다 |
| 들여쓰기는 보기 좋게 하는 용도 | 들여쓰기가 문법이다 |

**자주 하는 실수: 들여쓰기를 빠뜨린다**

```python
key = ""
if key == "":
print("비어 있음")
```

결과:

```
  File "예시.py", line 3
    print("비어 있음")
    ^^^^^
IndentationError: expected an indented block after 'if' statement on line 2
```

`IndentationError`는 "2번째 줄 `if` 다음에 들여쓴 블록이 와야 한다"는 뜻입니다.

---

### 2-11. `==` 비교와 `True` / `False`

**설명**

`==`는 두 값이 같은지 비교합니다.
결과는 `True`(참) 또는 `False`(거짓) 둘 중 하나입니다.

`=` 하나는 비교가 아니라 "값을 넣어라"(대입)라는 뜻입니다. 둘을 헷갈리면 안 됩니다.

**작은 예시**

```python
a = "사과"
print(a == "사과")
print(a == "배")
```

결과:

```
True
False
```

**이 프로젝트 코드**

```python
if NEIS_API_KEY == "":
```

`NEIS_API_KEY`가 빈 문자열 `""`과 같은지 비교합니다.

**Java 비교**

Java에서 문자열에 `==`를 쓰면 "같은 객체(메모리 속 같은 물건)인가"를 비교합니다.
그래서 문자열 내용을 비교할 때는 `.equals()`를 씁니다.

```java
if (neisApiKey.equals("")) { ... }
```

Python의 `==`는 **내용**을 비교합니다. `.equals()`가 따로 필요 없습니다.

**자주 하는 실수: `if` 안에 `=`를 하나만 쓴다**

```python
key = ""
if key = "":
    print("비어 있음")
```

결과:

```
  File "예시.py", line 2
    if key = "":
       ^^^^^^^^
SyntaxError: invalid syntax. Maybe you meant '==' or ':=' instead of '='?
```

Python이 "`==`를 쓰려던 것 아닌가요?"라고 알려 줍니다.

---

### 2-12. `import`와 `from ... import`

**설명**

모듈은 코드를 담은 `.py` 파일 하나입니다.
`import`는 다른 모듈의 코드를 가져와 쓰는 명령입니다.

`import os`는 `os` 모듈을 통째로 가져옵니다.
쓸 때는 `os.getenv(...)`처럼 앞에 `모듈이름.`을 붙입니다.

`from dotenv import load_dotenv`는 `dotenv` 모듈 안의 `load_dotenv` 하나만 가져옵니다.
쓸 때는 이름만 씁니다. (`load_dotenv()`)

`import`한 순간, 가져온 파일의 코드가 위에서부터 한 번 실행됩니다.
그래서 `check_setup.py`가 `app.config`를 가져오면, `config.py` 안의 `load_dotenv()`도 그때 실행됩니다.

**작은 예시 1: 모듈 통째로 가져오기**

```python
import os

print(os.getenv("NO_SUCH_NAME", "기본값"))
```

결과:

```
기본값
```

`NO_SUCH_NAME`이라는 환경 변수가 없어서, 두 번째에 적은 기본값이 나왔습니다.

**작은 예시 2: 하나만 가져오기**

```python
from os import getenv

print(getenv("NO_SUCH_NAME", "기본값"))
```

결과:

```
기본값
```

**이 프로젝트 코드**

```python
import os                                  # app/config.py

from dotenv import load_dotenv             # app/config.py

import sys                                 # check_setup.py

from app.config import NEIS_API_KEY        # check_setup.py
```

**설치 이름과 import 이름이 다를 수 있습니다**

설치할 때는 `python-dotenv`라고 썼습니다. 그런데 가져올 때는 `dotenv`라고 씁니다.
라이브러리마다 다르니, 공식 설명서를 확인해야 합니다.

**Java 비교**

| Python | Java |
| --- | --- |
| `from dotenv import load_dotenv` | `import java.util.List;` (클래스 하나 가져오기) |
| `import os` 후 `os.getenv(...)` | 가져오지 않고 `java.lang.System.getenv(...)`처럼 전체 이름 쓰기와 비슷 |
| `from os import getenv` 후 `getenv(...)` | `import static java.lang.Math.max;` 후 `max(...)` |

**자주 하는 실수: 가져올 이름에 오타를 낸다**

```python
from dotenv import load_dotnev
```

결과:

```
Traceback (most recent call last):
  File "예시.py", line 1, in <module>
    from dotenv import load_dotnev
ImportError: cannot import name 'load_dotnev' from 'dotenv' (C:\neis_groupware_bot\.venv\Lib\site-packages\dotenv\__init__.py). Did you mean: 'load_dotenv'?
```

`ImportError`는 "그런 이름을 가져올 수 없다"는 오류입니다. 여기서도 `Did you mean`이 바른 이름을 알려 줍니다.

---

### 2-13. 패키지와 `__init__.py`

**설명**

패키지는 모듈(`.py` 파일)을 모아 둔 폴더입니다.

폴더 안에 `__init__.py` 파일을 두면 Python이 그 폴더를 패키지로 봅니다.
이번 단계의 `app/__init__.py`는 설명 주석만 들어 있는 파일입니다.

`from app.config import NEIS_API_KEY`는 "`app` 패키지의 `config` 모듈에서 `NEIS_API_KEY`를 가져와라"라는 뜻입니다.
점(`.`)은 "폴더 안으로 들어간다"는 표시입니다.

`python check_setup.py`로 실행하면, Python은 `check_setup.py`가 있는 폴더에서 모듈을 찾기 시작합니다.
그 폴더(프로젝트 최상위)에 `app` 폴더가 있으니 `app.config`를 찾을 수 있습니다.

**`__pycache__` 폴더**

실행하고 나면 `app\__pycache__` 폴더가 생깁니다.

```
app\__pycache__\config.cpython-313.pyc
app\__pycache__\__init__.cpython-313.pyc
```

Python이 읽은 코드를 다음에 더 빨리 읽으려고 바꿔 저장해 둔 파일입니다.
지워도 다시 생기므로 `.gitignore`로 GitHub에 올리지 않습니다.

**Java 비교**

```java
// app/Config.java
package app;

public class Config {
    public static final String NEIS_API_KEY = ...;
}

// 다른 파일
import app.Config;
```

Java는 폴더가 곧 패키지이고, 파일 맨 위에 `package app;`을 선언합니다.
Python은 선언 대신 폴더 구조와 `__init__.py`로 패키지를 나타냅니다.

**자주 하는 실수: 모듈을 통째로 가져와 놓고 이름만 쓴다**

```python
import app.config

print(NEIS_API_KEY)
```

결과 (프로젝트 최상위 폴더에서 실행):

```
Traceback (most recent call last):
  File "예시.py", line 3, in <module>
    print(NEIS_API_KEY)
          ^^^^^^^^^^^^
NameError: name 'NEIS_API_KEY' is not defined
```

`import app.config`로 가져왔다면 `app.config.NEIS_API_KEY`처럼 전체 이름을 써야 합니다.
이름만 쓰고 싶으면 `from app.config import NEIS_API_KEY`로 가져옵니다.

---

### 2-14. `None`

**설명**

`None`은 "값이 없음"을 뜻하는 특별한 값입니다.

`os.getenv`는 찾는 환경 변수가 없고 기본값도 주지 않으면 `None`을 돌려줍니다.
함수가 일을 마치고 돌려주는 결과를 **반환값**이라고 합니다.

**작은 예시**

```python
import os

print(os.getenv("NO_SUCH_NAME"))
```

결과:

```
None
```

`None`과 빈 문자열 `""`은 다른 값입니다.

```python
print(None == "")
print("" == "")
```

결과:

```
False
True
```

**이 프로젝트에서**

`app/config.py`는 `os.getenv("NEIS_API_KEY", "")`처럼 기본값 `""`를 줍니다.
그래서 값이 없을 때 `None` 대신 빈 문자열을 받습니다. 아래 실수를 막기 위해서입니다.

**Java 비교**

Java의 `null`과 비슷합니다.

`System.getenv("X")`는 값이 없으면 `null`을 돌려줍니다.
`null`인 상태로 `key.isEmpty()`를 부르면 `NullPointerException`이 납니다.

**자주 하는 실수: `None`에 문자열을 이어 붙인다**

```python
import os

key = os.getenv("NO_SUCH_NAME")
print("키: " + key)
```

결과:

```
Traceback (most recent call last):
  File "예시.py", line 4, in <module>
    print("키: " + key)
          ~~~~~~~^~~~~
TypeError: can only concatenate str (not "NoneType") to str
```

`TypeError`는 "이 종류의 값끼리는 그 일을 할 수 없다"는 오류입니다.
문자열에는 문자열만 이어 붙일 수 있는데 `None`이 왔기 때문입니다.

---

### 2-15. 대문자 이름 (상수 관례)

**설명**

프로그램이 도는 동안 바뀌지 않을 설정값은 이름을 **대문자와 밑줄**로 짓는 관례가 있습니다. (`NEIS_API_KEY`)
이런 값을 상수라고 부릅니다.

Python에는 Java의 `final`처럼 "다시 못 넣게 막는 기능"이 없습니다.
대문자 이름은 "이 값은 바꾸지 마세요"라는 사람끼리의 약속입니다.

**작은 예시**

```python
NEIS_API_KEY = "첫 번째 값"
NEIS_API_KEY = "두 번째 값"
print(NEIS_API_KEY)
```

결과:

```
두 번째 값
```

**Java 비교**

```java
public static final String NEIS_API_KEY = "첫 번째 값";
NEIS_API_KEY = "두 번째 값";   // 컴파일 오류
```

**자주 하는 실수: 대문자로 지으면 못 바꾼다고 믿는다**

위 예시처럼 Python은 막지 않습니다. 약속을 지키는 것은 코드를 쓰는 사람의 몫입니다.

---

## 3. 코드 줄 단위 해설

### 3-1. `app/__init__.py`

```python
# 이 파일이 있으면 Python은 app 폴더를 '패키지'(코드 파일을 모아 둔 묶음)로 본다.
# 그래서 다른 파일에서 from app.config import ... 처럼 app 폴더 안의 파일을 불러올 수 있다.
# 지금은 이 파일에 넣을 코드가 없어서 설명만 적어 둔다.
```

| 줄 | 설명 |
| --- | --- |
| 1~3 | 모두 주석입니다. 실행되는 코드는 없습니다. 파일이 있다는 것 자체가 "app은 패키지"라는 표시입니다. |

### 3-2. `app/config.py`

**1~5줄: 파일 설명 주석**

```python
# config.py: .env 파일에 적어 둔 설정값을 읽어 오는 파일
#
# 인증키를 코드에 직접 쓰면 코드를 GitHub에 올릴 때 키도 같이 올라간다.
# 그래서 비밀 정보는 .env 파일에만 두고, 다른 코드는 모두 이 파일을 거쳐서 값을 읽는다.
# 읽는 곳을 한 군데로 모아 두면 항목 이름이 바뀌어도 이 파일만 고치면 된다.
```

이 파일이 왜 있는지 적었습니다. 2줄의 `#` 하나는 문단을 나누려고 비워 둔 주석입니다.

**7~9줄: 필요한 것 가져오기**

```python
import os

from dotenv import load_dotenv
```

| 줄 | 설명 |
| --- | --- |
| 7 | `os` 모듈을 가져옵니다. `os`는 Python에 기본으로 들어 있는 표준 라이브러리입니다. 운영체제와 관련된 기능을 모아 두었습니다. 여기서는 환경 변수를 읽는 `getenv`를 씁니다. |
| 8 | 빈 줄입니다. 표준 라이브러리와 따로 설치한 라이브러리를 나눠 적는 관례입니다. |
| 9 | 따로 설치한 `python-dotenv` 라이브러리에서 `load_dotenv` 함수 하나만 가져옵니다. |

**11~13줄: .env 읽기**

```python
# .env 파일의 내용을 환경 변수로 등록한다.
# .env 파일이 없어도 오류를 내지 않으므로, 값이 비었는지는 쓰는 쪽에서 확인해야 한다.
load_dotenv()
```

| 줄 | 설명 |
| --- | --- |
| 11~12 | 왜 이렇게 하는지 적은 주석입니다. |
| 13 | `load_dotenv` 함수를 실행합니다. 괄호 안이 비어 있으면 기본 설정으로 동작합니다. 이 코드가 있는 `app` 폴더부터 위쪽 폴더로 올라가며 `.env`를 찾습니다. 그래서 프로젝트 최상위의 `.env`를 찾아 읽습니다. (시험용 `.env`로 실제 확인) |

**15~17줄: 인증키 꺼내기**

```python
# 값이 없을 때 None 대신 빈 문자열("")을 넣는다.
# 그래야 이 값을 쓰는 코드가 "문자열인가?"를 따로 따지지 않고 바로 비교할 수 있다.
NEIS_API_KEY: str = os.getenv("NEIS_API_KEY", "")
```

17줄을 조각으로 나눠 봅니다.

| 조각 | 뜻 |
| --- | --- |
| `NEIS_API_KEY` | 변수 이름입니다. 대문자는 "바꾸지 않을 설정값"이라는 약속입니다. (2-15) |
| `: str` | 타입 힌트입니다. 문자열이 들어간다는 표시입니다. (2-9) |
| `=` | 오른쪽 값을 왼쪽 이름에 넣습니다. (2-8) |
| `os.getenv(` | `os` 모듈의 `getenv` 함수를 부릅니다. (2-12) |
| `"NEIS_API_KEY"` | 찾을 환경 변수의 이름입니다. |
| `""` | 그 이름이 없을 때 대신 돌려받을 기본값입니다. (2-14) |

Java로 쓰면 이렇습니다.

```java
public static final String NEIS_API_KEY =
        Objects.requireNonNullElse(System.getenv("NEIS_API_KEY"), "");
```

### 3-3. `check_setup.py`

**1~6줄**

```python
# check_setup.py: 1단계 환경 준비가 잘 되었는지 확인하는 파일
# 실행 방법(가상환경을 켠 상태에서): python check_setup.py

import sys

from app.config import NEIS_API_KEY
```

| 줄 | 설명 |
| --- | --- |
| 1~2 | 파일 설명과 실행 방법을 적은 주석입니다. |
| 4 | `sys` 모듈을 가져옵니다. `sys`는 지금 실행 중인 Python 자체의 정보를 알려 주는 표준 라이브러리입니다. |
| 6 | `app/config.py`에서 `NEIS_API_KEY`를 가져옵니다. 이 순간 `config.py`가 한 번 실행되면서 `load_dotenv()`도 실행됩니다. (2-12) |

**8~11줄**

```python
# 가상환경의 Python으로 실행되었는지 눈으로 확인하려고 Python의 위치를 보여 준다.
# 위치가 .venv 폴더 안이면 가상환경이 켜진 상태다.
print("Python 버전:", sys.version)
print("Python 위치:", sys.executable)
```

| 줄 | 설명 |
| --- | --- |
| 8~9 | 왜 위치를 보여 주는지 적은 주석입니다. |
| 10 | `sys.version`은 Python 버전을 담은 문자열입니다. 쉼표 덕분에 앞 글자와 빈칸 하나를 두고 출력됩니다. |
| 11 | `sys.executable`은 지금 실행 중인 `python.exe` 파일의 위치입니다. |

**13~17줄**

```python
# 인증키 값 자체는 화면에 보여 주지 않는다. 화면 캡처나 기록을 통해 새어 나갈 수 있어서다.
if NEIS_API_KEY == "":
    print("NEIS_API_KEY: 비어 있음 (.env 파일을 확인하세요)")
else:
    print("NEIS_API_KEY: 입력됨")
```

| 줄 | 설명 |
| --- | --- |
| 13 | 키 값을 출력하지 않는 이유를 적은 주석입니다. |
| 14 | 키가 빈 문자열인지 비교합니다. 줄 끝의 `:`은 블록 시작 표시입니다. |
| 15 | 4칸 들여썼으므로 14줄 `if`의 블록입니다. 키가 비었을 때만 실행됩니다. |
| 16 | `else:`는 "조건이 거짓이면"이라는 뜻입니다. |
| 17 | 4칸 들여썼으므로 `else`의 블록입니다. 키가 있을 때만 실행됩니다. |

**실행 결과** (개발자가 NEIS 인증키를 넣은 뒤)

```
Python 버전: 3.13.16 (tags/v3.13.16:cbc944f, Sep 30 2026, 19:17:50) [MSC v.1944 64 bit (AMD64)]
Python 위치: C:\neis_groupware_bot\.venv\Scripts\python.exe
NEIS_API_KEY: 입력됨
```

### 3-4. 설정 파일들

**`requirements.txt`**: 2-4에서 설명했습니다.

**`.env.example`**: 2-5에서 설명했습니다. 지금은 아래 세 항목의 이름이 들어 있습니다.

| 항목 | 쓰는 단계 |
| --- | --- |
| `NEIS_API_KEY` | 2단계부터 |
| `SLACK_BOT_TOKEN` | 4단계부터 |
| `SLACK_SIGNING_SECRET` | 7단계부터 |

**`.gitignore`**: Git이 무시할 파일 목록입니다. 규칙 읽는 법은 아래와 같습니다.

| 규칙 | 뜻 |
| --- | --- |
| `.env` | 이름이 정확히 `.env`인 파일을 무시합니다. |
| `.env.*` | `*`는 "아무 글자나"라는 뜻입니다. `.env.txt`, `.env.local` 등을 무시합니다. |
| `!.env.example` | `!`는 "무시하지 마라"라는 예외입니다. 위 규칙에 걸리는 `.env.example`을 다시 살려 냅니다. |
| `*.key`, `*.pem` | 개인키 파일의 흔한 확장자입니다. 미리 막아 둡니다. |
| `secrets/` | 끝의 `/`는 폴더라는 뜻입니다. 폴더째 무시합니다. |
| `.venv/` | 가상환경 폴더입니다. 언제든 다시 만들 수 있고 용량이 커서 올리지 않습니다. |
| `__pycache__/`, `*.pyc` | Python이 자동으로 만드는 파일입니다. (2-13) |
| `.pytest_cache/` | 3단계에서 쓸 테스트 도구가 만드는 폴더입니다. 미리 막아 둡니다. |
| `logs/`, `*.log` | 실행 기록입니다. 요청 내용이 들어 있을 수 있어서 올리지 않습니다. |
| `.idea/`, `.vscode/` | 편집기 설정입니다. 사람마다 달라서 공유하지 않습니다. |

규칙이 제대로 동작하는지 `git check-ignore`로 실제 확인했습니다. 개발 기록 4번에 결과가 있습니다.

**`tests/.gitkeep`**: Git은 빈 폴더를 저장하지 않습니다. 그래서 빈 `tests` 폴더를 남기려고 빈 파일 하나를 넣었습니다. `.gitkeep`은 사람들이 흔히 쓰는 이름일 뿐, 특별한 기능은 없습니다.

---

## 4. 사용한 라이브러리

| 라이브러리 | 종류 | 이번에 쓴 것 | 하는 일 |
| --- | --- | --- | --- |
| python-dotenv 1.2.4 | 따로 설치 (pip) | `load_dotenv()` | `.env` 파일을 읽어 환경 변수로 등록합니다. 인자(함수 괄호 안에 넘기는 값) 없이 부르면, 부른 파일의 폴더부터 위쪽으로 `.env`를 찾습니다. |
| os | 표준 라이브러리 | `os.getenv(이름, 기본값)` | 환경 변수 값을 문자열로 돌려줍니다. 없으면 기본값을, 기본값도 없으면 `None`을 돌려줍니다. |
| sys | 표준 라이브러리 | `sys.version`, `sys.executable` | 실행 중인 Python의 버전과 파일 위치를 알려 줍니다. |
| venv | 표준 라이브러리 (도구) | `py -3.13 -m venv .venv` | 가상환경을 만듭니다. |
| pip | 도구 | `python -m pip install ...` | 라이브러리를 설치합니다. |

표준 라이브러리는 Python을 설치하면 함께 들어 있는 라이브러리입니다. 따로 설치하지 않아도 됩니다.

---

## 5. 용어 정리

| 용어 | 쉬운 뜻 | 예시 |
| --- | --- | --- |
| 컴파일 | 사람이 쓴 코드를 실행용 파일로 미리 바꾸는 일 | Java의 `javac` |
| 라이브러리 | 남이 만들어 둔 코드 묶음 | python-dotenv |
| 표준 라이브러리 | Python에 기본으로 들어 있는 라이브러리 | `os`, `sys` |
| 모듈 | 코드를 담은 `.py` 파일 하나 | `config.py` |
| 패키지 | 모듈을 모아 둔 폴더 | `app` 폴더 |
| 함수 | 이름을 부르면 정해진 일을 하는 코드 묶음 | `print()`, `load_dotenv()` |
| 인자 | 함수 괄호 안에 넘기는 값 | `os.getenv("NEIS_API_KEY", "")`의 두 값 |
| 반환값 | 함수가 일을 마치고 돌려주는 결과 | `os.getenv`가 돌려주는 문자열 |
| 변수 | 값에 붙이는 이름표 | `bot_name = "급식봇"` |
| 문자열 | 따옴표로 감싼 글자 묶음 | `"안녕하세요"` |
| 주석 | `#` 뒤에 쓰는, 실행되지 않는 메모 | `# 왜 이렇게 했는지` |
| 타입 힌트 | 변수에 넣을 값의 종류를 적는 표시 (검사는 안 함) | `count: int = 3` |
| 블록 | 한 덩어리로 실행되는 줄들. 들여쓰기로 구분 | `if` 아래 4칸 들여쓴 줄 |
| 들여쓰기 | 줄 앞의 빈칸. Python에서는 문법 | 4칸 |
| `True` / `False` | 참 / 거짓 | `"a" == "a"` → `True` |
| `None` | 값이 없음 | `os.getenv("없는이름")` |
| 상수 | 바꾸지 않기로 약속한 값. 대문자 이름 | `NEIS_API_KEY` |
| 가상환경 | 이 프로젝트만 쓰는 Python 작업 공간 | `.venv` 폴더 |
| pip | 라이브러리 설치 프로그램 | `python -m pip install ...` |
| PyPI | Python 라이브러리 공개 저장소 | Java의 Maven Central |
| 환경 변수 | 운영체제가 들고 있는 "이름=값" 쌍 | `NEIS_API_KEY=...` |
| `.env` | 환경 변수로 쓸 값을 적은 파일 (GitHub에 안 올림) | 프로젝트 최상위의 `.env` |
| Traceback | 오류가 어디를 거쳐 났는지 보여 주는 기록. 맨 아래 줄이 원인 | `ModuleNotFoundError: ...` |
| 스크립트 | 명령을 모아 둔 파일 | `Activate.ps1` |
| `__pycache__` | Python이 자동으로 만드는 임시 폴더 | `app\__pycache__` |

---

## 6. 개발자 질문

**질문: `.env.example`은 `git status`에 나와. 정상인 거지?**

정상입니다. `.env.example`은 GitHub에 **올리라고** 만든 파일입니다.

- 값 없이 항목 이름만 들어 있습니다.
- 저장소를 받은 사람이 어떤 값을 준비해야 하는지 알 수 있습니다.
- `.gitignore`의 `!.env.example` 규칙이 이 파일만 예외로 통과시킵니다.

그때 `git status --short`에는 `AM .env.example`로 나왔습니다.

| 글자 | 뜻 |
| --- | --- |
| `A` (Added) | 커밋할 목록에 올라가 있다 |
| `M` (Modified) | 목록에 올린 뒤 내용이 또 바뀌었다 (네이버웍스 항목을 Slack 항목으로 바꿈) |

정말 확인해야 할 것은 **`.env`가 목록에 없는 것**입니다. `.env`는 `.gitignore`의 `.env` 규칙 때문에 나오지 않았습니다.

---

## 7. 확인 문제

### 문제 1. 코드 읽기: 이 코드를 실행하면 화면에 무엇이 나올까요?

`NO_SUCH_NAME`이라는 환경 변수는 없다고 가정합니다.

```python
import os

key = os.getenv("NO_SUCH_NAME", "없음")
if key == "":
    print("비어 있음")
else:
    print("값:", key)
```

<details><summary>정답</summary>

```
값: 없음
```

- `NO_SUCH_NAME`이 없으므로 `os.getenv`는 기본값 `"없음"`을 돌려줍니다.
- `"없음" == ""`은 `False`이므로 `else` 블록이 실행됩니다.
- `print`에 쉼표로 두 값을 넣었으므로 `값:`과 `없음` 사이에 빈칸이 하나 들어갑니다.

(실제로 실행해 확인한 결과입니다.)

</details>

### 문제 2. 빈칸 채우기

`app/config.py`의 마지막 줄입니다. 빈칸 두 곳을 채우세요.

```python
NEIS_API_KEY: ____ = os.getenv("NEIS_API_KEY", ____)
```

<details><summary>정답</summary>

```python
NEIS_API_KEY: str = os.getenv("NEIS_API_KEY", "")
```

- 첫 번째 빈칸 `str`: 문자열이 들어간다는 타입 힌트입니다.
- 두 번째 빈칸 `""`: 환경 변수가 없을 때 `None` 대신 돌려받을 빈 문자열입니다. 이렇게 하면 `None`에 문자열을 이어 붙이다 나는 `TypeError`를 막을 수 있습니다.

</details>

### 문제 3. 작은 수정: 오류를 고쳐서 `입력됨`이 나오게 하세요

```python
key = "abc"
if key == ""
    print("비어 있음")
else:
print("입력됨")
```

<details><summary>정답</summary>

고칠 곳은 두 군데입니다.

```python
key = "abc"
if key == "":
    print("비어 있음")
else:
    print("입력됨")
```

1. 2번째 줄 끝에 콜론 `:`이 빠졌습니다.
2. 마지막 줄을 4칸 들여써야 `else`의 블록이 됩니다.

고친 코드의 실행 결과:

```
입력됨
```

참고: Python은 오류를 **한 번에 하나씩** 알려 줍니다. 실제로 실행해 보면 이렇습니다.

- 처음 실행하면 `SyntaxError: expected ':'`만 나옵니다.
- 콜론을 고치고 다시 실행하면 `IndentationError: expected an indented block after 'else' statement on line 4`가 나옵니다.

오류를 하나 고쳤는데 또 오류가 나도 당황하지 마세요. 하나씩 고쳐 나가면 됩니다.

</details>

---

## 이번 단계 핵심 정리

1. Python은 `python 파일명.py`로 실행하고, 파일의 맨 위 줄부터 한 줄씩 실행된다.
2. 가상환경(`.venv`)을 켜야 이 프로젝트용 Python과 라이브러리를 쓴다. 줄 앞의 `(.venv)`를 확인한다.
3. 라이브러리는 `python -m pip install`로 설치하고, `requirements.txt`에 버전과 함께 적는다.
4. 비밀값은 `.env`에만 두고, 코드는 `app/config.py`를 거쳐 `os.getenv`로 읽는다.
5. Python은 `{}` 대신 콜론 `:`과 들여쓰기로 블록을 만들고, 문장 끝에 `;`를 쓰지 않는다.
