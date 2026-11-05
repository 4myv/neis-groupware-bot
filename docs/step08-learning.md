# 8단계 학습 정리: 명령어 응답 (양방향 완성)

## 이 문서를 다 읽으면 할 수 있게 되는 것

1. "내일", "이번 주 월요일"처럼 날짜를 계산하는 코드를 읽고 설명할 수 있다.
2. 학사일정을 날짜별로 묶는 코드(리스트가 든 딕셔너리, `continue`, `sorted`)를 설명할 수 있다.
3. 서버가 Slack에 먼저 응답하고, 답장은 뒤에서 보내는 이유와 방법을 설명할 수 있다.

## 읽기 전에

- 코드 예시는 모두 실제로 실행한 결과를 붙였습니다. 긴 파일 경로는 `예시.py`처럼 줄여 적었습니다.
- 학교 이름과 일정은 공개된 예시 학교(서울고등학교)의 실제 NEIS 자료입니다.
- 앞 단계에서 설명한 것은 "step03 참고"처럼 적었습니다.

---

## 1. 이번 단계에서 새로 나온 것

**개념**

1. 3초 규칙과 백그라운드 작업

**Python 문법과 라이브러리**

2. `date`와 `timedelta`: 날짜 더하고 빼기
3. `strftime`: 날짜를 글자로
4. 기본값이 있는 매개변수
5. `continue`: 이번 차례만 건너뛰기
6. 리스트가 든 딕셔너리 `dict[str, list[str]]`
7. `sorted`: 순서대로 늘어놓기
8. `if`와 `return`으로 갈래 나누기
9. 함수를 값으로 넘기기
10. FastAPI `BackgroundTasks`

**앞 단계에서 설명한 것**

- step02: 딕셔너리, 리스트, `for`
- step03: `datetime.strptime`, `weekday()`(월요일이 0), `strip`, `append`, `not in`, `join`, `\n`, f-문자열
- step04: `-> None`(돌려주는 값이 없는 함수)
- step05: `try` / `except`, `NeisError`, `logger`
- step06: FastAPI, `@app.post`, `async def`
- step07: `parse_command`, 명령어 이름 상수

---

## 2. 하나씩 설명

### 2-1. 3초 규칙과 백그라운드 작업

**설명**

Slack은 이벤트를 보낸 뒤 **3초 안에** 응답(HTTP 200)을 받아야 성공으로 봅니다. (Slack 공식 문서 Events API)

3초 안에 응답이 없으면 실패로 보고, 같은 이벤트를 다시 보냅니다.

답장을 만들려면 두 가지 일을 해야 합니다.

1. NEIS에서 급식이나 일정을 가져온다.
2. Slack으로 답장을 보낸다.

평소에는 둘을 합쳐 0.5초도 걸리지 않습니다. 그런데 NEIS가 실패하면 3초를 기다렸다가 다시 시도합니다. (step05) 그러면 3초를 쉽게 넘깁니다.

그래서 순서를 바꿉니다.

1. 요청을 받자마자 Slack에 200을 돌려준다.
2. 답장은 응답을 돌려준 **뒤에** 따로 만든다.

응답과 따로, 뒤에서 하는 일을 **백그라운드 작업**이라고 부릅니다.

**비유**

식당 점원은 주문을 받으면 "주문 받았습니다"라고 바로 말합니다(응답). 요리는 주방에서 따로 만들어 나중에 가져다줍니다(백그라운드 작업). 요리가 다 될 때까지 손님을 계산대 앞에 세워 두지 않습니다.

**실제로 확인한 것** (개발 기록 4번)

- 로컬 시험: 서버가 응답을 돌려주기까지 0.02초 걸렸습니다. 답장은 그 뒤에 보내졌습니다.
- 실제 Slack: 명령어를 받고 0.3~0.5초 뒤에 답장 전송이 끝났습니다.

**Java 비교**

Spring에서 `@Async`가 붙은 메서드를 부르고, 끝나기를 기다리지 않고 바로 `ResponseEntity.ok()`를 돌려주는 것과 비슷합니다.

**자주 하는 실수: 답장을 다 보낸 뒤에 응답한다**

평소에는 빨라서 문제가 보이지 않습니다. NEIS가 느린 날에만 3초를 넘겨, Slack이 같은 이벤트를 다시 보냅니다. 가끔만 생기는 문제라서 원인을 찾기 어렵습니다.

---

### 2-2. `date`와 `timedelta`: 날짜 더하고 빼기

**설명**

`date`는 **날짜**(연, 월, 일)만 담는 객체입니다. 객체는 값과 그 값을 다루는 기능(메서드)을 함께 가진 것입니다. (step02 참고)

step03의 `datetime`은 날짜에 **시각**까지 담습니다. 이번 단계는 날짜만 필요해서 `date`를 씁니다.

```python
from datetime import date, datetime

print(date(2026, 11, 5))
print(datetime.strptime("20261105", "%Y%m%d"))
```

