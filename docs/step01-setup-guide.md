# 1단계 안내서: 개발자가 직접 할 일

이 문서는 에이전트가 대신할 수 없는 일을 순서대로 안내합니다.
인증키나 시크릿(남에게 알려지면 안 되는 비밀값)은 이 문서에도, 채팅에도 적지 마세요. `.env` 파일에만 적습니다.

> 메신저는 처음 계획한 네이버웍스 대신 **Slack**을 씁니다.
> 네이버웍스는 미성년자가 가입할 수 없어서 바꿨습니다. 자세한 이유는 [개발 기록](step01-devlog.md)에 있습니다.

## 이 문서를 다 읽으면 할 수 있게 되는 것

1. PowerShell에서 가상환경을 켜고 `python check_setup.py`를 실행할 수 있다.
2. NEIS 인증키를 받아 `.env` 파일에 넣을 수 있다.
3. Slack 워크스페이스와 봇(앱)을 만들고, 봇 토큰을 `.env`에 넣을 수 있다.

---

## 순서 한눈에 보기

| 순서 | 할 일 | 언제까지 |
| --- | --- | --- |
| 1 | PowerShell 실행 정책 바꾸기 | 지금 (처음 한 번만) |
| 2 | 가상환경 켜고 확인하기 | 지금 |
| 3 | `.env` 파일 만들기 | 지금 |
| 4 | NEIS 인증키 발급받기 | 2단계 시작 전 |
| 5 | Slack 워크스페이스 만들기 | 4단계 시작 전 |
| 6 | Slack 앱 만들고 권한 주기 | 4단계 시작 전 |
| 7 | 앱 설치하고 비밀값 2개 받기 | 4단계 시작 전 |
| 8 | 테스트 채널에 앱 초대하기 | 4단계 시작 전 |
| 9 | 확인하고 알려 주기 | 끝난 뒤 |

2단계(NEIS 급식 조회)에는 4번까지만 필요합니다.
Slack(5~8번)은 4단계(메시지 전송) 전에만 끝내면 됩니다.

---

## 1. PowerShell 실행 정책 바꾸기 (처음 한 번만)

### 왜 하나요?

가상환경을 켜는 명령은 `Activate.ps1`이라는 파일을 실행합니다.
이 파일은 PowerShell 스크립트(PowerShell 명령을 모아 둔 파일)입니다.

Windows는 처음 설치된 상태에서 스크립트 실행을 막아 둡니다.
이 컴퓨터도 막혀 있습니다. 그래서 그대로 켜면 아래 문장이 들어 있는 빨간 오류가 납니다.
(에이전트가 이 컴퓨터와 같은 조건을 만들어 실제로 확인한 문장입니다.)

```
File C:\neis_groupware_bot\.venv\Scripts\Activate.ps1 cannot be loaded because running scripts is disabled on this system.
```

### 어떻게 하나요?

1. 시작 메뉴에서 "PowerShell"을 검색해 엽니다. 관리자 권한으로 열 필요는 없습니다.
2. 아래 명령을 그대로 입력하고 Enter를 누릅니다.

   ```powershell
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
   ```

3. 바꿀지 묻는 문장이 나오면 `Y`를 입력하고 Enter를 누릅니다. 아무것도 묻지 않고 끝나도 정상입니다.
4. 잘 바뀌었는지 확인합니다.

   ```powershell
   Get-ExecutionPolicy -Scope CurrentUser
   ```

   결과가 아래처럼 나오면 성공입니다.

   ```
   RemoteSigned
   ```

### 이 설정은 무슨 뜻인가요?

- 내 컴퓨터에서 만든 스크립트는 실행을 허용합니다.
- 인터넷에서 내려받은 스크립트는 서명(만든 사람을 증명하는 표시)이 있어야 실행됩니다.
- `-Scope CurrentUser`는 "지금 로그인한 사용자에게만 적용"이라는 뜻입니다. 컴퓨터 전체 설정은 바꾸지 않습니다.

