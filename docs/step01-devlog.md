# 1단계 개발 기록: 환경 준비

## 이 문서를 다 읽으면 할 수 있게 되는 것

1. 1단계에서 무엇을 왜 만들었는지 설명할 수 있다.
2. 같은 개발 환경을 다른 컴퓨터에서 다시 만들 수 있다.
3. 1단계에서 실제로 겪은 문제와 해결 방법을 알 수 있다.

---

## 1. 목표

- 프로젝트 폴더 구조, 가상환경, `requirements.txt`, `.gitignore`, `.env.example`을 만든다.
- 비밀값을 `.env`에서 읽는 통로(`app/config.py`)를 만들고, 잘 읽히는지 확인한다.
- 개발자가 직접 해야 하는 일(NEIS 인증키 발급, 메신저 봇 등록)을 단계별로 안내한다.
- 커밋하고 GitHub에 push한다.

---

## 2. 한 일 (순서대로)

1. **문서 읽기와 질문**
   - CLAUDE.md와 기획서를 읽고, 프로젝트 요약과 지켜야 할 규칙을 정리해 개발자에게 확인받았다.
   - 개발자의 답: 가상환경은 `py`로 만들기, 최상위 폴더는 지금 폴더 그대로, CLAUDE.md와 기획서도 커밋에 넣기, GitHub 저장소는 비공개.
2. **환경 확인**
   - 운영체제는 Windows 11 Home이다.
   - `py --version`의 결과는 Python 3.13.16이다.
   - `python` 명령은 동작하지 않았다. (5번 문제 1)
   - PowerShell 실행 정책은 모든 범위가 `Undefined`였다. Windows 기본값인 Restricted가 적용되는 상태다. (5번 문제 2)
3. **가상환경 만들기**: `py -3.13 -m venv .venv`를 실행했다.
4. **라이브러리 설치**: `python-dotenv`를 설치했다. 설치된 버전(1.2.4)을 `requirements.txt`에 고정했다.
5. **공식 문서 확인**: NEIS와 네이버웍스 공식 문서를 읽고, 개발자용 안내서를 썼다.
6. **파일 작성**: 아래 파일들을 만들었다.
   - `.gitignore`, `.env.example`, `requirements.txt`
   - `app/__init__.py`, `app/config.py`, `check_setup.py`
   - `tests/.gitkeep`
7. **동작 확인**: 다섯 가지를 확인했다. (4번)
   - 설치 명령
   - `.env`가 없을 때와 있을 때
   - 가상환경 밖에서 실행했을 때
   - `.gitignore` 규칙
   - 가상환경 켜기
8. **메신저 변경**
   - 개발자가 "미성년자라 네이버웍스에 가입할 수 없다"고 알려 왔다.
   - Slack과 Discord의 나이 조건을 공식 약관에서 확인해 알렸다.
   - 개발자가 Slack을 골랐다. 그에 맞춰 `.env.example`과 안내서를 바꿨다. (5번 문제 3)
9. **Slack 앱 생성 방법 변경**
   - 개발자가 "앱 만들기 화면에 Blank app이 없고 AI agent와 Starter app만 있다"고 알려 왔다.
   - 공식 문서의 manifest 링크 방식으로 다시 안내했다. (5번 문제 4)
10. **개발자 작업 확인**
    - 개발자가 "1단계 안내서 완료"를 알려 왔다.
    - `.env`의 세 항목에 값이 들어 있는지만 확인했다. 값 자체는 출력하지 않았다.
11. **문서 작성과 커밋**: 학습 정리와 개발 기록을 쓴 뒤, 커밋 대상에 비밀 파일이 없는지 확인하고 커밋·push한다.

---

## 3. 바뀐 파일

모두 새로 만든 파일입니다.