결과:

```
2026-11-05
2026-11-05 00:00:00
```

`datetime`에는 `00:00:00`(시각)이 붙어 있습니다. `date`에는 없습니다.

---

`date.today()`는 오늘 날짜를 돌려줍니다.

```python
from datetime import date

print(date.today())
```

결과 (이 문서를 쓴 날):

```
2026-11-05
```

---

`timedelta`는 "하루", "6일" 같은 **기간**입니다. 날짜에 더하거나 뺄 수 있습니다.

```python
from datetime import date, timedelta

today = date(2026, 11, 5)
print(today)
print(today + timedelta(days=1))
print(today.weekday())
print(today - timedelta(days=today.weekday()))
print(today.strftime("%Y%m%d"))
```

결과:

```
2026-11-05
2026-11-06
3
2026-11-02
20261105
```

- `today + timedelta(days=1)`: 하루 뒤인 11월 6일입니다.
- `today.weekday()`: 목요일이라 `3`입니다. 월요일이 0입니다. (step03 참고)
- `today - timedelta(days=3)`: 3일 전, 곧 이번 주 **월요일**(11월 2일)입니다.
- `strftime`은 2-3에서 설명합니다.

달이나 해가 바뀌어도 알아서 계산합니다. 2027년 1월 1일(금)의 월요일은 2026년 12월 28일입니다. (테스트 `test_this_week_across_new_year`)

**비유**

`date`는 달력의 한 칸입니다. `timedelta`는 "몇 칸 옮겨라"라는 쪽지입니다. 쪽지를 더하면 달력에서 그만큼 옮겨 갑니다.

**이 프로젝트 코드** (`app/commands.py` 59~66줄, 88줄)

```python
def week_start(today: date) -> date:
    # 이번 주 월요일. weekday()는 월요일이 0이라서, 그만큼 날짜를 빼면 월요일이 된다.
    return today - timedelta(days=today.weekday())


def week_end(today: date) -> date:
    # 이번 주 일요일 (월요일 + 6일)
    return week_start(today) + timedelta(days=6)
```

```python
        return make_lunch_reply(today + timedelta(days=1), NO_LUNCH_TOMORROW_TEXT)
```

오늘 날짜는 `app/notifier.py` 52줄의 `date.today()`에서 정합니다.

**Java 비교**

```java
LocalDate today = LocalDate.of(2026, 11, 5);
LocalDate tomorrow = today.plusDays(1);
LocalDate monday = today.minusDays(today.getDayOfWeek().getValue() - 1);  // Java는 월요일이 1
LocalDate now = LocalDate.now();
```

**자주 하는 실수: 날짜에 숫자를 그대로 더한다**

```python
from datetime import date

print(date(2026, 11, 5) + 1)
```

결과:

```
TypeError: unsupported operand type(s) for +: 'datetime.date' and 'int'
```

`1`만 보고는 1일인지 1시간인지 알 수 없습니다. 그래서 `timedelta(days=1)`처럼 단위를 밝혀야 합니다.

---

### 2-3. `strftime`: 날짜를 글자로

**설명**

`날짜.strftime(형식)`은 날짜를 **글자**로 바꿉니다. step03의 `strptime`과 반대 방향입니다.

- `strptime`: 글자 → 날짜 (p는 parse, "읽기")
- `strftime`: 날짜 → 글자 (f는 format, "모양 만들기")

`%Y`는 네 자리 연도, `%m`은 두 자리 월, `%d`는 두 자리 일입니다.

NEIS는 날짜를 `"20261105"` 모양의 글자로 받습니다. 그래서 날짜를 계산한 뒤 글자로 바꿔야 합니다.

**작은 예시**

```python
from datetime import date

print(date(2026, 11, 5).strftime("%Y%m%d"))
print(date(2027, 1, 3).strftime("%Y%m%d"))
```

결과:

```
20261105
20270103
```

1월과 3일도 `01`, `03`처럼 두 자리로 채워집니다.

**이 프로젝트 코드** (`app/commands.py` 54~56줄)

```python
def to_yyyymmdd(day: date) -> str:
    # NEIS가 받는 날짜 모양(예: "20261105")으로 바꾼다.
    return day.strftime("%Y%m%d")
```

**Java 비교**

```java
String text = day.format(DateTimeFormatter.ofPattern("yyyyMMdd"));
```

**자주 하는 실수: `%`를 빠뜨린다**

```python
from datetime import date

print(date(2026, 11, 5).strftime("Ymd"))
```

결과:

```
Ymd
```

오류 없이 글자 `Ymd`가 그대로 나옵니다. `%`가 붙어야 "여기에 연도를 넣어라"라는 뜻이 됩니다.

---

### 2-4. 기본값이 있는 매개변수

**설명**

매개변수 뒤에 `= 값`을 붙이면, 부를 때 그 값을 생략할 수 있습니다. 생략하면 적어 둔 값(기본값)이 들어갑니다.

