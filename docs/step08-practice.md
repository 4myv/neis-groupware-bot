# 8단계 실습 과제: 날짜 계산, 날짜별로 묶기, 함수를 값으로, 백그라운드 작업

## 이 문서를 다 풀면 할 수 있게 되는 것

1. `date`와 `timedelta`로 "100일 뒤", "이번 주 금요일", "다음 주 월요일"을 계산할 수 있다.
2. 섞여 있는 일정을 날짜별로 묶고, 숨길 것은 빼고, 날짜순으로 늘어놓을 수 있다.
3. 함수를 값으로 넘기고, 서버에서 "응답 먼저, 일은 나중에"를 만들 수 있다.

## 시작하기 전에

- 함께 볼 문서: [`step08-learning.md`](step08-learning.md)
- 실습 파일은 `practice\step08\` 폴더에 만듭니다. (`New-Item -ItemType Directory -Force practice\step08`)
- 가상환경을 켜고 프로젝트 맨 위 폴더에서 실행합니다.
  - 보통 파일: `python practice\step08\파일.py`
  - `app`을 가져오는 파일: `python -m practice.step08.파일`
- 과제 7은 PowerShell 창 두 개가 필요합니다. (서버는 8001번 포트)
- 결과는 모두 실제로 실행해 확인했습니다. 과제 6은 NEIS 자료라서, 학교가 일정을 고치면 결과가 달라질 수 있습니다.

---

## 과제 1. 날짜 계산 (★)

**다지는 개념**: `date`와 `timedelta`(2-2), `strftime`(2-3)

**할 일**

`practice\step08\p1_dates.py`를 만듭니다. 기준 날짜는 `date(2026, 11, 5)`(목요일)입니다.

1. 100일 뒤의 날짜를 출력합니다.
2. 그 날짜를 NEIS 모양 글자(`"20270213"` 같은)로 출력합니다.
3. 기준 날짜가 있는 주의 **금요일**을 출력합니다. (월요일을 먼저 구한 뒤 더합니다)
4. `date(2027, 3, 2) - 기준 날짜`를 출력합니다. (날짜끼리 빼면 무엇이 나올까요?)

**확인 방법**

```
2027-02-13
20270213
2026-11-06
117 days, 0:00:00
```

마지막 줄: 날짜에서 날짜를 빼면 **기간**(`timedelta`)이 나옵니다. 117일 차이입니다.

<details><summary>정답 예시</summary>

```python
# date와 timedelta, strftime 연습
from datetime import date, timedelta

day = date(2026, 11, 5)
after_100_days = day + timedelta(days=100)
monday = day - timedelta(days=day.weekday())

print(after_100_days)
print(after_100_days.strftime("%Y%m%d"))
print(monday + timedelta(days=4))
print(date(2027, 3, 2) - day)
```

- 월요일 + 4일 = 금요일입니다. `app/commands.py`의 `week_start`, `week_end`와 같은 방법입니다.

</details>

---

## 과제 2. 기본값이 있는 매개변수 (★)

**다지는 개념**: 기본값이 있는 매개변수(2-4), 키워드 인자(step02)

**할 일**

`practice\step08\p2_default.py`를 만듭니다.

1. `app.formatter`의 `format_date`를 가져옵니다.
2. 함수 `make_title(meal_date: str, meal_name: str = "중식") -> str`: `"[11월 5일(목) 중식]"` 모양의 제목을 돌려줍니다.
3. 세 가지로 불러 출력합니다.
   - `make_title("20261105")`
   - `make_title("20261105", "석식")`
   - `make_title(meal_name="조식", meal_date="20261106")` (이름을 붙여 넘기면 순서를 바꿔도 됩니다)

**확인 방법**

```
[11월 5일(목) 중식]
[11월 5일(목) 석식]
[11월 6일(금) 조식]
```

<details><summary>정답 예시</summary>

```python
# 기본값이 있는 매개변수 연습
from app.formatter import format_date


def make_title(meal_date: str, meal_name: str = "중식") -> str:
    return f"[{format_date(meal_date)} {meal_name}]"