| 파일 | 내용 |
| --- | --- |
| `.gitignore` | `.env`, `.env.*`(단 `.env.example`은 예외), 키 파일, `secrets/`, `.venv/`, `__pycache__/`, 로그, 편집기 설정을 Git에서 제외 |
| `.env.example` | `.env`에 적을 항목 이름 3개: `NEIS_API_KEY`, `SLACK_BOT_TOKEN`, `SLACK_SIGNING_SECRET` |
| `requirements.txt` | `python-dotenv==1.2.4` |
| `app/__init__.py` | `app` 폴더를 패키지로 만드는 파일 (설명 주석만) |
| `app/config.py` | `.env`를 읽고 `NEIS_API_KEY`를 꺼내는 파일 |
| `check_setup.py` | Python 버전·위치와 인증키 입력 여부를 출력하는 확인용 파일 |
| `tests/.gitkeep` | 빈 `tests` 폴더를 Git에 남기기 위한 빈 파일 |
| `docs/step01-setup-guide.md` | 개발자가 직접 할 일 안내서 (실행 정책, 가상환경, `.env`, NEIS, Slack) |
| `docs/step01-learning.md` | 1단계 학습 정리 |
| `docs/step01-devlog.md` | 이 문서 |
| `CLAUDE.md`, `급식·학사일정 알림 봇 프로젝트 기획서.md` | 내용은 그대로 두고 첫 커밋에 포함 (개발자 결정) |

`.venv/` 폴더도 만들었지만 `.gitignore`로 제외했습니다.

---

## 4. 실행 방법과 결과

### 새 컴퓨터에서 환경을 다시 만드는 방법

```powershell
cd C:\neis_groupware_bot
py -3.13 -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
Copy-Item .env.example .env
python check_setup.py
```

`.env`에는 값을 직접 넣어야 합니다. 방법은 [안내서](step01-setup-guide.md)에 있습니다.

> 에이전트는 가상환경을 켜지 않고 `.venv\Scripts\python.exe`를 직접 지정해 실행했습니다.
> 가상환경을 켠 상태에서 `python`을 쓰는 것과 같은 Python입니다.

### 결과 1: 라이브러리 설치

```
Collecting python-dotenv
  Downloading python_dotenv-1.2.4-py3-none-any.whl.metadata (29 kB)
Downloading python_dotenv-1.2.4-py3-none-any.whl (23 kB)
Installing collected packages: python-dotenv
Successfully installed python-dotenv-1.2.4
```

`requirements.txt`로 다시 설치하면 아래처럼 나옵니다.

```
Requirement already satisfied: python-dotenv==1.2.4 in .\.venv\Lib\site-packages (from -r requirements.txt (line 7)) (1.2.4)
```

### 결과 2: `.env`가 없을 때

```
Python 버전: 3.13.16 (tags/v3.13.16:cbc944f, Sep 30 2026, 19:17:50) [MSC v.1944 64 bit (AMD64)]
Python 위치: C:\neis_groupware_bot\.venv\Scripts\python.exe
NEIS_API_KEY: 비어 있음 (.env 파일을 확인하세요)
```

### 결과 3: 시험용 `.env`를 만들었을 때

`NEIS_API_KEY=dummy-value-for-test` 한 줄만 넣은 `.env`를 만들어 실행했습니다. 실행한 뒤 바로 지웠습니다.

```
NEIS_API_KEY: 입력됨
```

`app/config.py`는 `app` 폴더 안에 있습니다. 그래도 프로젝트 최상위의 `.env`를 찾아 읽는다는 것을 확인했습니다.

### 결과 4: 가상환경 밖의 Python으로 실행했을 때 (`py check_setup.py`)

```
ModuleNotFoundError: No module named 'dotenv'
```

라이브러리는 가상환경에만 설치되어 있으므로, 예상한 결과입니다.

### 결과 5: `.gitignore` 규칙 확인

```powershell
git check-ignore -v --no-index .env .env.txt .env.local secrets/private_20261104.key private_20261104.key some.pem .venv/Scripts/python.exe app/__pycache__/config.cpython-313.pyc logs/bot.log
```

```
.gitignore:9:.env	.env
.gitignore:11:.env.*	.env.txt
.gitignore:11:.env.*	.env.local
.gitignore:18:secrets/	secrets/private_20261104.key
.gitignore:15:*.key	private_20261104.key
.gitignore:16:*.pem	some.pem
.gitignore:21:.venv/	.venv/Scripts/python.exe
.gitignore:24:__pycache__/	app/__pycache__/config.cpython-313.pyc
.gitignore:29:logs/	logs/bot.log
```