**작은 예시**

```python
def greet(name: str, greeting: str = "안녕") -> str:
    return greeting + ", " + name


print(greet("급식봇"))
print(greet("급식봇", "반가워"))
```

결과:

```
안녕, 급식봇
반가워, 급식봇
```

첫 번째는 `greeting`을 생략해서 기본값 `"안녕"`이 들어갔습니다.

**이 프로젝트 코드** (`app/formatter.py` 117줄, 125줄)

```python
def format_lunch_message(meal_result: dict, meal_date: str, no_meal_text: str = NO_MEAL_TEXT) -> str:
    ...
    if lunch_row == {}:
        return title + "\n" + no_meal_text
```

- 정기 알림(`send_lunch_notification`)은 전처럼 두 값만 넘깁니다. 그러면 "오늘은 급식이 없습니다."가 들어갑니다.
- `내일 급식` 답장은 세 번째 값으로 "내일은 급식이 없습니다."를 넘깁니다.

기본값 덕분에 원래 이 함수를 부르던 곳(정기 알림, 테스트)은 하나도 고치지 않았습니다.

**Java 비교**

Java에는 기본값이 없어서, 보통 매개변수 개수가 다른 메서드를 하나 더 만듭니다(오버로딩).

```java
String formatLunchMessage(Map<String, Object> result, String date) {
    return formatLunchMessage(result, date, NO_MEAL_TEXT);
}

String formatLunchMessage(Map<String, Object> result, String date, String noMealText) { ... }
```

**자주 하는 실수: 기본값이 있는 매개변수를 앞에 둔다**

```python
def greet(greeting: str = "안녕", name: str) -> str:
    return greeting + ", " + name
```

결과:

```
SyntaxError: parameter without a default follows parameter with a default
```

기본값이 없는 매개변수가 기본값이 있는 매개변수 뒤에 올 수 없습니다. 기본값이 있는 것은 **맨 뒤**에 둡니다.

---

### 2-5. `continue`: 이번 차례만 건너뛰기

**설명**

`for` 반복 중에 `continue`를 만나면, 그 아래 줄을 실행하지 않고 **다음 차례**로 넘어갑니다. (`for`는 step02 참고)

**작은 예시**

```python
for name in ["수업공개의 날", "토요휴업일", "독서골든벨"]:
    if name == "토요휴업일":
        continue
    print(name)
```

결과:

```
수업공개의 날
독서골든벨
```

"토요휴업일" 차례에서 `continue`를 만나 `print`를 건너뛰었습니다. 그다음 "독서골든벨"은 그대로 출력됩니다.

**비유**

줄 선 사람들에게 하나씩 나눠 주다가, 받지 않을 사람의 차례면 그냥 다음 사람에게 넘어가는 것입니다.

**이 프로젝트 코드** (`app/formatter.py` 139~140줄)

```python
        if event_name in HIDDEN_EVENT_NAMES:
            continue
```

`HIDDEN_EVENT_NAMES`(`["토요휴업일"]`)에 있는 행사는 메시지에 넣지 않고 건너뜁니다.

**Java 비교**

Java의 `continue`와 똑같습니다.

**자주 하는 실수: `break`와 헷갈린다**

```python
for name in ["수업공개의 날", "토요휴업일", "독서골든벨"]:
    if name == "토요휴업일":
        break
    print(name)
```

결과:

```
수업공개의 날
```

`break`는 반복 **전체**를 끝냅니다. 그래서 뒤에 있던 "독서골든벨"까지 사라졌습니다.

---

### 2-6. 리스트가 든 딕셔너리 `dict[str, list[str]]`

**설명**

학사일정은 하루에 행사가 여러 개일 수 있습니다. 그래서 날짜(키)마다 행사 이름의 **리스트**(값)를 둡니다. (딕셔너리, 리스트는 step02 참고)

타입 힌트 `dict[str, list[str]]`는 "키는 문자열, 값은 문자열 리스트인 딕셔너리"라는 뜻입니다.

처음 보는 날짜에는 **빈 리스트를 먼저** 넣어야, 그 리스트에 `append`할 수 있습니다.

**작은 예시**

```python
events = {}
events["20261104"] = []
events["20261104"].append("수업공개의 날")
events["20261104"].append("독서골든벨")
print(events)
```

결과:

```
{'20261104': ['수업공개의 날', '독서골든벨']}
```

**비유**

날짜별 서랍장입니다. 처음 쓰는 날짜면 빈 서랍(빈 리스트)을 먼저 만들고, 그 서랍에 행사를 하나씩 넣습니다.

**이 프로젝트 코드** (`app/formatter.py` 130~146줄)