print(make_title("20261105"))
print(make_title("20261105", "석식"))
print(make_title(meal_name="조식", meal_date="20261106"))
```

- 기본값이 있는 매개변수는 **뒤에** 둡니다. 앞에 두면 `SyntaxError`입니다. (2-4 자주 하는 실수)

</details>

---

## 과제 3. 날짜별로 묶고, 빼고, 늘어놓기 (★★)

**다지는 개념**: `continue`(2-5), 리스트가 든 딕셔너리(2-6), `sorted`(2-7)

**할 일**

`practice\step08\p3_group.py`를 만들고, 아래 자료로 시작합니다. 날짜 순서가 섞여 있고, 같은 행사가 두 번 들어 있습니다.

```python
rows = [
    {"date": "20261106", "name": "학교폭력예방교육"},
    {"date": "20261102", "name": "수학 하이챌린지"},
    {"date": "20261107", "name": "토요휴업일"},
    {"date": "20261104", "name": "수업공개의 날"},
    {"date": "20261104", "name": "독서골든벨"},
    {"date": "20261106", "name": "학교폭력예방교육"},
]
HIDDEN_NAMES: list[str] = ["토요휴업일"]
```

1. `events_by_date: dict[str, list[str]]`에 날짜별로 행사 이름을 모읍니다.
   - `HIDDEN_NAMES`에 있는 행사는 `continue`로 건너뜁니다.
   - 같은 날 같은 이름은 한 번만 넣습니다.
2. `events_by_date`를 그대로 출력합니다.
3. 날짜순으로 한 줄씩, 같은 날 행사는 `", "`로 이어 출력합니다.

**확인 방법**

```
{'20261106': ['학교폭력예방교육'], '20261102': ['수학 하이챌린지'], '20261104': ['수업공개의 날', '독서골든벨']}
20261102 수학 하이챌린지
20261104 수업공개의 날, 독서골든벨
20261106 학교폭력예방교육
```

- 첫 줄: 딕셔너리는 **넣은 순서대로** 보입니다. 날짜순이 아닙니다.
- 아랫줄들: `sorted`로 늘어놓아서 날짜순입니다.

<details><summary>정답 예시</summary>

```python
events_by_date: dict[str, list[str]] = {}
for row in rows:
    if row["name"] in HIDDEN_NAMES:
        continue
    if row["date"] not in events_by_date:
        events_by_date[row["date"]] = []
    if row["name"] not in events_by_date[row["date"]]:
        events_by_date[row["date"]].append(row["name"])

print(events_by_date)
for event_date in sorted(events_by_date):
    print(event_date, ", ".join(events_by_date[event_date]))
```

`app/formatter.py`의 `group_events_by_date`, `format_schedule_lines`와 같은 흐름입니다. 비교해 읽어 보세요.

</details>

---

## 과제 4. `if`와 `return`으로 갈래 나누기 (★)

**다지는 개념**: `if`와 `return`(2-8), `weekday()`(step03)

**할 일**

`practice\step08\p4_if_return.py`를 만듭니다.

1. 함수 `describe_day(day: date) -> str`
   - 토요일·일요일(`weekday()`가 5 이상)이면 `주말이라 급식이 없어요`
   - 금요일(4)이면 `금요일이에요`
   - 나머지는 `평일이에요`
   - `else` 없이 `if`와 `return`만 씁니다.
2. 2026년 11월 5일~8일로 확인합니다.

**확인 방법**

```
2026-11-05 평일이에요
2026-11-06 금요일이에요
2026-11-07 주말이라 급식이 없어요
2026-11-08 주말이라 급식이 없어요
```

<details><summary>정답 예시</summary>

```python
# if와 return으로 갈래 나누기
from datetime import date


def describe_day(day: date) -> str:
    if day.weekday() >= 5:
        return "주말이라 급식이 없어요"
    if day.weekday() == 4:
        return "금요일이에요"
    return "평일이에요"


for day in [date(2026, 11, 5), date(2026, 11, 6), date(2026, 11, 7), date(2026, 11, 8)]:
    print(day, describe_day(day))
```

- `>=`는 "크거나 같다"입니다.
- 맨 아래 `return`은 "위의 어느 것에도 해당하지 않으면"입니다. `app/commands.py`의 `build_reply`에서 `HELP_TEXT`가 이 자리에 있습니다.

</details>

---

## 과제 5. 함수를 값으로 넘기기 (★★)

**다지는 개념**: 함수를 값으로 넘기기(2-9), 리스트와 `append`(step03)

**할 일**

`practice\step08\p5_function_value.py`를 만듭니다.

1. 함수 두 개를 만듭니다.
   - `shout(text: str) -> str`: 끝에 `!`를 붙여 돌려줍니다.
   - `wrap(text: str) -> str`: 앞뒤에 `[`, `]`를 붙여 돌려줍니다.
2. 함수 `apply_to_all(change, words: list[str]) -> list[str]`: `words`의 단어마다 `change`를 실행한 결과를 모아 새 리스트로 돌려줍니다.
3. `["급식", "일정"]`에 `shout`, `wrap`을 각각 적용해 출력합니다.

**확인 방법**

```
['급식!', '일정!']
['[급식]', '[일정]']
```

<details><summary>정답 예시</summary>

```python
# 함수를 값으로 넘기기
def shout(text: str) -> str:
    return text + "!"