- 모든 경로가 무시 대상으로 나왔습니다.
- 줄 번호는 확인할 때의 `.gitignore` 기준입니다. 그 뒤 설명 주석이 한 줄 늘어서, 지금 파일과는 줄 번호가 조금 다를 수 있습니다.
- `.env.example`은 `!.env.example` 규칙 때문에 무시되지 않는 것도 확인했습니다.

### 결과 6: 가상환경 켜기

개발자 컴퓨터와 같은 실행 정책(Restricted)으로 실행했을 때:

```
File C:\neis_groupware_bot\.venv\Scripts\Activate.ps1 cannot be loaded because running scripts is disabled on this system.
```

RemoteSigned로 실행했을 때:

```
Python 3.13.16
C:\neis_groupware_bot\.venv\Scripts\python.exe
```

- 가상환경이 켜졌고, `python`이 가상환경의 Python을 가리켰습니다.
- `deactivate`로 끈 뒤에는 다시 `C:\Users\...\WindowsApps\python.exe`를 가리켰습니다.

### 결과 7: 개발자 작업 확인 (값은 출력하지 않음)

개발자가 안내서를 끝낸 뒤 확인한 결과입니다.

```
NEIS_API_KEY: 입력됨
SLACK_BOT_TOKEN filled: True
SLACK_BOT_TOKEN starts with xoxb-: True
SLACK_SIGNING_SECRET filled: True
```

`git status`에 `.env`가 나오지 않는 것도 확인했습니다. `.gitignore` 9번째 줄의 `.env` 규칙이 적용되었습니다.

### 결과 8: 커밋 전 비밀 파일 점검

커밋 대상 목록에 `.env`, `.env.*`(`.env.example` 제외), `*.key`, `*.pem`, `secrets/`, `.venv/`, `__pycache__`가 하나도 없는지 확인했습니다.
결과는 0건이었습니다.

---

## 5. 발생한 문제와 해결

### 문제 1. `python` 명령이 동작하지 않음

- **에러**

  ```
  Python was not found; run without arguments to install from the Microsoft Store, or disable this shortcut from Settings > Apps > Advanced app settings > App execution aliases.
  ```

- **원인**
  - Python을 설치할 때 PATH(명령 이름으로 프로그램을 찾는 폴더 목록)에 Python이 등록되지 않았다.
  - 그래서 Windows가 Microsoft Store 안내용 `python.exe`를 대신 실행했다.
  - Python 런처 `py`는 설치되어 있었다. `py --version`의 결과는 `Python 3.13.16`이었다.
- **해결**
  - Python을 다시 설치하지 않았다. 대신 `py -3.13 -m venv .venv`로 가상환경을 만들었다. (개발자 동의)
  - 가상환경을 켜면 그 안에서는 `python`이 정상 동작한다.

### 문제 2. 가상환경을 켜는 스크립트가 막힘

- **확인 방법**
  - 개발자 컴퓨터의 실행 정책은 모든 범위가 `Undefined`라서, Windows 기본값인 Restricted가 적용된다.
  - 에이전트가 쓰는 PowerShell은 정책이 Bypass라서 그대로는 같은 상황이 생기지 않는다.
  - 그래서 `powershell.exe -ExecutionPolicy Restricted`로 개발자 컴퓨터와 같은 조건을 만들어 확인했다.
- **에러**

  ```
  File C:\neis_groupware_bot\.venv\Scripts\Activate.ps1 cannot be loaded because running scripts is disabled on this system.
  ```

- **해결**
  - 개발자가 직접 `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`를 실행하도록 안내했다. (안내서 1번)
  - Python 공식 문서도 같은 방법을 안내한다.
  - RemoteSigned 조건에서 가상환경이 켜지는 것을 확인했다. (4번 결과 6)

### 문제 3. 네이버웍스에 가입할 수 없음