```python
def group_events_by_date(schedule_result: dict) -> dict[str, list[str]]:
    events_by_date = {}
    if "SchoolSchedule" not in schedule_result:
        return events_by_date
    for row in schedule_result["SchoolSchedule"][1]["row"]:
        event_date = row["AA_YMD"]
        event_name = row["EVENT_NM"].strip()
        if event_name in HIDDEN_EVENT_NAMES:
            continue
        if event_date not in events_by_date:
            events_by_date[event_date] = []
        # 같은 날 같은 행사가 두 번 들어 있는 경우가 있어서 한 번만 넣는다.
        if event_name not in events_by_date[event_date]:
            events_by_date[event_date].append(event_name)
    return events_by_date
```

(주석 일부는 줄였습니다.)

**Java 비교**

```java
Map<String, List<String>> eventsByDate = new HashMap<>();
if (!eventsByDate.containsKey(eventDate)) {
    eventsByDate.put(eventDate, new ArrayList<>());
}
eventsByDate.get(eventDate).add(eventName);
```

**자주 하는 실수: 빈 리스트를 넣지 않고 바로 `append` 한다**

```python
events = {}
events["20261105"].append("과학 하이챌린지")
```

결과:

```
KeyError: '20261105'
```

`"20261105"`라는 키가 아직 없어서, 꺼낼 리스트가 없습니다. Java에서 `map.get(key)`가 `null`이라 `.add`에서 `NullPointerException`이 나는 것과 같습니다.

---

### 2-7. `sorted`: 순서대로 늘어놓기

**설명**

`sorted(값들)`은 작은 것부터 늘어놓은 **새 리스트**를 돌려줍니다. 원래 것은 바꾸지 않습니다.

딕셔너리를 넣으면 **키**만 늘어놓은 리스트가 나옵니다.

`"20261102"` 같은 글자는 앞 글자부터 하나씩 비교합니다. 자릿수가 모두 같아서, 글자 순서가 곧 날짜 순서입니다.

**작은 예시**

```python
print(sorted(["20261106", "20261102", "20261104"]))
print(sorted({"20261106": ["b"], "20261102": ["a"]}))
```

결과:

```
['20261102', '20261104', '20261106']
['20261102', '20261106']
```

**이 프로젝트 코드** (`app/formatter.py` 149~155줄)

```python
def format_schedule_lines(schedule_result: dict) -> list[str]:
    # 날짜마다 한 줄: "11월 4일(수) 수업공개의 날, 독서골든벨"
    lines = []
    events_by_date = group_events_by_date(schedule_result)
    for event_date in sorted(events_by_date):
        lines.append(format_date(event_date) + " " + EVENT_SEPARATOR.join(events_by_date[event_date]))
    return lines
```

NEIS 응답의 순서에 기대지 않고 직접 늘어놓으므로, 메시지는 늘 날짜 순서입니다.

**Java 비교**

```java
List<String> dates = new ArrayList<>(eventsByDate.keySet());
Collections.sort(dates);
```

**자주 하는 실수: `리스트.sort()`의 결과를 쓰려고 한다**

```python
dates = ["20261106", "20261102", "20261104"]
print(dates.sort())
print(dates)
```

결과:

```
None
['20261102', '20261104', '20261106']
```

`리스트.sort()`는 원래 리스트를 직접 바꾸고, 돌려주는 값이 없습니다(`None`). 새 리스트가 필요하면 `sorted(리스트)`를 씁니다.

---

### 2-8. `if`와 `return`으로 갈래 나누기

**설명**

함수는 `return`을 만나면 **바로 끝납니다.** 그 아래 줄은 실행하지 않습니다.

그래서 `if`를 `else` 없이 나란히 써도, 맞는 `if` 하나만 실행됩니다. 맨 아래의 `return`은 "어느 것에도 해당하지 않으면"이라는 뜻이 됩니다.

**작은 예시**

```python
def reply(command: str) -> str:
    if command == "today_lunch":
        return "오늘 급식 답장"
    if command == "this_week_schedule":
        return "이번 주 일정 답장"
    return "도움말"


print(reply("today_lunch"))
print(reply("help"))
print(reply("아무 말"))
```

결과:

```
오늘 급식 답장
도움말
도움말
```

**이 프로젝트 코드** (`app/commands.py` 82~91줄)

```python
def build_reply(command: str, today: date) -> str:
    if command == TODAY_LUNCH:
        return make_lunch_reply(today, NO_MEAL_TEXT)
    if command == TOMORROW_LUNCH:
        return make_lunch_reply(today + timedelta(days=1), NO_LUNCH_TOMORROW_TEXT)
    if command == THIS_WEEK_SCHEDULE:
        return make_week_schedule_reply(today)
    return HELP_TEXT
```

`도움말`(`HELP`)은 따로 `if`를 두지 않았습니다. 맨 아래 `return HELP_TEXT`가 맡습니다.

**Java 비교**