def wrap(text: str) -> str:
    return "[" + text + "]"


def apply_to_all(change, words: list[str]) -> list[str]:
    results = []
    for word in words:
        results.append(change(word))
    return results


words = ["급식", "일정"]
print(apply_to_all(shout, words))
print(apply_to_all(wrap, words))
```

- `apply_to_all(shout, words)`처럼 **괄호 없이** 넘깁니다. `shout("급식")`처럼 괄호를 붙이면 그 자리에서 실행되어 글자가 넘어갑니다.
- `apply_to_all`은 무엇을 할지 모른 채 "받은 함수를 단어마다 실행"만 합니다. 스케줄러(`add_job`)와 `add_task`도 이렇게 받은 함수를 나중에 실행합니다.

</details>

---

## 과제 6. 프로젝트 함수로 "다음 주 일정" 만들기 (★★★)

**다지는 개념**: `timedelta`(2-2), 프로젝트 함수 조합(`week_start`, `to_yyyymmdd`, `fetch_schedules`, `format_week_schedule_message`)

**할 일**

`practice\step08\p6_next_week.py`를 만듭니다. 새 명령어 `다음 주 일정`을 만든다면 어떻게 될지 미리 해 보는 과제입니다.

1. 기준 날짜는 `date(2026, 11, 5)`입니다.
2. `app.commands`의 `week_start`로 이번 주 월요일을 구하고, 7일을 더해 **다음 주 월요일**, 거기서 6일을 더해 **다음 주 일요일**을 구합니다.
3. 둘을 `to_yyyymmdd`로 NEIS 모양 글자로 바꿔 출력합니다.
4. `fetch_schedules("B10", "7010083", 시작일, 끝일)`로 공개 예시 학교(서울고등학교)의 일정을 가져와, `format_week_schedule_message`로 메시지를 만들어 출력합니다.
5. `python -m practice.step08.p6_next_week`로 실행합니다.

**확인 방법** (2026-11-05에 실행한 결과)

```
20261109 20261115
[11월 9일(월) ~ 11월 15일(일) 학사일정]
11월 9일(월) 과학 하이챌린지(1,2)
11월 10일(화) 과학 하이챌린지(1,2)
11월 11일(수) 과학 하이챌린지(1,2)
11월 12일(목) 글로벌 인문학 특강
11월 13일(금) 과학탐사(천문캠프), 학급자치
```

**더 해 보기**: `app.config`의 `NEIS_OFFICE_CODE`, `NEIS_SCHOOL_CODE`를 가져와 내 학교로 바꿔 봅니다.

<details><summary>정답 예시</summary>

```python
# 프로젝트 함수로 "다음 주 일정" 만들어 보기 (공개 예시 학교)
from datetime import date, timedelta

from app.commands import to_yyyymmdd, week_start
from app.formatter import format_week_schedule_message
from app.neis import fetch_schedules

today = date(2026, 11, 5)
next_monday = week_start(today) + timedelta(days=7)
next_sunday = next_monday + timedelta(days=6)
start_date = to_yyyymmdd(next_monday)
end_date = to_yyyymmdd(next_sunday)
print(start_date, end_date)