- **상황**: 개발자가 미성년자라서 네이버웍스에 가입할 수 없다고 알려 왔다.
- **원인**: 서비스 가입 나이 조건 때문이다. 에이전트는 이 조건을 미리 확인하지 않고 네이버웍스 안내서를 썼다.
- **해결**
  - CLAUDE.md 진행 규칙에 따라 우회하지 않았다. 대신 개발자에게 상황을 설명하고 Slack으로 바꿀지 물었다.
  - 그 전에 대안 서비스의 나이 조건을 공식 약관에서 확인했다.
    - Slack: 만 16세 미만은 쓸 수 없다. (Slack User Terms of Service)
    - Discord: 기본 13세 이상이고 나라별 법정 나이를 따른다. 한국 기준은 공식 문서로 확인하지 못했다.
  - 개발자가 Slack을 골랐다.
  - `.env.example`의 네이버웍스 항목 6개를 Slack 항목 2개로 바꿨다.
  - 안내서의 네이버웍스 부분(5~8번)을 Slack 절차로 다시 썼다.
- **배운 점**: 앞으로 외부 서비스(터널 도구 등)를 안내하기 전에는 가입 나이 조건부터 확인한다.

### 문제 4. Slack 앱 만들기 화면이 공식 문서와 다름

- **상황**
  - 공식 문서(Creating an app from app settings)는 "Blank app"을 고르라고 안내한다.
  - 그런데 개발자 화면에는 "AI agent"와 "Starter app"만 있었다.
- **원인**: Slack 화면이 바뀐 것으로 보인다. "Starter app"이 무엇을 미리 켜 두는지는 공식 문서에 나와 있지 않다.
- **해결**
  - 공식 문서(Configuring apps with app manifests)에 나온 manifest 링크 방식을 안내했다.
    - 주소는 `https://api.slack.com/apps?new_app=1&manifest_json=<설정>` 모양이다.
    - 이 주소로 들어가면 그 설정으로 앱 만들기가 바로 시작된다.
  - 링크에 넣을 설정(JSON)은 Python으로 URL 인코딩했다. 다시 풀었을 때 원래 설정과 같은지도 확인했다(`round-trip ok: True`).
  - 이 안내 뒤 개발자가 안내서 완료를 알려 왔다.

### 문제 5. 공식 문서만으로 확인하지 못한 것

아래 항목은 안내서에 "확인하지 못했다"고 적어 두었습니다.

- NEIS 인증키 신청서의 칸 이름: 로그인해야 보이는 화면이라 확인하지 못했다.
- Slack 채널 만들기 버튼 이름: 공식 도움말에서 찾지 못했다.
- Slack Signing Secret을 보이게 하는 버튼 이름: 공식 문서에 없었다.

### 문제 6. 커밋 준비 중 줄바꿈 경고 (오류 아님)

`git add`를 실행했을 때 아래 경고가 파일마다 나왔습니다.

```
warning: in the working copy of 'app/config.py', LF will be replaced by CRLF the next time Git touches it
```

- **원인**
  - 이 컴퓨터의 Git 설정이 `core.autocrlf=true`이다.
  - 그래서 Git이 줄바꿈 문자를 Windows 방식(CRLF)으로 바꾸겠다고 알린 것이다.
- **해결**: 동작에는 영향이 없는 알림이라 그대로 두었다.

---

## 6. 결정한 것과 이유

