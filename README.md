# 급식·학사일정 알림 봇 (NEIS + Slack)

교육청 공공 API(NEIS)에서 우리 학교의 급식과 학사일정을 가져와, Slack 봇으로 알려 주는 프로그램입니다.

- 매일 아침 정해진 시각에 오늘 급식과 오늘의 학사일정을 Slack 채널에 보냅니다.
- 봇에게 `오늘 급식`, `내일 급식`, `이번 주 일정`을 보내면 답장합니다.
- API 호출이나 전송이 실패하면 관리자 채널로 오류를 알립니다.

Python을 처음 배우는 고등학생 개발자의 학습용 프로젝트입니다. 그룹웨어 연동의 세 가지 구조(API 호출, 콜백 수신, 인증)를 작은 규모로 모두 구현해 보는 것이 목표입니다. 단계별 학습 정리와 개발 기록은 [`docs/`](docs/)에 있습니다.

> 처음 계획은 네이버웍스 봇이었지만, 개발자가 미성년자라 가입할 수 없어서 **Slack**으로 바꿨습니다. ([막혔던 문제](#막혔던-문제와-해결-과정) 3번)

---

## 할 수 있는 일

| 기능 | 방향 | 동작 |
| --- | --- | --- |
| 정기 알림 | 프로그램 → Slack | 매일 아침 7시 30분(바꿀 수 있음)에 오늘 급식 + 오늘의 학사일정을 급식 알림 채널로 보냄 |
| 명령어 답장 | 사용자 → Slack → 프로그램 → Slack | 봇과의 1:1 대화로 보낸 명령어에 답함 |
| 오류 알림 | 프로그램 → Slack | NEIS 조회나 Slack 전송이 실패하면 관리자 채널로 알림 |

### 정기 알림 예시

```
[11월 5일(목) 중식]
흑미밥 / 부대찌개 / 호박볶음 / 오지치즈스틱 / 고등어구이 / 백김치

[오늘의 학사일정]
과학 하이챌린지(1,2)
```

- 메뉴 뒤의 알레르기 번호는 메시지에서 빼고 따로 보관합니다.
- 급식이 없는 날(주말·방학·공휴일)은 `오늘은 급식이 없습니다.`라고 보냅니다. 오류가 아닌 정상 상황입니다.
- 학사일정의 `토요휴업일`은 매주 들어 있어서 빼고 보여 줍니다.

### 명령어

봇(`lunch-bot`)과의 **1:1 대화**로 보냅니다. 앞뒤 공백과 띄어쓰기 차이는 무시합니다. (`내일급식` = `내일 급식`)

| 명령어 | 답장 |
| --- | --- |
| `오늘 급식` | 오늘 중식 메뉴 |
| `내일 급식` | 내일 중식 메뉴 |
| `이번 주 일정` | 이번 주(월~일) 학사일정 |
| `도움말` 또는 그 밖의 말 | 사용할 수 있는 명령어 안내 |

---

## 구조

```
 ① 정기 알림: 매일 07:30
    scheduler.py ──┐
                   ├──▶ notifier.py ──▶ neis.py ──▶ formatter.py ──▶ sender.py ──▶ Slack ──▶ 사용자
    server.py ─────┘    (알림·답장)     (NEIS 조회)   (메시지 만들기)    (메시지 보내기)
       ▲
       │  서명 검증(auth.py) → 명령어 해석(commands.py) → Slack에 바로 200 응답, 답장은 뒤에서
       │
 ② 명령어: 사용자 ──▶ Slack ──▶ 터널(Cloudflare) ──▶ 127.0.0.1:8000/slack/events
```

- `main.py`가 스케줄러(`scheduler.py`)와 콜백 서버(`server.py`)를 **한 프로그램**으로 함께 실행합니다. 스케줄러는 따로 일하는 줄(스레드)에서 돕니다.
- 두 흐름 모두 같은 조회(`neis.py`)·변환(`formatter.py`)·전송(`sender.py`) 모듈을 씁니다. 흐름마다 따로 만들지 않았습니다.
- `sender.py`는 `auth.py`에서 Slack 토큰을 받아 씁니다. 토큰은 12시간마다 만료되고, 프로그램이 알아서 새로 받습니다(토큰 자동 교체).
- Slack은 이벤트를 보낸 뒤 3초 안에 응답을 받아야 합니다. 그래서 서버는 먼저 응답하고, 답장은 그 뒤에 보냅니다.

### 폴더 구조

```
neis_groupware_bot/
├── main.py                 # 실행 파일: 스케줄러 + 콜백 서버 (python main.py)
├── app/
│   ├── config.py           # .env 읽기
│   ├── log.py              # 로그 파일(logs/bot.log) 설정
│   ├── neis.py             # NEIS 조회 (급식, 학사일정, 학교 찾기), 실패 시 한 번 재시도
│   ├── formatter.py        # 데이터 변환 (알레르기 번호, <br/>, 날짜, 학사일정 묶기)
│   ├── auth.py             # Slack 토큰 교환·재발급·저장, 요청 서명 검증
│   ├── sender.py           # Slack 메시지 전송, 토큰 오류 시 새 토큰으로 재전송
│   ├── notifier.py         # 정기 알림·명령어 답장을 끝까지 처리, 실패 시 관리자 알림
│   ├── commands.py         # 명령어 해석과 답장 글 만들기
│   ├── server.py           # 콜백 서버 (FastAPI)
│   └── scheduler.py        # 매일 정기 알림 예약 (APScheduler)
├── tests/                  # pytest 테스트 (68개)
├── docs/                   # 단계별 학습 정리·개발 기록, 1단계 준비 안내서
├── check_setup.py          # 1단계 환경 확인
├── find_school.py          # 학교 이름으로 NEIS 학교 코드 찾기
├── show_meal_json.py       # 급식 원본 JSON 보기
├── show_lunch_message.py   # 급식 메시지 모양 미리 보기 (보내지 않음)
├── setup_slack_token.py    # 처음 한 번: 봇 토큰을 자동 교체 토큰으로 바꿔 저장
├── reinstall_slack_app.py  # Slack 앱 권한을 바꾼 뒤 다시 설치하고 새 토큰 저장
├── send_lunch_message.py   # 원하는 날짜의 급식 알림을 직접 한 번 보내기
├── .env.example            # .env에 적을 항목 이름 (값은 비어 있음)
├── requirements.txt        # 필요한 라이브러리와 버전
└── pytest.ini              # pytest 설정
```

`.env`(비밀값), `secrets/`(Slack 토큰 파일), `logs/`(로그)는 `.gitignore`로 저장소에서 뺐습니다.

CLAUDE.md의 권장 구조에 세 파일을 더했습니다.
- `app/log.py`, `app/notifier.py`: 5단계에서 추가. 로그 설정을 한 곳에 모으고, 정기 알림과 수동 전송이 같은 흐름을 쓰게 함
- `main.py`: 9단계에서 추가. 스케줄러와 콜백 서버를 한 프로그램으로 실행함

자세한 이유는 step05, step09 개발 기록에 있습니다.

---

## 실행 방법

Windows PowerShell 기준입니다.

### 준비물

| 준비물 | 설명 |
| --- | --- |
| Python 3.11 이상 | 이 프로젝트는 3.13.16으로 만들었습니다 |
| NEIS 인증키 | [NEIS 교육정보 개방 포털](https://open.neis.go.kr)에서 발급 |
| Slack 워크스페이스와 앱 | Slack은 만 16세 이상만 쓸 수 있습니다 (Slack 이용약관) |
| cloudflared | 명령어 답장을 받을 때만 필요합니다. 정기 알림에는 필요 없습니다 |

인증키 발급과 Slack 앱 만들기는 [`docs/step01-setup-guide.md`](docs/step01-setup-guide.md)에 화면 순서대로 적어 두었습니다.

### 1. 설치 (처음 한 번)

```powershell
cd C:\neis_groupware_bot
py -3.13 -m venv .venv                         # 가상환경 만들기
.venv\Scripts\Activate.ps1                     # 가상환경 켜기
python -m pip install -r requirements.txt      # 라이브러리 설치
Copy-Item .env.example .env                    # .env 만들기
```

`Activate.ps1`이 "running scripts is disabled"로 막히면, 처음 한 번만 아래를 실행합니다.

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### 2. `.env` 채우기

`.env`를 열어 `=` 뒤에 값을 적습니다. 따옴표와 띄어쓰기 없이 적습니다.

| 항목 | 어디서 | 처음 쓰는 단계 |
| --- | --- | --- |
| `NEIS_API_KEY` | NEIS 포털에서 발급받은 인증키 | 2 |
| `NEIS_OFFICE_CODE`, `NEIS_SCHOOL_CODE` | `python find_school.py` 결과의 `ATPT_OFCDC_SC_CODE`, `SD_SCHUL_CODE` | 2 |
| `SLACK_BOT_TOKEN` | Slack 앱 설정 → OAuth & Permissions의 봇 토큰(`xoxb-`) | 4 |
| `SLACK_CLIENT_ID`, `SLACK_CLIENT_SECRET` | Slack 앱 설정 → Basic Information → App Credentials | 4 |
| `SLACK_CHANNEL_ID` | 급식 알림 채널의 ID (`C`로 시작) | 4 |
| `SLACK_ADMIN_CHANNEL_ID` | 오류 알림 채널의 ID | 5 |
| `SLACK_SIGNING_SECRET` | Slack 앱 설정 → Basic Information → Signing Secret | 7 |
| `NOTIFY_HOUR`, `NOTIFY_MINUTE` | 정기 알림 시각. 숫자만 적고, 비워 두면 7시 30분 | 9 |

### 3. Slack 앱 설정 (요약)

| 설정 | 값 | 자세한 내용 |
| --- | --- | --- |
| Bot Token Scopes | `chat:write`, `im:history` | step01 안내서, step06 개발 기록 |
| 토큰 자동 교체(Token Rotation) | 켜기. 켜려면 Redirect URL이 필요해서 `https://localhost/slack/oauth/callback` 등록 | step04 개발 기록 |
| App Home → Messages Tab | 켜기 (봇과의 1:1 대화) | step06 개발 기록 |
| Event Subscriptions | Request URL: `https://(터널 주소)/slack/events`, 구독: `message.im` | step06 개발 기록 |
| 채널 | 급식 알림 채널과 관리자 채널에 봇 초대 | step01 안내서 |

### 4. Slack 토큰 준비 (처음 한 번)

```powershell
python setup_slack_token.py
```

`.env`의 봇 토큰을 "12시간마다 바뀌는 토큰 + refresh token"으로 바꿔 `secrets/slack_tokens.json`에 저장합니다. 그다음부터는 프로그램이 알아서 새 토큰을 받습니다.

나중에 앱 권한(scope)을 바꿨다면 `python reinstall_slack_app.py`로 다시 설치합니다.

### 5. 실행

```powershell
python main.py
```

```
정기 알림 다음 실행 시각: 2026-11-06 07:30:00+09:00
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

- 다음 알림 시각이 나오면 잘 켜진 것입니다.
- 끌 때는 이 창에서 **Ctrl+C**를 누릅니다.
- 정기 알림은 이 프로그램이 켜져 있어야 나갑니다. 정해진 시각을 1시간 넘게 놓치면 그날 알림은 건너뜁니다.
- 코드를 고쳤다면 Ctrl+C로 끄고 다시 켭니다. (`--reload`는 Windows에서 멈출 수 있어서 쓰지 않습니다)

### 6. 명령어 답장 받기 (터널)

다른 PowerShell 창에서 터널을 켭니다.

```powershell
& "$HOME\Downloads\cloudflared-windows-amd64.exe" tunnel --url http://127.0.0.1:8000
```

1. 화면에 나온 `https://(이름).trycloudflare.com` 주소를 복사합니다.
2. Slack 앱 설정 → Event Subscriptions → Request URL에 `https://(이름).trycloudflare.com/slack/events`를 넣습니다. **`/slack/events`를 꼭 붙입니다.**
3. **Verified**가 뜨면 **Save Changes**를 누릅니다.
4. Slack에서 봇과의 1:1 대화로 `오늘 급식`을 보내 봅니다.

이 터널(Quick Tunnel)은 계정 없이 쓸 수 있는 대신, **켤 때마다 주소가 바뀌고** 가끔 끊깁니다. 그때마다 1~3을 다시 합니다.

### 7. 테스트

```powershell
python -m pytest
```

```
============================= 68 passed =============================
```

테스트는 NEIS와 Slack에 요청을 보내지 않습니다. 변환 규칙, 날짜 계산, 명령어 해석, 서명 검증, 예약 설정을 확인합니다.

### 그 밖의 실행 파일

| 파일 | 하는 일 |
| --- | --- |
| `python check_setup.py` | Python 버전과 위치(가상환경인지), `.env`에 NEIS 인증키가 들어갔는지 확인합니다 |
| `python find_school.py` | 학교 이름으로 학교 코드를 찾습니다 |
| `python show_meal_json.py` | 급식 원본 JSON을 봅니다 |
| `python show_lunch_message.py` | 급식 메시지 모양을 미리 봅니다 (보내지 않음) |
| `python send_lunch_message.py` | 입력한 날짜의 급식 알림을 급식 알림 채널로 한 번 보냅니다 |

---

## 알아 둘 점

- **비밀 정보**: NEIS 인증키, Slack 토큰·시크릿은 `.env`와 `secrets/`에만 있습니다. 코드와 문서에는 없습니다. 로그에도 남기지 않습니다. (외부 요청 오류는 종류 이름만 기록합니다)
- **로그**: 모든 요청과 오류는 시각과 함께 `logs/bot.log`에 남습니다.
- **같은 이벤트는 한 번만**: Slack이 같은 이벤트를 다시 보내도 한 번만 답합니다. 이 기억은 프로그램이 켜져 있는 동안만 유지됩니다.
- **봇의 메시지는 무시**: 봇이 보낸 답장도 이벤트로 들어오지만 명령어로 보지 않습니다. 그래서 봇이 자기 답장에 또 답하지 않습니다.
- **PC가 켜져 있어야 함**: 이 프로그램은 개발자의 PC에서 돕니다. PC나 `main.py`가 꺼져 있으면 알림도 답장도 없습니다.

---

## 막혔던 문제와 해결 과정

각 단계 개발 기록의 "발생한 문제와 해결"을 모았습니다. 자세한 에러 메시지와 확인 과정은 단계별 개발 기록(`docs/stepNN-devlog.md`)에 있습니다.

### 환경 준비

| 번호 | 단계 | 문제 | 원인 | 해결 |
| --- | --- | --- | --- | --- |
| 1 | 01 | `python` 명령이 "Python was not found"로 동작하지 않음 | Python이 PATH에 등록되지 않아, Windows가 Microsoft Store 안내용 `python.exe`를 실행함 | Python 런처로 가상환경을 만듦: `py -3.13 -m venv .venv`. 가상환경 안에서는 `python`이 동작함 |
| 2 | 01 | `Activate.ps1`이 "running scripts is disabled"로 막힘 | Windows 기본 실행 정책(Restricted) | 개발자가 `Set-ExecutionPolicy RemoteSigned -Scope CurrentUser` 실행 |
| 3 | 01 | 네이버웍스에 가입할 수 없음 | 개발자가 미성년자. 에이전트가 가입 나이 조건을 미리 확인하지 않음 | 우회하지 않고 대안의 나이 조건을 공식 약관에서 확인한 뒤 Slack(만 16세 이상)으로 변경. 이후 외부 서비스는 나이 조건부터 확인 |
| 4 | 01 | Slack 앱 만들기 화면에 공식 문서의 "Blank app"이 없음 | Slack 화면이 바뀐 것으로 보임 | 공식 문서의 manifest 링크(`?new_app=1&manifest_json=...`)로 설정을 미리 채워 앱을 만듦 |
| 5 | 01 | 에이전트 환경에서 `git push` 실패 | 비공개 저장소라 GitHub 로그인이 필요한데, 에이전트 환경은 로그인 창을 띄울 수 없음 | 개발자가 PowerShell에서 직접 push해 로그인 정보를 저장함 |

### NEIS 조회와 변환

| 번호 | 단계 | 문제 | 원인 | 해결 |
| --- | --- | --- | --- | --- |
| 6 | 02 | NEIS 포털의 API 명세 표가 비어 보임 | 표 내용을 페이지 스크립트가 나중에 채우는데, 웹 페이지 읽기 도구는 스크립트를 실행하지 않음 | 스크립트가 쓰는 주소(`selectOpenApiMeta.do`)로 공식 명세 데이터를 직접 받음 |
| 7 | 02 | 한글 학교 이름으로 학교를 찾지 못함 (시험 중) | PowerShell 5.1이 파이프로 넘기는 글자 앞에 BOM(`\ufeff`)을 붙임 | 시험할 때 Python에서 BOM 없는 글자를 넘김. 키보드로 직접 입력할 때는 생기지 않아 코드는 그대로 둠 |
| 8 | 03 | `pytest`만 치면 `ModuleNotFoundError: No module named 'app'` | `pytest`는 `python -m pytest`와 달리 프로젝트 폴더를 모듈 찾는 곳에 넣지 않음 | `pytest.ini`에 `pythonpath = .` 추가 |
| 9 | 03→05 | 인증키 오류(`ERROR-290`)도 "오늘은 급식이 없습니다."로 보임 | 데이터 없음(`INFO-200`)과 오류를 구별하지 않음 | 5단계에서 `neis.py`가 결과 코드를 먼저 확인하고, 오류면 재시도 후 `NeisError`로 알림 |

### Slack 토큰과 오류 처리

| 번호 | 단계 | 문제 | 원인 | 해결 |
| --- | --- | --- | --- | --- |
| 10 | 04 | 토큰 자동 교체를 켜려니 Redirect URL이 필요하다고 함 | Slack 화면의 조건 (공식 문서에서는 찾지 못함) | 개발자 PC를 가리키는 `https://localhost/slack/oauth/callback`을 등록. 6단계 다시 설치에 실제로 쓰임 |
| 11 | 04 | 재발급 시험에서 이미 쓴 refresh token을 다시 씀 | 에이전트 시험 방식의 실수 | 저장된 토큰으로 정상 재발급·저장 후 동작 확인. 프로젝트 코드는 재발급하면 항상 바로 저장함 |
| 12 | 05 | requests 오류 메시지에 NEIS 인증키가 들어 있음 | requests가 오류 메시지에 요청 주소 전체(`KEY=...` 포함)를 넣음 | 오류는 종류 이름(`ConnectionError` 등)만 기록하고, `raise ... from None`으로 원래 메시지를 숨김 |
| 13 | 05 | 관리자 오류 알림에 원인이 없음 (개발자 질문: "급식 불러오기 실패한 이유가 뭐야?") | 실패 원인이 로그에만 남고 알림까지 전달되지 않음 | `NeisError`가 원인(결과 코드와 공식 설명)을 담아 알림까지 전달 |

### 콜백 서버와 명령어

| 번호 | 단계 | 문제 | 원인 | 해결 |
| --- | --- | --- | --- | --- |
| 14 | 06 | ngrok 공식 사이트가 열리지 않아 나이 조건을 확인하지 못함 | 사이트 접속 오류 | 계정이 필요 없는 Cloudflare Quick Tunnel을 고름 |
| 15 | 06 | 권한을 늘린 뒤 다시 설치하는 버튼이 없음 | Slack 화면이 공식 문서와 달라짐 | 공식 "Installing with OAuth" 과정을 그대로 밟는 `reinstall_slack_app.py`를 만듦 (`state` 확인 포함) |
| 16 | 06 | "토큰 자동 교체가 꺼져 있다"는 오해 | 화면의 초록색 Opt In 버튼은 PKCE 기능 버튼이었음 | 같은 화면의 "This app is using token rotation" 문구로 켜져 있음을 확인 |
| 17 | 06 | 1:1 메시지가 서버에 도착하지 않음 | Cloudflare 쪽에서 임시 터널이 지워짐 (`Unauthorized: Tunnel not found`) | 터널을 다시 켜고 Request URL을 새 주소로 변경 |
| 18 | 06 | Request URL 확인 실패 ("didn't respond with the value of the challenge parameter") | 주소 끝의 `/slack/events`를 빠뜨려 `/`로 요청이 감 (404) | 주소 끝에 `/slack/events`를 붙임 |
| 19 | 08 | 로컬 시험에서 답장이 가지 않음 | Windows에서 `--reload` 서버가 다시 시작하다 멈추고, 예전 코드로 계속 응답함 | 서버 프로세스를 모두 끄고 `--reload` 없이 다시 켬. 이후 `--reload`를 쓰지 않음 |
| 20 | 09 | 진짜 Ctrl+C로 종료 시험을 할 수 없음 | 에이전트 실행 환경에서는 Ctrl+C가 보통처럼 전달되지 않음 | Ctrl+C와 같은 신호를 흉내 내어 정상 종료를 확인. 진짜 Ctrl+C는 개발자가 확인 |

---

## 주요 결정

| 결정 | 이유 | 기록 |
| --- | --- | --- |
| 메신저를 네이버웍스 대신 Slack으로 | 미성년자 가입 불가. Slack은 만 16세 이상 가능. 전송 부분만 바꾸면 되도록 구조를 유지 | step01 |
| 명령어는 봇과의 1:1 대화(`message.im`)로 받음 | CLAUDE.md의 "봇에 보낸 명령어"에 가장 가깝고, 채널 대화 전체를 읽지 않아도 됨 | step06 |
| 토큰 자동 교체 켜기 | CLAUDE.md의 "토큰 만료 시 재발급"을 실제로 구현해 보려고. 한 번 켜면 끌 수 없다는 것을 알고 개발자가 정함 | step04 |
| 터널은 Cloudflare Quick Tunnel | 계정·가입이 필요 없음 | step06 |
| 서명 검증을 모든 요청에 가장 먼저 | 터널 주소를 아는 누구나 요청할 수 있음. 5분 넘은 요청도 거부 | step07 |
| Slack에 먼저 응답하고 답장은 뒤에서 | Slack의 3초 규칙 | step08 |
| `main.py`로 스케줄러와 서버를 한 프로그램에 | 위에서 아래로 읽히는 순서가 실행 순서와 같아 이해하기 쉬움 | step09 |
| 학사일정이 실패해도 급식 알림은 보냄 | 급식은 필수, 학사일정은 선택 기능 | step09 |

---

## 문서

| 문서 | 내용 |
| --- | --- |
| [`docs/step01-setup-guide.md`](docs/step01-setup-guide.md) | NEIS 인증키 발급, Slack 워크스페이스·앱 만들기 안내 |
| `docs/stepNN-learning.md` | 그 단계에서 새로 나온 Python 문법과 코드 줄 단위 해설, 확인 문제 |
| `docs/stepNN-devlog.md` | 그 단계에서 한 일, 실행 결과, 문제와 해결, 결정과 이유 |
| `docs/stepNN-practice.md` | 1~9단계 개념을 다지는 실습 과제 (단계마다 6~7개, 정답은 접어 둠). 실습 파일은 `practice\stepNN\`에 만듦 |

| 단계 | 내용 |
| --- | --- |
| [01](docs/step01-learning.md) | 환경 준비: 가상환경, pip, `.env` |
| [02](docs/step02-learning.md) | 데이터 조회: requests로 NEIS 호출, JSON |
| [03](docs/step03-learning.md) | 데이터 변환: 알레르기 번호, 날짜, pytest |
| [04](docs/step04-learning.md) | 메시지 전송: Slack 토큰 발급·재발급 → 단방향 완성 |
| [05](docs/step05-learning.md) | 예외 처리: 재시도, 오류 알림, 로그 |
| [06](docs/step06-learning.md) | 콜백 서버: FastAPI, 터널 |
| [07](docs/step07-learning.md) | 서명 검증과 명령어 해석 |
| [08](docs/step08-learning.md) | 명령어 응답 → 양방향 완성 |
| [09](docs/step09-learning.md) | 통합: 스케줄러 + 콜백 서버, 학사일정 |
| [10](docs/step10-learning.md) | 정리: 프로그램 전체 흐름 복습 |

---

## 확인한 공식 문서

- NEIS 교육정보 개방 포털: https://open.neis.go.kr
  - 급식식단정보: https://open.neis.go.kr/portal/data/service/selectServicePage.do?infId=OPEN17320190722180924242823&infSeq=2
  - 학사일정: https://open.neis.go.kr/portal/data/service/selectServicePage.do?infId=OPEN17220190722175038389180&infSeq=2
  - 학교기본정보: https://open.neis.go.kr/portal/data/service/selectServicePage.do?infId=OPEN17020190531110010104913&infSeq=2
- Slack
  - 토큰 자동 교체: https://docs.slack.dev/authentication/using-token-rotation/
  - OAuth 설치: https://docs.slack.dev/authentication/installing-with-oauth/
  - 요청 서명 확인: https://docs.slack.dev/authentication/verifying-requests-from-slack/
  - Events API: https://docs.slack.dev/apis/events-api/
  - `chat.postMessage`: https://docs.slack.dev/reference/methods/chat.postMessage/
  - `message.im` 이벤트: https://docs.slack.dev/reference/events/message.im/
  - 이용약관(나이 조건): https://slack.com/terms-of-service/user
- FastAPI Background Tasks: https://fastapi.tiangolo.com/tutorial/background-tasks/
- APScheduler 3.x: https://apscheduler.readthedocs.io/en/3.x/userguide.html
- Cloudflare Tunnel 내려받기: https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/downloads/
- Python 가상환경: https://docs.python.org/3/library/venv.html