schedule_result = fetch_schedules("B10", "7010083", start_date, end_date)
print(format_week_schedule_message(schedule_result, start_date, end_date))
```

- 진짜 명령어로 만들려면 `app/commands.py`의 명령어 표(`COMMANDS`)에 `"다음주일정"`을 더하고, `build_reply`에 갈래 하나를 더하면 됩니다. 조회·변환 함수는 그대로 다시 씁니다.

</details>

---

## 과제 7. 도전: 응답 먼저, 일은 나중에 (★★★)

**다지는 개념**: 3초 규칙과 백그라운드 작업(2-1), FastAPI `BackgroundTasks`(2-10), 함수를 값으로(2-9)

**할 일**

1. `practice\step08\bg_server.py`를 만듭니다.
   - 2초 걸리는 함수 `make_reply(text: str) -> None`: `time.sleep(2)` 뒤에 `[뒤에서 끝남]`과 글을 출력합니다. (NEIS 조회 + Slack 전송 흉내)
   - `POST /command` 창구: 본문의 `text`를 꺼내 `make_reply`를 **백그라운드 작업으로 맡기고**, `[먼저] 응답을 돌려줍니다`를 출력한 뒤 `ok`를 돌려줍니다.
2. 창 1에서 켭니다: `python -m uvicorn practice.step08.bg_server:app --port 8001`
3. `practice\step08\p7_client.py`를 만들어 창 2에서 실행합니다. `{"text": "오늘 급식"}`을 보내고, **응답까지 걸린 시간**을 소수 둘째 자리까지 출력합니다.

**확인 방법**

창 2:

```
200 ok | 응답까지 0.07 초
```

창 1 (셋째 줄은 2초 뒤에 나옵니다):

```
[먼저] 응답을 돌려줍니다
INFO:     127.0.0.1:51927 - "POST /command HTTP/1.1" 200 OK
[뒤에서 끝남] 오늘 급식 에 답장했습니다
```

2초 걸리는 일을 맡겼는데도 응답은 0.1초 안에 왔습니다. Slack의 3초 규칙을 지키는 방법입니다.

**더 해 보기**: `add_task(make_reply, ...)` 대신 `make_reply(payload.get("text", ""))`로 바로 부르게 고쳐 보세요. 응답까지 몇 초 걸리나요?

<details><summary>정답 예시</summary>

`practice\step08\bg_server.py`:

```python
# 응답을 먼저 돌려주고, 일은 뒤에서 하는 실습 서버. 실행: python -m uvicorn practice.step08.bg_server:app --port 8001
import time

from fastapi import BackgroundTasks, FastAPI, Request
from fastapi.responses import PlainTextResponse

app = FastAPI()


def make_reply(text: str) -> None:
    # 오래 걸리는 일(NEIS 조회 + Slack 전송) 흉내
    time.sleep(2)
    print("[뒤에서 끝남]", text, "에 답장했습니다")


@app.post("/command")
async def command(request: Request, background_tasks: BackgroundTasks) -> PlainTextResponse:
    payload = await request.json()
    background_tasks.add_task(make_reply, payload.get("text", ""))
    print("[먼저] 응답을 돌려줍니다")
    return PlainTextResponse("ok")
```

`practice\step08\p7_client.py`:

```python
# 응답이 얼마나 빨리 오는지 재 보기
import time

import requests

started = time.time()
response = requests.post("http://127.0.0.1:8001/command", json={"text": "오늘 급식"}, timeout=10)
print(response.status_code, response.text, "| 응답까지", round(time.time() - started, 2), "초")
```

- `request: Request`와 `background_tasks: BackgroundTasks`를 함께 받을 수 있습니다. 타입 힌트를 보고 FastAPI가 각각 알맞은 값을 넣어 줍니다.
- **더 해 보기**에서는 일을 다 한 뒤에야 응답하므로 2초 넘게 걸립니다. Slack이었다면 늦어질 때 같은 이벤트를 다시 보냈을 것입니다.

</details>

---

## 다 풀었다면

- [ ] 날짜에 `timedelta(days=숫자)`를 더하고 빼서 원하는 날을 구할 수 있다.
- [ ] `continue`, 빈 리스트 먼저 넣기, `sorted`로 일정을 날짜별로 정리할 수 있다.
- [ ] 함수를 괄호 없이 넘기는 것과 괄호를 붙여 넘기는 것의 차이를 말할 수 있다.

## 이번 단계 핵심 정리

1. `date + timedelta(days=n)`은 n일 뒤, 날짜 - 날짜는 기간이다. `strftime("%Y%m%d")`로 NEIS 모양 글자가 된다.
2. 기본값이 있는 매개변수를 더하면, 원래 부르던 코드를 고치지 않고 기능을 넓힐 수 있다.
3. 날짜별로 묶을 때는 처음 보는 키에 빈 리스트를 먼저 넣고, 늘어놓을 때는 `sorted`를 쓴다.
4. `if ... return`을 나란히 쓰면 맞는 갈래 하나만 실행되고, 맨 아래 `return`이 "그 밖"이다.
5. `add_task(함수, 값)`처럼 함수를 괄호 없이 넘기면 응답 뒤에 실행된다.