```java
switch (command) {
    case TODAY_LUNCH: return makeLunchReply(today, NO_MEAL_TEXT);
    case TOMORROW_LUNCH: return makeLunchReply(today.plusDays(1), NO_LUNCH_TOMORROW_TEXT);
    case THIS_WEEK_SCHEDULE: return makeWeekScheduleReply(today);
    default: return HELP_TEXT;
}
```

**자주 하는 실수: `return`을 빠뜨린다**

```python
def reply(command: str) -> str:
    if command == "today_lunch":
        "오늘 급식 답장"
    return "도움말"


print(reply("today_lunch"))
```

결과:

```
도움말
```

글자를 적기만 하고 돌려주지 않았습니다. 그래서 아래로 내려가 "도움말"이 나왔습니다. 오류가 나지 않아서 찾기 어렵습니다. 이런 실수는 테스트로 잡습니다.

---

### 2-9. 함수를 값으로 넘기기

**설명**

함수 이름 뒤에 괄호를 붙이면 **지금 실행**합니다. 예: `say("안녕")`

괄호 없이 이름만 쓰면 **함수 그 자체**를 숫자나 글자처럼 다른 함수에 넘길 수 있습니다. 받은 쪽이 나중에 실행합니다.

**작은 예시**

```python
def say(text: str) -> None:
    print("말하기:", text)


def later(function, text: str) -> None:
    print("나중에 실행합니다")
    function(text)


later(say, "안녕")
```

결과:

```
나중에 실행합니다
말하기: 안녕
```

`later`에 `say`를 넘겼습니다. `later`가 먼저 "나중에 실행합니다"를 출력한 뒤, 받은 함수를 실행했습니다.

**비유**

요리를 해서 건네는 것(괄호를 붙여 실행)과, 요리법 카드를 건네는 것(이름만 넘기기)의 차이입니다. 카드를 받은 사람은 원할 때 요리합니다.

**이 프로젝트 코드** (`app/server.py` 82줄)

```python
            background_tasks.add_task(send_command_reply, event["channel"], command)
```

`send_command_reply`를 괄호 없이 넘깁니다. 그 뒤의 `event["channel"]`, `command`는 나중에 실행할 때 넣어 줄 값입니다.

**Java 비교**

Java에서는 메서드 참조나 람다로 넘깁니다.

```java
executor.execute(() -> sendCommandReply(channelId, command));
```

**자주 하는 실수: 괄호를 붙여서 넘긴다**

```python
later(say("안녕"), "안녕")
```

결과:

```
말하기: 안녕
나중에 실행합니다
...
TypeError: 'NoneType' object is not callable
```

1. `say("안녕")`이 **그 자리에서** 먼저 실행됩니다.
2. `say`는 돌려주는 값이 없어서(`-> None`) `None`이 넘어갑니다.
3. `later`가 `None`을 실행하려다 오류가 납니다. "`None`은 실행할 수 없다"는 뜻입니다.

---

### 2-10. FastAPI `BackgroundTasks`

**설명**

처리 함수의 매개변수 타입을 `BackgroundTasks`로 적으면, FastAPI가 그 객체를 만들어 넣어 줍니다.

`background_tasks.add_task(함수, 값1, 값2, ...)`로 함수를 맡깁니다. 맡긴 함수는 **응답을 돌려준 뒤에** 실행됩니다. (FastAPI 공식 문서)

**작은 예시** (`예시.py`, 연습용 서버를 8001번 포트로 켜고 요청을 보냈습니다)

```python
import time

from fastapi import BackgroundTasks, FastAPI
from fastapi.responses import PlainTextResponse

app = FastAPI()


def slow_job(name: str) -> None:
    time.sleep(2)
    print("뒤에서 끝난 일:", name)


@app.post("/good")
async def good(background_tasks: BackgroundTasks) -> PlainTextResponse:
    background_tasks.add_task(slow_job, "답장 보내기")
    print("응답을 먼저 돌려줍니다")
    return PlainTextResponse("ok")
```

요청을 보낸 쪽의 결과:

```
/good 200 ok | 응답까지 0.03 초
```

서버 화면:

```
응답을 먼저 돌려줍니다
INFO:     127.0.0.1:49691 - "POST /good HTTP/1.1" 200 OK
뒤에서 끝난 일: 답장 보내기
```

2초 걸리는 일을 맡겼는데도 응답은 0.03초 만에 왔습니다. 맡긴 일은 응답(`200 OK`) 다음에 끝났습니다.

**이 프로젝트 코드** (`app/server.py` 46줄, 80~82줄)

```python
async def receive_slack_event(request: Request, background_tasks: BackgroundTasks) -> PlainTextResponse:
```

```python
            # NEIS 조회와 Slack 전송은 3초를 넘길 수 있다.
            # 그래서 답장은 뒤에서(응답을 돌려준 다음에) 보내도록 맡겨 두고, Slack에는 바로 200을 돌려준다.
            background_tasks.add_task(send_command_reply, event["channel"], command)
```

**Java 비교**