| 결정 | 다른 선택지 | 고른 이유 |
| --- | --- | --- |
| 지금 폴더(`C:\neis_groupware_bot`)를 최상위로 사용 | CLAUDE.md 권장대로 `lunch-bot/` 폴더를 새로 만들기 | 저장소가 이미 이 폴더에 연결되어 있다. 폴더를 한 겹 더 만들 이유가 없다. (개발자 결정) |
| `py -3.13 -m venv .venv`로 가상환경 생성 | Python을 PATH 등록 옵션으로 다시 설치 | 재설치 없이 바로 진행할 수 있다. 가상환경 안에서는 `python`이 동작한다. (개발자 결정) |
| 라이브러리는 단계마다 필요할 때 `requirements.txt`에 추가 | 기술 스택 전체를 지금 한 번에 추가 | CLAUDE.md 코드 규칙("그 단계에 꼭 필요한 만큼만")에 맞다. 질문에 따로 답이 없어 추천안을 적용했다. |
| 버전을 `==`로 고정 | 버전 없이 이름만 적기 | 언제 누가 설치해도 같은 버전이 깔린다. |
| 1단계에 `app/config.py`를 만듦 | 2단계에서 처음 만들기 | `.env`가 실제로 읽히는지 1단계에서 확인할 수 있다. 비밀값을 읽는 곳을 처음부터 한 곳으로 모은다. |
| `config.py`는 아직 `NEIS_API_KEY`만 읽음 | Slack 항목까지 지금 읽기 | Slack 값은 4단계부터 쓴다. 쓰지 않는 코드를 미리 넣지 않는다. |
| `check_setup.py`를 최상위에 둠 (CLAUDE.md 권장 구조에 없는 파일) | `app/` 안에 두기 | 최상위에 있어야 `python check_setup.py` 한 줄로 실행되고, `from app.config import ...`가 바로 동작한다. |
| `app/__init__.py` 추가 | 파일 없이 폴더만 두기 | 일반 패키지로 만들어 import 동작을 분명하게 한다. 파일 역할을 학습 정리에서 설명할 수 있다. |
| `tests/.gitkeep` 추가 | 3단계까지 `tests` 폴더 만들지 않기 | CLAUDE.md 1단계 할 일에 폴더 구조가 있다. Git은 빈 폴더를 저장하지 않는다. |
| `.gitignore`에 `.env.*`와 `!.env.example` | `.env` 한 줄만 | 메모장이 `.env.txt`로 저장하는 실수까지 막는다. |
| `.gitignore`에 `*.key`, `*.pem`, `secrets/` 유지 | Slack은 키 파일이 없으니 빼기 | 나중에 키 파일을 다루더라도 실수로 올라가지 않게 미리 막아 둔다. |
| 메신저를 네이버웍스에서 **Slack**으로 변경 | Discord, 메신저 결정 미루기 | 개발자가 미성년자라 네이버웍스에 가입할 수 없다. Slack은 CLAUDE.md가 정한 대안이고 개발자가 직접 골랐다. 전송 부분만 바꿔 끼울 수 있는 구조는 그대로 유지한다. |
| CLAUDE.md와 기획서의 네이버웍스 내용은 고치지 않음 | 문서를 Slack 기준으로 고치기 | 두 문서는 개발자가 쓴 원본이다. 바뀐 결정은 이 개발 기록에 남긴다. (CLAUDE.md 진행 규칙) |
| `.env.example`의 Slack 항목은 2개만 (`SLACK_BOT_TOKEN`, `SLACK_SIGNING_SECRET`) | 채널 ID, 관리자 ID까지 미리 넣기 | 1단계에서 받는 값은 이 둘뿐이다. 채널 ID는 4단계, 관리자 ID는 5단계에서 필요할 때 추가한다. |
| Slack 앱을 manifest 링크로 생성 | "Starter app"을 고르고 나중에 설정 고치기 | "Starter app"이 무엇을 미리 켜 두는지 공식 문서에 없다. manifest를 쓰면 필요한 설정만 정확히 넣을 수 있다. |
| manifest에서 `socket_mode_enabled: false` | Socket Mode 켜기 | 이 프로젝트의 목적은 콜백 주소로 요청을 받고 서명을 검증하는 구조를 직접 만들어 보는 것이다. Socket Mode는 그 과정을 건너뛴다. |
| manifest에서 `token_rotation_enabled: false` | 토큰 자동 교체 켜기 | 토큰 발급·만료 처리는 4단계(메시지 전송)에서 정한다. 그때까지는 가장 단순한 상태로 둔다. |
| 개발자용 안내서를 별도 문서(`step01-setup-guide.md`)로 작성 | 개발 기록 안에 넣기 | 개발자가 화면을 보며 따라 할 순서가 길다. 개발자가 "추가로 필요한 문서는 알아서" 만들라고 했다. |
| CLAUDE.md와 기획서를 첫 커밋에 포함 | 커밋하지 않기 | 저장소만 봐도 프로젝트 의도와 진행 규칙을 알 수 있다. (개발자 결정) |
| pip를 새 버전으로 올리지 않음 | `python -m pip install --upgrade pip` | 지금 버전으로 문제가 없다. 이 단계에 필요하지 않다. |