Python 공식 문서도 같은 명령을 안내합니다. (https://docs.python.org/3/library/venv.html)

### 바꾸고 싶지 않다면

가상환경을 켜지 않고, 가상환경의 Python을 직접 지정해 실행해도 됩니다.

```powershell
.venv\Scripts\python.exe check_setup.py
```

결과는 같습니다. 다만 명령을 칠 때마다 앞부분이 길어집니다.

---

## 2. 가상환경 켜고 확인하기

가상환경(이 프로젝트만 쓰는 Python 작업 공간)은 에이전트가 `.venv` 폴더에 만들어 두었습니다.
자세한 설명은 [학습 정리](step01-learning.md)의 2-2를 보세요.

### 켜기

```powershell
cd C:\neis_groupware_bot
.venv\Scripts\Activate.ps1
```

켜지면 줄 맨 앞에 `(.venv)`가 붙습니다.

```
(.venv) PS C:\neis_groupware_bot>
```

### 확인하기

```powershell
python check_setup.py
```

에이전트가 실행했을 때 나온 결과입니다.

```
Python 버전: 3.13.16 (tags/v3.13.16:cbc944f, Sep 30 2026, 19:17:50) [MSC v.1944 64 bit (AMD64)]
Python 위치: C:\neis_groupware_bot\.venv\Scripts\python.exe
NEIS_API_KEY: 비어 있음 (.env 파일을 확인하세요)
```

- "Python 위치"가 `.venv` 폴더 안이면 성공입니다.
- 마지막 줄은 아직 인증키를 넣지 않아서 "비어 있음"이 맞습니다.

### 끄기

```powershell
deactivate
```

줄 앞의 `(.venv)`가 사라지면 꺼진 것입니다.

> 새 PowerShell 창을 열 때마다 가상환경을 다시 켜야 합니다.

---

## 3. `.env` 파일 만들기

`.env`는 인증키 같은 비밀값을 적어 두는 파일입니다.
`.env.example`은 어떤 항목을 적어야 하는지 보여 주는 견본입니다.

```powershell
Copy-Item .env.example .env
notepad .env
```

- 첫 줄은 견본을 복사해 `.env`를 만듭니다.
- 둘째 줄은 메모장으로 `.env`를 엽니다.

값은 `=` 바로 뒤에 붙여 적습니다. 따옴표와 빈칸은 넣지 않습니다.

```
NEIS_API_KEY=여기에_발급받은_키
```

### 주의할 점

- 메모장의 "다른 이름으로 저장"을 쓰면 파일 이름이 `.env.txt`로 바뀔 수 있습니다. 위 명령으로 만들고 그냥 "저장"만 하세요.
- `.env`는 `.gitignore`에 들어 있어서 GitHub에 올라가지 않습니다.
- 확인 방법: `git status`를 실행했을 때 목록에 `.env`가 나오지 않아야 합니다.

---

## 4. NEIS 인증키 발급받기

1. https://open.neis.go.kr 에 들어갑니다.
2. 위쪽 메뉴의 **"로그인"**을 누릅니다.
   - 따로 회원가입을 하지 않습니다.
   - 구글, 카카오톡, 페이스북, 네이버 계정 중 하나로 로그인합니다.
3. 위쪽 메뉴 **"활용가이드"** → **"인증키 신청"**으로 들어갑니다.
4. 신청서를 채우고 신청합니다.
   - 신청서는 로그인해야 보여서, 에이전트가 칸 이름을 미리 확인하지 못했습니다.
   - 용도를 묻는 칸이 있으면 "학교 급식·학사일정 알림 프로그램 개발 연습(개인 학습용)"처럼 적으면 됩니다.
5. 인증키는 신청하면 바로 발급됩니다. 마이페이지의 **"인증키 발급 내역"**에서 볼 수 있습니다.
6. 인증키를 복사해 `.env`의 `NEIS_API_KEY=` 바로 뒤에 붙여 넣고 저장합니다.
7. 가상환경을 켠 상태에서 확인합니다.

   ```powershell
   python check_setup.py
   ```

   마지막 줄이 아래처럼 바뀌면 성공입니다.

   ```
   NEIS_API_KEY: 입력됨
   ```

> 이용약관에 따라 인증키는 발급받은 본인만 써야 하고 남과 공유하면 안 됩니다.
> 채팅, 스크린샷, 코드 어디에도 붙여 넣지 마세요.

---

## 5. Slack 워크스페이스 만들기

워크스페이스(workspace)는 Slack 안의 "우리 팀 공간"입니다.
회사 하나가 그룹웨어 하나를 쓰는 것과 비슷합니다. 연습용으로 나만 쓰는 워크스페이스를 새로 만듭니다.

> Slack 약관은 **만 16세 미만은 쓸 수 없다**고 정해 두었습니다. 이 조건에 맞는지 먼저 확인하세요.

1. https://slack.com/get-started#/createnew 에 들어갑니다.
2. 이메일 주소를 입력하고 **"Continue"**를 누릅니다. Apple이나 Google 계정으로 계속해도 됩니다.
3. 이메일로 온 확인 코드를 입력합니다.
4. **"Create a Workspace"**를 누르고 화면 안내를 따릅니다.
   - 워크스페이스 이름 예시: `lunch-bot-lab`
   - 유료 플랜 체험이나 결제를 권하는 화면이 나오면 건너뛰고 무료로 계속합니다.

워크스페이스를 만든 사람은 **Workspace Primary Owner**(워크스페이스의 최고 관리자)가 됩니다. (공식 도움말)

---

## 6. Slack 앱 만들고 권한 주기

Slack에서는 봇을 "앱(app)"으로 만듭니다.
앱은 우리 프로그램이 Slack API(프로그램끼리 정해진 방식으로 요청하고 답을 받는 창구)를 쓰겠다고 등록하는 것입니다.

### 왜 링크로 만드나요?

공식 문서는 앱 만들기 화면에서 "Blank app"을 고르라고 안내합니다.
그런데 2026년 11월 현재 실제 화면에는 "AI agent"와 "Starter app"만 보입니다. (개발자가 직접 확인)
"Starter app"이 무엇을 미리 켜 두는지는 공식 문서에 나와 있지 않습니다.

그래서 **manifest(앱 이름과 권한 같은 설정을 한 번에 적은 설정 묶음)를 담은 링크**로 앱을 만듭니다.
공식 문서에 따르면 `https://api.slack.com/apps?new_app=1&manifest_json=<설정>` 주소로 들어가면, 그 설정으로 앱 만들기가 바로 시작됩니다.

링크에 담은 설정은 아래와 같습니다. 이 프로젝트에 필요한 것만 넣었습니다.

```json
{
  "display_information": {
    "name": "lunch-bot",
    "description": "Learning project: posts school lunch menus and schedules."
  },
  "features": {
    "bot_user": {
      "display_name": "lunch-bot",
      "always_online": false
    }
  },
  "oauth_config": {
    "scopes": {
      "bot": [
        "chat:write"
      ]
    }
  },
  "settings": {
    "org_deploy_enabled": false,
    "socket_mode_enabled": false,
    "token_rotation_enabled": false
  }
}
```

| 설정 | 뜻 |
| --- | --- |
| `name`, `display_name` | 앱과 봇의 이름. 봇 이름에는 영어 소문자, 숫자, `-`, `_`, `.`만 쓸 수 있습니다. |
| `"bot": ["chat:write"]` | 봇에게 줄 권한(scope). `chat:write`는 메시지를 보낼 수 있는 권한입니다. |
| `socket_mode_enabled: false` | Socket Mode(공개 주소 없이 Slack과 연결을 유지하는 방식)를 끕니다. 이 프로젝트는 6단계에서 콜백 주소로 요청을 받는 방식을 직접 만들어 봅니다. |
| `token_rotation_enabled: false` | 토큰 자동 교체를 끕니다. 4단계에서 토큰을 다룰 때 다시 정합니다. |

### 앱 만들기

1. Slack에 로그인한 브라우저에서 아래 링크를 엽니다. 한 줄 전체를 복사해야 합니다.

   ```
   https://api.slack.com/apps?new_app=1&manifest_json=%7B%22display_information%22%3A%7B%22name%22%3A%22lunch-bot%22%2C%22description%22%3A%22Learning%20project%3A%20posts%20school%20lunch%20menus%20and%20schedules.%22%7D%2C%22features%22%3A%7B%22bot_user%22%3A%7B%22display_name%22%3A%22lunch-bot%22%2C%22always_online%22%3Afalse%7D%7D%2C%22oauth_config%22%3A%7B%22scopes%22%3A%7B%22bot%22%3A%5B%22chat%3Awrite%22%5D%7D%7D%2C%22settings%22%3A%7B%22org_deploy_enabled%22%3Afalse%2C%22socket_mode_enabled%22%3Afalse%2C%22token_rotation_enabled%22%3Afalse%7D%7D
   ```

2. 5번에서 만든 워크스페이스를 고르고 **"Next"**를 누릅니다.
3. 설정 요약을 확인하고 **"Create"**를 누릅니다.
   - 앱 이름이 `lunch-bot`인지 확인합니다.
   - 봇 권한이 `chat:write` 하나뿐인지 확인합니다.

권한(scope)은 링크에 이미 들어 있으므로 따로 추가하지 않습니다.
다른 권한이 필요해지면 그 단계에서 추가합니다.

> 링크를 열어도 "AI agent / Starter app" 선택 화면만 나오면 아무것도 누르지 말고 알려 주세요.

만들고 나면 앱의 **"Basic Information"** 페이지가 열립니다. 7번에서 다시 옵니다.

---

## 7. 앱 설치하고 비밀값 2개 받기

### 앱을 워크스페이스에 설치하기

1. **"OAuth & Permissions"** 페이지 맨 위로 올라갑니다.
2. **"Install to Workspace"**를 누릅니다. (문서에 따라 "Install App to Workspace"로도 적혀 있습니다.)
3. 다음 화면에서 **"Allow"**를 누릅니다.

### 봇 토큰 받기 → `SLACK_BOT_TOKEN`

토큰(token)은 "이 요청은 우리 봇이 보낸 것"임을 증명하는 긴 문자열입니다. 비밀번호와 같습니다.

1. 설치가 끝나면 **"OAuth & Permissions"** 페이지로 돌아옵니다.
2. **"OAuth Tokens"** 부분에 토큰이 보입니다. 이름은 "Bot User OAuth Token"처럼 적혀 있습니다.
3. **`xoxb-`로 시작하는** 토큰을 복사해 `.env`의 `SLACK_BOT_TOKEN=` 뒤에 붙여 넣습니다.

> 공식 문서의 당부: "Keep it secret. Keep it safe." (비밀로, 안전하게 보관하라)

### Signing Secret 받기 → `SLACK_SIGNING_SECRET`

Signing Secret은 Slack이 우리 프로그램으로 보낸 요청이 진짜인지 확인할 때 쓰는 비밀값입니다. 7단계(서명 검증)에서 씁니다.

1. 왼쪽 메뉴 **"Basic Information"**으로 갑니다.
2. **"Signing Secret"** 항목을 찾습니다. 값이 가려져 있으면 보이게 하는 버튼을 누릅니다.
3. 복사해 `.env`의 `SLACK_SIGNING_SECRET=` 뒤에 붙여 넣습니다.

> 같은 곳에 "Verification Token"이 보일 수 있습니다. 예전 방식이라 쓰지 않습니다.
> 공식 문서도 Signing Secret만 쓰라고 권합니다.

### scope를 나중에 바꾸면

scope를 추가하거나 빼면 앱을 다시 설치해야 적용됩니다.
그때는 같은 페이지의 "Reinstall to Workspace"를 누릅니다.

---

## 8. 테스트 채널에 앱 초대하기

채널(channel)은 Slack의 대화방입니다.
새로 만든 앱은 초대받은 채널에만 메시지를 보낼 수 있습니다. 그래서 테스트용 채널에 앱을 초대해 둡니다.

1. Slack에서 테스트용 채널을 하나 만듭니다. 예시 이름: `lunch-bot-test`
   - 채널 만드는 버튼은 Slack 화면 버전마다 위치가 달라서 이름을 적지 않았습니다. 왼쪽 채널 목록 근처에서 채널을 추가하는 버튼을 찾으세요.
2. 그 채널의 메시지 입력창에 아래처럼 입력하고 보냅니다. (`@` 뒤는 6번에서 정한 앱 이름입니다.)

   ```
   /invite @lunch-bot
   ```

3. 앱이 채널에 추가되었다는 메시지가 보이면 성공입니다.

채널 ID(채널마다 붙은 고유 번호)는 4단계에서 필요할 때 찾는 방법을 안내합니다.

---

## 9. 확인하고 알려 주기

### 체크리스트

- [ ] `python check_setup.py`의 마지막 줄이 `NEIS_API_KEY: 입력됨`이다.
- [ ] `.env`의 `SLACK_BOT_TOKEN`과 `SLACK_SIGNING_SECRET`에 값을 넣었다. (값은 에이전트에게 보여 주지 않습니다.)
- [ ] 테스트 채널에 앱을 초대했다.
- [ ] `git status`를 실행했을 때 `.env`가 목록에 나오지 않는다.

### 알려 주는 방법

- 다 되면 "1단계 안내서 완료"라고만 알려 주세요.
- NEIS까지만 끝냈다면 "NEIS 완료"라고 알려 주세요. 2단계는 바로 시작할 수 있습니다.
- 막히면 ① 몇 번 순서에서 ② 화면에 어떤 문구가 나왔는지 알려 주세요.
- 화면을 캡처해서 보낼 때는 키, 토큰, Signing Secret이 보이는 부분을 가려 주세요.

---

## 확인한 공식 문서

- NEIS 개발자 가이드: https://open.neis.go.kr/portal/guide/apiGuidePage.do
- NEIS Open API 소개: https://open.neis.go.kr/portal/guide/apiIntroPage.do
- NEIS 서비스 이용약관: https://open.neis.go.kr/portal/userAgreementPage.do
- Slack 워크스페이스 만들기: https://slack.com/help/articles/206845317-Create-a-Slack-workspace
- Slack 앱 설정 화면으로 앱 만들기: https://docs.slack.dev/app-management/quickstart-app-settings/
- Slack Bolt for Python 앱 만들기(버튼 이름 비교용): https://docs.slack.dev/tools/bolt-python/creating-an-app/
- Slack manifest로 앱 만들기(링크 방식): https://docs.slack.dev/app-manifests/configuring-apps-with-app-manifests/
- Slack manifest 항목 설명: https://docs.slack.dev/reference/app-manifest/
- Slack `chat:write` scope: https://docs.slack.dev/reference/scopes/chat.write/
- Slack 요청 검증(Signing Secret): https://docs.slack.dev/authentication/verifying-requests-from-slack/
- Slack 사용자 약관(나이 조건): https://slack.com/terms-of-service/user
- Python venv 문서(실행 정책): https://docs.python.org/3/library/venv.html

## 이번 문서 핵심 정리

1. PowerShell 실행 정책을 RemoteSigned로 한 번 바꾸면 가상환경을 켤 수 있다.
2. 비밀값은 모두 `.env`에만 적는다. `.env`는 GitHub에 올라가지 않는다.
3. NEIS 인증키는 2단계 전에, Slack 준비는 4단계 전에 끝내면 된다.
4. Slack 봇은 앱으로 만들고, `chat:write` 권한을 준 뒤 설치해야 `xoxb-` 토큰이 나온다.
5. 막히면 억지로 진행하지 말고, 어디서 어떤 문구가 나왔는지 알려 준다.