Spring에서 `TaskExecutor`에 일을 넘기고 바로 응답하는 것과 비슷합니다. FastAPI는 "응답을 보낸 다음"이라는 때를 알아서 맞춰 줍니다.

**자주 하는 실수: 타입 힌트 `BackgroundTasks`를 빠뜨린다**

```python
@app.post("/no-hint")
async def no_hint(background_tasks) -> PlainTextResponse:
    return PlainTextResponse("ok")
```

결과 (요청을 보낸 쪽):

```
/no-hint 422 {"detail":[{"type":"missing","loc":["query","background_tasks"],"msg":"Field required","input":null}]}
```

FastAPI는 타입 힌트를 보고 무엇을 넣어 줄지 정합니다. 타입이 없으면 주소 뒤에 붙는 값(`?background_tasks=...`)으로 착각합니다. 그 값이 없어서 `422`(요청 내용이 맞지 않음)로 거부했습니다.

---

## 3. 코드 줄 단위 해설

### 3-1. `app/commands.py` (바뀐 부분)

| 줄 | 설명 |
| --- | --- |
| 7 | 날짜 계산에 쓸 `date`, `timedelta`를 가져옵니다. (2-2) |
| 9 | `.env`의 교육청 코드와 학교 코드를 가져옵니다. |
| 10 | 메시지를 만드는 함수와 "오늘은 급식이 없습니다." 문구(`NO_MEAL_TEXT`)를 `formatter.py`에서 가져옵니다. 정기 알림과 같은 문구를 쓰기 위해서입니다. |
| 11 | NEIS에서 급식과 학사일정을 가져오는 함수입니다. |
| 36~38 | `내일 급식`에 급식이 없을 때의 문구입니다. |
| 54~56 | `to_yyyymmdd`: 날짜를 `"20261105"` 모양의 글자로 바꿉니다. (2-3) |
| 59~61 | `week_start`: 이번 주 월요일을 구합니다. (2-2) |
| 64~66 | `week_end`: 월요일에 6일을 더해 일요일을 구합니다. |
| 69~72 | `make_lunch_reply`: 날짜를 글자로 바꾸고 → NEIS 조회 → 3단계 메시지 함수로 답장을 만듭니다. |
| 75~79 | `make_week_schedule_reply`: 월요일과 일요일을 구하고 → 그 사이 학사일정 조회 → 메시지로 만듭니다. |
| 82~91 | `build_reply`: 명령어마다 갈래를 나눕니다. (2-8) |

`build_reply`가 오늘 날짜(`today`)를 직접 구하지 않고 **매개변수로 받는** 이유가 있습니다. 테스트에서 원하는 날짜를 넣어 볼 수 있기 때문입니다.

NEIS 조회에 실패하면 `NeisError`가 생깁니다. 이 파일은 그 오류를 잡지 않고 부른 쪽(`notifier.py`)으로 그대로 올려 보냅니다. (step05 참고)

### 3-2. `app/formatter.py` (추가·수정된 부분)

| 줄 | 설명 |
| --- | --- |
| 21 | 학사일정이 없을 때의 문구 `"없음"`입니다. (CLAUDE.md 메시지 예시) |
| 25 | 메시지에서 뺄 행사 이름 목록입니다. 지금은 `"토요휴업일"` 하나입니다. |
| 28 | 같은 날 행사 사이에 넣을 구분자 `", "`입니다. |
| 117 | `no_meal_text` 매개변수를 기본값과 함께 추가했습니다. (2-4) |
| 125 | 급식이 없으면 넘겨받은 문구를 씁니다. |
| 130~146 | `group_events_by_date`: 날짜별로 묶습니다. (2-6) |
| 134~135 | 일정이 없는 기간은 `"SchoolSchedule"` 키 없이 `RESULT`만 옵니다. 그러면 빈 딕셔너리를 돌려줍니다. 급식 응답과 같은 모양입니다. (step03 참고) |
| 138 | 행사 이름 앞뒤의 빈칸을 지웁니다. (`strip`, step03 참고) |
| 139~140 | 숨길 행사면 건너뜁니다. (2-5) |
| 141~142 | 처음 보는 날짜면 빈 리스트를 먼저 넣습니다. |
| 144~145 | 같은 날에 같은 이름이 아직 없을 때만 넣습니다. 실제 응답에 같은 날 같은 행사가 두 번 온 경우가 있었습니다. (개발 기록) |
| 149~155 | `format_schedule_lines`: 날짜 순서대로 "11월 4일(수) 수업공개의 날, 독서골든벨" 같은 줄을 만듭니다. (2-7) |
| 158~166 | `format_week_schedule_message`: 제목 한 줄 + 날짜별 줄을 `\n`으로 이어 붙입니다. 줄이 없으면 `"없음"`입니다. |

### 3-3. `app/neis.py` (추가된 부분, 99~108줄)