---

## 7. 다음 단계에서 할 일 (2단계: 데이터 조회)

1. `requests` 라이브러리를 설치하고 `requirements.txt`에 추가한다.
2. NEIS 공식 문서에서 아래 내용을 확인한다.
   - 학교 코드 조회 API(학교기본정보)
   - 급식 API(급식식단정보)의 주소, 파라미터, 응답 필드
3. 개발자의 학교 코드(교육청 코드, 학교 코드)를 찾는 방법을 안내한다. 학교 코드는 비밀값은 아니지만, 설정값이라 `.env`에 둘지 정한다.
4. requests로 급식 API를 호출해 JSON 원본을 확인한다.
   - 방학·주말에는 데이터가 없을 수 있다. 그래서 급식이 있던 지난 날짜로도 조회해 본다. (기획서 7번 위험 요소)

---

## 확인한 공식 문서

**NEIS**

- 개발자 가이드: https://open.neis.go.kr/portal/guide/apiGuidePage.do
- Open API 소개: https://open.neis.go.kr/portal/guide/apiIntroPage.do
- 인증키 신청(로그인 필요해서 내용 확인 못 함): https://open.neis.go.kr/portal/guide/actKeyPage.do
- 서비스 이용약관: https://open.neis.go.kr/portal/userAgreementPage.do

**네이버웍스** (조사했지만 문제 3 때문에 사용하지 않음)

- 봇 개요: https://developers.worksmobile.com/kr/docs/bot
- Developer Console: https://developers.worksmobile.com/kr/docs/developer-console
- 인증: https://developers.worksmobile.com/kr/docs/auth
- 서비스 계정 인증(JWT): https://developers.worksmobile.com/kr/docs/auth-jwt
- Scope 목록: https://developers.worksmobile.com/kr/docs/auth-scope
- 관리자 도움말(Bot): https://help.worksmobile.com/ko/admin-guides/manage-service/bot/
- 요금제: https://naver.worksmobile.com/pricing/

**Slack**

- 사용자 약관(나이 조건): https://slack.com/terms-of-service/user
- 워크스페이스 만들기: https://slack.com/help/articles/206845317-Create-a-Slack-workspace
- 앱 설정 화면으로 앱 만들기: https://docs.slack.dev/app-management/quickstart-app-settings/
- Bolt for Python 앱 만들기: https://docs.slack.dev/tools/bolt-python/creating-an-app/
- manifest로 앱 만들기: https://docs.slack.dev/app-manifests/configuring-apps-with-app-manifests/
- manifest 항목 설명: https://docs.slack.dev/reference/app-manifest/
- `chat:write` scope: https://docs.slack.dev/reference/scopes/chat.write/
- `chat.postMessage`: https://docs.slack.dev/reference/methods/chat.postMessage/
- 요청 검증(Signing Secret): https://docs.slack.dev/authentication/verifying-requests-from-slack/

**Discord** (대안으로 나이 조건만 확인)

- 이용약관: https://discord.com/terms

**Python**

- venv 문서(실행 정책 안내): https://docs.python.org/3/library/venv.html

---

## 이번 단계 핵심 정리

1. `py -3.13 -m venv .venv`로 가상환경을 만들고, `python-dotenv==1.2.4`를 `requirements.txt`에 고정했다.
2. 비밀값은 `.env`에서 `app/config.py`를 거쳐 읽는다. `.env`와 키 파일은 `.gitignore`로 막혀 있다.
3. 메신저는 네이버웍스(미성년자 가입 불가) 대신 Slack을 쓴다. Slack 앱은 manifest 링크로 만들었다.
4. 개발자가 NEIS 인증키와 Slack 봇 토큰, Signing Secret을 `.env`에 넣었다. 값은 출력하지 않고 확인했다.
5. 다음 단계는 requests로 NEIS 급식 API를 호출해 JSON 원본을 확인하는 것이다.