```python
def fetch_schedules(office_code: str, school_code: str, from_date: str, to_date: str) -> dict:
    search_conditions = {
        "ATPT_OFCDC_SC_CODE": office_code,
        "SD_SCHUL_CODE": school_code,
        "AA_FROM_YMD": from_date,
        "AA_TO_YMD": to_date,
    }
    return call_neis_api("SchoolSchedule", search_conditions)
```

- 급식의 `fetch_meals`와 모양이 같습니다. 서비스 이름과 조건만 다릅니다.
- `AA_FROM_YMD`, `AA_TO_YMD`: 시작일과 끝일입니다. NEIS 학사일정 공식 명세에서 확인했습니다.
- 실패하면 한 번 더 시도하는 일은 5단계의 `call_neis_api`가 그대로 해 줍니다.

### 3-4. `app/notifier.py` (추가된 부분, 48~63줄)

| 줄 | 설명 |
| --- | --- |
| 48 | 답장을 보낼 대화방(`channel_id`)과 명령어를 받습니다. |
| 51~52 | 오늘 날짜로 답장 글을 만듭니다. |
| 53~55 | NEIS에서 정보를 받지 못하면 로그를 남기고 관리자에게 알립니다. (step05와 같은 방식) |
| 57 | 사용자에게는 "지금은 정보를 가져오지 못했습니다…"라고 답합니다. 아무 답이 없는 것보다 낫습니다. |
| 59 | 답장을 보냅니다. 토큰이 만료되면 새로 받아 다시 보내는 일은 `post_message`가 합니다. (step05 참고) |
| 60~63 | 성공하면 로그를 남기고, 실패하면 관리자에게 알립니다. |

이 함수는 응답을 돌려준 **뒤에** 실행됩니다. 그래서 여기서 오류가 나도 Slack에 보낸 응답은 이미 200입니다. 오류는 로그와 관리자 알림으로만 알 수 있습니다. 그래서 오류를 빠짐없이 기록하게 만들었습니다.

### 3-5. `app/server.py` (바뀐 부분)

| 줄 | 설명 |
| --- | --- |
| 14 | `BackgroundTasks`를 가져옵니다. (2-10) |
| 21 | 답장을 보내는 함수 `send_command_reply`를 가져옵니다. |
| 46 | 처리 함수에 `background_tasks: BackgroundTasks` 매개변수를 더했습니다. |
| 82 | 사람이 보낸 새 메시지일 때만 답장을 맡깁니다. 답장은 메시지가 온 대화방(`event["channel"]`)으로 갑니다. (2-9) |

봇의 답장도 Slack에서 이벤트로 다시 들어옵니다. 7단계에서 만든 `is_user_message`가 그것을 걸러 냅니다. 그래서 봇이 자기 답장에 또 답하는 일이 없습니다. (개발 기록 4번에서 확인)

### 3-6. 테스트 (8개 추가, 전체 60개)

- `tests/test_formatter.py` (3개)
  - `내일 급식` 문구를 넘기면 그 문구가 나오는지 확인합니다.
  - 학사일정을 날짜별로 묶고, 토요휴업일과 중복을 빼는지 확인합니다.
  - 일정이 없으면 `없음`이 나오는지 확인합니다.
- `tests/test_commands.py` (5개)
  - 날짜를 `"20261105"` 모양으로 바꾸는지 확인합니다.
  - 목요일·월요일·일요일, 해가 바뀌는 주의 월요일과 일요일을 확인합니다.
  - `도움말`은 NEIS 없이 바로 안내문이 나오는지 확인합니다.

급식·일정 답장은 NEIS에 실제로 요청해야 해서 테스트에 넣지 않았습니다. 대신 개발 기록 4번처럼 직접 실행해 확인했습니다.

---

## 4. 사용한 라이브러리

| 라이브러리 | 종류 | 이번에 쓴 것 | 뜻 |
| --- | --- | --- | --- |
| datetime | 표준 | `date(연, 월, 일)`, `date.today()`, `timedelta(days=숫자)`, `날짜.weekday()`, `날짜.strftime("%Y%m%d")` | 날짜 만들기, 오늘 날짜, 기간, 요일 번호, 날짜를 글자로 |
| FastAPI | 따로 설치 | `BackgroundTasks`, `background_tasks.add_task(함수, 값들...)` | 응답을 돌려준 뒤에 실행할 일을 맡깁니다. |
| (기본 기능) | 내장 | `sorted(값들)` | 작은 것부터 늘어놓은 새 리스트 |

---

## 5. 용어 정리

| 용어 | 쉬운 뜻 | 예시 |
| --- | --- | --- |
| 3초 규칙 | Slack이 이벤트를 보낸 뒤 3초 안에 응답을 받아야 한다는 규칙 | 늦으면 같은 이벤트를 다시 보냄 |
| 백그라운드 작업 | 응답과 따로, 뒤에서 하는 일 | 명령어 답장 보내기 |
| 기간 | 날짜에 더하거나 뺄 수 있는 길이 | `timedelta(days=1)` |
| 기본값 | 부를 때 생략하면 대신 들어가는 값 | `no_meal_text: str = NO_MEAL_TEXT` |
| 정렬 | 작은 것부터 순서대로 늘어놓기 | `sorted(["20261106", "20261102"])` |
| 함수를 값으로 넘기기 | 괄호 없이 함수 이름만 넘겨, 받은 쪽이 나중에 실행하게 하기 | `add_task(send_command_reply, ...)` |
| 422 | "요청 내용이 맞지 않음" 상태 코드 | 필요한 값이 빠진 요청 |
| 양방향 | 프로그램이 먼저 보내기도 하고, 사용자의 말에 답하기도 하는 것 | 정기 알림 + 명령어 답장 |

---

## 6. 확인 문제

### 문제 1. 코드 읽기: 출력은?

```python
from datetime import date, timedelta

today = date(2026, 12, 31)
print(today + timedelta(days=1))
print(today - timedelta(days=today.weekday()))
print((today + timedelta(days=1)).strftime("%Y%m%d"))
```

힌트: 2026년 12월 31일은 목요일입니다.

<details><summary>정답</summary>

```
2027-01-01
2026-12-28
20270101
```

- 하루를 더하면 해가 바뀌어 2027년 1월 1일입니다. `timedelta`가 알아서 계산합니다. (2-2)
- 목요일의 `weekday()`는 `3`입니다. 3일을 빼면 그 주 월요일인 12월 28일입니다.
- 1월 1일을 NEIS 모양 글자로 바꾸면 `20270101`입니다. (2-3)

</details>

### 문제 2. 빈칸 채우기

학사일정에서 "토요휴업일"은 빼고, 날짜별로 묶으려고 합니다. 빈칸에 들어갈 말은?

```python
    for row in schedule_result["SchoolSchedule"][1]["row"]:
        event_date = row["AA_YMD"]
        event_name = row["EVENT_NM"].strip()
        if event_name in HIDDEN_EVENT_NAMES:
            ________
        if event_date not in events_by_date:
            events_by_date[event_date] = __
        if event_name not in events_by_date[event_date]:
            events_by_date[event_date].append(event_name)
```

<details><summary>정답</summary>

- `continue`: 숨길 행사면 이번 차례만 건너뜁니다. `break`를 쓰면 그 뒤의 일정이 모두 사라집니다. (2-5)
- `[]`: 처음 보는 날짜에는 빈 리스트를 먼저 넣어야 `append`할 수 있습니다. 넣지 않으면 `KeyError`가 납니다. (2-6)

</details>

### 문제 3. 작은 수정: 서버를 이렇게 고쳤더니 이상합니다. 고치세요.

```python
            background_tasks.add_task(send_command_reply(event["channel"], command))
```

연습용 서버(2-10의 `예시.py`)에 같은 실수를 넣어 실행한 결과입니다.

```
/wrong 200 ok | 응답까지 2.03 초
```

서버 화면:

```
뒤에서 끝난 일: 답장 보내기
응답을 먼저 돌려줍니다
INFO:     127.0.0.1:49692 - "POST /wrong HTTP/1.1" 200 OK
ERROR:    Exception in ASGI application
...
TypeError: the first argument must be callable
```

<details><summary>정답</summary>

```python
            background_tasks.add_task(send_command_reply, event["channel"], command)
```

- 괄호를 붙이면 `send_command_reply`가 **그 자리에서** 실행됩니다. 그래서 답장을 다 보낸 뒤에야 응답이 갑니다. 연습용 서버에서는 2초짜리 일 때문에 응답이 2.03초 늦었습니다. 3초 규칙(2-1)을 지킬 수 없습니다.
- 그다음 `add_task`에는 함수의 결과인 `None`이 넘어갑니다. 응답 뒤에 `None`을 실행하려다 `TypeError`가 납니다. "첫 번째 값은 실행할 수 있는 것이어야 한다"는 뜻입니다. (2-9)
- 함수는 괄호 없이 넘기고, 넣을 값은 뒤에 차례로 적습니다.

</details>

---

## 이번 단계 핵심 정리

1. 서버는 Slack에 먼저 200을 돌려주고, 답장은 `BackgroundTasks`로 응답 뒤에 보낸다(3초 규칙).
2. 날짜는 `date`와 `timedelta`로 계산하고, `strftime("%Y%m%d")`로 NEIS 모양 글자로 바꾼다.
3. 학사일정은 `dict[str, list[str]]`로 날짜별로 묶고, 토요휴업일은 `continue`로 빼고, `sorted`로 날짜순으로 늘어놓는다.
4. 기본값이 있는 매개변수로, 기존 코드를 고치지 않고 "내일은 급식이 없습니다." 문구를 더했다.
5. 함수는 괄호 없이 넘겨야 받은 쪽이 나중에 실행한다.
