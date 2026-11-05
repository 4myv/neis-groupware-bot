# 3단계 학습 정리: 문자열 다루기, 날짜, 그리고 테스트

## 이 문서를 다 읽으면 할 수 있게 되는 것

1. 문자열을 나누고, 다듬고, 잘라서 원하는 부분만 꺼낼 수 있다.
2. `20261105` 같은 날짜 글자를 `11월 5일(목)`로 바꾸는 코드를 설명할 수 있다.
3. pytest로 테스트를 실행하고, 실패했을 때 화면을 읽고 원인을 찾을 수 있다.

## 읽기 전에

- 이번 단계는 새로 나온 것이 많습니다. 그래서 세 부분으로 나눴습니다. 한 번에 다 읽지 말고 한 부분씩 읽으세요.
  - **A. 문자열과 리스트 다루기** (2-1 ~ 2-7)
  - **B. 날짜와 메시지 만들기** (2-8 ~ 2-11)
  - **C. 테스트** (2-12 ~ 2-14)
- 코드 예시는 모두 실제로 실행한 결과를 붙였습니다. 오류 메시지의 긴 파일 경로는 `예시.py`처럼 줄여 적었습니다.
- 앞 단계에서 설명한 것은 "step01 참고", "step02 참고"라고만 적었습니다.

---

## 1. 이번 단계에서 새로 나온 것

**A. 문자열과 리스트 다루기**

1. `split`과 `strip`: 나누기와 다듬기
2. `endswith`, `rfind`, `isdigit`: 확인하고 찾기
3. 슬라이싱: `문자열[시작:끝]`
4. 빈 리스트와 `append`
5. `in`, `not in`, `not`
6. `join`: 리스트를 하나의 문자열로
7. 리스트 타입 힌트: `list[str]`, `list[dict]`

**B. 날짜와 메시지 만들기**

8. `datetime`: 날짜 글자를 날짜로
9. f-문자열: `f"{값}월"`
10. 줄바꿈 문자 `\n`과, 괄호로 긴 문자열 이어 쓰기
11. "없음"을 돌려주는 방법: `-1`, `[]`, `{}`

**C. 테스트**

12. pytest와 `assert`
13. 괄호로 여러 줄에 걸쳐 import 하기
14. `pytest.ini` 설정 파일

**앞 단계에서 설명한 것**

- step01 참고: `print`, 주석, 변수, `if`/`else`, `==`, `None`, 대문자 상수
- step02 참고: 함수, 딕셔너리, 리스트, `for`, 메서드, 문자열 `+`, `replace`

---

# A. 문자열과 리스트 다루기

## 2-1. `split`과 `strip`: 나누기와 다듬기

**설명**

`문자열.split(구분자)`는 문자열을 구분자가 있는 곳마다 잘라 **리스트**로 돌려줍니다.

`문자열.strip()`은 문자열 **양쪽 끝의 빈칸**을 지운 새 문자열을 돌려줍니다. 가운데 빈칸은 그대로 둡니다.

**비유**

`split`은 가위입니다. 표시(구분자)가 있는 곳마다 자릅니다.
`strip`은 양 끝 실밥을 정리하는 것입니다.

**작은 예시**

```python
text = "쌀밥<br/>된장찌개<br/>배추김치"
print(text.split("<br/>"))
```

결과:

```
['쌀밥', '된장찌개', '배추김치']
```

```python
dish = "  흑미밥 "
print("[" + dish + "]")
print("[" + dish.strip() + "]")
```

결과:

```
[  흑미밥 ]
[흑미밥]
```

빈칸이 보이도록 앞뒤에 `[ ]`를 붙여 출력했습니다.

**이 프로젝트 코드** (`app/formatter.py`의 `split_dishes`)

```python
for part in ddish_text.split("<br/>"):
    # 태그 앞뒤에 빈칸이 붙어 오는 경우가 있어서 양쪽 빈칸을 지운다.
    dish = part.strip()
```

실제 NEIS 응답은 `"흑미밥 <br/>부대찌개 ..."`처럼 `<br/>` 앞에 빈칸이 있습니다. 그래서 자른 뒤 `strip`으로 다듬습니다.

**Java 비교**

```java
String[] parts = text.split("<br/>");
String dish = part.strip();   // 또는 trim()
```

Java의 `split`은 배열을 돌려주고, Python의 `split`은 리스트를 돌려줍니다.

**자주 하는 실수: 구분자를 데이터와 다르게 쓴다**

```python
text = "쌀밥<br/>된장찌개"
print(text.split("<br>"))
```

결과:

```
['쌀밥<br/>된장찌개']
```

데이터에는 `<br/>`(슬래시 있음)가 있는데 `<br>`로 자르려고 했습니다.
구분자를 찾지 못하면 오류 없이 **통째로 한 칸짜리 리스트**가 나옵니다. 그래서 실수를 알아채기 어렵습니다.

---

## 2-2. `endswith`, `rfind`, `isdigit`: 확인하고 찾기

**설명**

`문자열.endswith(글자)`는 문자열이 그 글자로 끝나면 `True`, 아니면 `False`를 돌려줍니다.

`문자열.rfind(글자)`는 그 글자를 **뒤에서부터** 찾아 위치 번호를 돌려줍니다.
위치 번호는 리스트처럼 0부터 셉니다. (step02 참고) 찾지 못하면 오류 대신 `-1`을 돌려줍니다.

`문자열.isdigit()`은 문자열이 **숫자로만** 되어 있으면 `True`를 돌려줍니다. 빈 문자열이면 `False`입니다.

**작은 예시 1**

```python
dish = "부대찌개 (1.2.5.6)"
print(dish.endswith(")"))
print(dish.rfind("("))
print(dish.rfind("["))
```

결과:

```
True
5
-1
```

`부`(0) `대`(1) `찌`(2) `개`(3) 빈칸(4) `(`(5) 순서라서 `(`의 위치는 5입니다. `[`는 없어서 `-1`입니다.

**작은 예시 2**

```python
print("1256".isdigit())
print("1.2.5.6".isdigit())
print("1.2.5.6".replace(".", "").isdigit())
print("국물".isdigit())
print("".isdigit())
```

결과:

```
True
False
True
False
False
```

`replace`(step02 참고)로 점을 지운 뒤 검사하면 "숫자와 점으로만 된 글자"인지 알 수 있습니다.

**이 프로젝트 코드** (`find_allergy_start`)

```python
if not dish.endswith(")"):
    return -1
start = dish.rfind("(")
...
if inside.replace(".", "").isdigit():
    return start
```

- 알레르기 번호는 메뉴 이름 **맨 끝** 괄호에 있습니다. 그래서 `)`로 끝나는지 먼저 봅니다.
- `떡볶이(국물) (5.6)`처럼 괄호가 두 개일 수 있습니다. 그래서 **마지막** `(`를 찾으려고 `rfind`를 씁니다.
- 괄호 안이 숫자와 점으로만 되어 있을 때만 알레르기 번호로 봅니다.

**Java 비교**

```java
dish.endsWith(")");
dish.lastIndexOf("(");               // 없으면 -1
inside.replace(".", "").matches("\\d+");
```

**자주 하는 실수: 점이 섞인 글자에 바로 `isdigit`을 쓴다**

위 작은 예시 2의 두 번째 줄처럼 `"1.2.5.6".isdigit()`은 `False`입니다.
점(`.`)은 숫자가 아니기 때문입니다. 점을 먼저 지워야 합니다.

---

## 2-3. 슬라이싱: `문자열[시작:끝]`

**설명**

`문자열[시작:끝]`은 시작 번호부터 끝 번호 **바로 앞까지** 잘라 낸 새 문자열을 돌려줍니다. 끝 번호 칸은 들어가지 않습니다.

시작을 비우면 맨 처음부터, 끝을 비우면 맨 끝까지라는 뜻입니다.

번호에 음수를 쓰면 뒤에서부터 셉니다. `-1`은 맨 마지막 글자입니다.

**비유**

자로 길이를 재는 것과 같습니다. 0cm부터 4cm까지 자르면 0, 1, 2, 3 칸이 잘립니다. 4는 "끝나는 눈금"이라 칸에 들어가지 않습니다.

**작은 예시**

```python
dish = "부대찌개 (1.2.5.6)"
print(dish[0:4])
print(dish[:4])
print(dish[6:-1])
print(dish[-1])
```

결과:

```
부대찌개
부대찌개
1.2.5.6
)
```

- `dish[6:-1]`은 6번(`1`)부터 마지막 글자(`)`) 바로 앞까지입니다. 괄호 안쪽만 꺼낸 것입니다.
- 리스트에도 같은 방법을 쓸 수 있습니다.

**이 프로젝트 코드**

```python
inside = dish[start + 1:-1]          # 괄호 안쪽: "(" 다음 칸부터 ")" 바로 앞까지
return dish[:start].strip()          # 괄호 앞의 메뉴 이름
```

**Java 비교**

```java
dish.substring(start + 1, dish.length() - 1);
dish.substring(0, start);
```

Java의 `substring(시작, 끝)`도 끝 번호 칸을 넣지 않습니다. 같은 규칙입니다. Java에는 음수 번호가 없습니다.

**자주 하는 실수: 끝 번호 칸도 들어간다고 생각한다**

```python
dish = "부대찌개 (1.2.5.6)"
print(dish[6:12])
```

결과:

```
1.2.5.
```

12번 칸(`6`)까지 들어갈 것 같지만, 끝 번호 칸은 빠집니다.

---

## 2-4. 빈 리스트와 `append`

**설명**

`[]`는 아무것도 없는 빈 리스트입니다.

`리스트.append(값)`은 리스트 **맨 뒤에 값 하나를 추가**합니다. 리스트 자체가 바뀝니다.

빈 리스트를 만들고, `for`로 돌면서 `append`로 하나씩 채우는 모양을 자주 씁니다.

**작은 예시**

```python
numbers = []
numbers.append("5")
numbers.append("6")
print(numbers)
```

결과:

```
['5', '6']
```

**이 프로젝트 코드** (`extract_allergy_numbers`)

```python
numbers = []
for part in inside.split("."):
    # "5.6.9."처럼 끝에 점이 있으면 마지막 조각이 빈 문자열이 되므로 건너뛴다.
    if part != "":
        numbers.append(part)
return numbers
```

`"5.6.9."`를 점으로 자르면 `['5', '6', '9', '']`가 됩니다. 마지막 빈 조각은 넣지 않습니다.

**Java 비교**

```java
List<String> numbers = new ArrayList<>();
numbers.add("5");
```

**자주 하는 실수: `append`의 결과를 다시 변수에 넣는다**

```python
numbers = []
numbers = numbers.append("5")
print(numbers)
```

결과:

```
None
```

`append`는 리스트를 직접 바꾸고, 돌려주는 값은 `None`입니다.
그래서 그 결과를 `numbers`에 다시 넣으면 리스트가 사라지고 `None`만 남습니다. `numbers.append("5")`만 쓰면 됩니다.

---

## 2-5. `in`, `not in`, `not`

**설명**

`키 in 딕셔너리`는 딕셔너리에 그 키가 있으면 `True`를 돌려줍니다.

`not in`은 그 반대입니다. 키가 **없으면** `True`입니다.

`not 조건`은 조건의 참과 거짓을 뒤집습니다.

**작은 예시 1**

```python
result = {"RESULT": {"CODE": "INFO-200"}}
print("mealServiceDietInfo" in result)
print("mealServiceDietInfo" not in result)
print("RESULT" in result)
```

결과:

```
False
True
True
```

**작은 예시 2**

```python
dish = "흑미밥"
print(dish.endswith(")"))
print(not dish.endswith(")"))
```

결과:

```
False
True
```

**이 프로젝트 코드**

```python
if "mealServiceDietInfo" not in meal_result:     # find_lunch_row
    return {}
```

```python
if not dish.endswith(")"):                       # find_allergy_start
    return -1
```

급식이 없는 날의 응답에는 `mealServiceDietInfo` 키가 없습니다. (step02 개발 기록 [C])
그래서 키가 있는지 먼저 확인합니다. 확인하지 않고 꺼내면 `KeyError`가 납니다. (step02 참고)

**Java 비교**

```java
if (!mealResult.containsKey("mealServiceDietInfo")) { return Map.of(); }
if (!dish.endsWith(")")) { return -1; }
```

Java의 `!`가 Python의 `not`입니다. Python은 기호 대신 영어 단어를 씁니다.

**자주 하는 실수: 안쪽 값도 `in`으로 찾아질 거라고 생각한다**

```python
result = {"RESULT": {"CODE": "INFO-200"}}
print("INFO-200" in result)
```

결과:

```
False
```

딕셔너리에 쓰는 `in`은 **바깥쪽 키**만 봅니다. `"INFO-200"`은 안쪽 딕셔너리의 값이라서 찾지 못합니다.

---

## 2-6. `join`: 리스트를 하나의 문자열로

**설명**

`구분자.join(리스트)`는 리스트의 문자열들을 구분자로 이어 붙인 하나의 문자열을 돌려줍니다.
`split`의 반대 일입니다.

**작은 예시**

```python
names = ["흑미밥", "부대찌개", "백김치"]
print(" / ".join(names))
```

결과:

```
흑미밥 / 부대찌개 / 백김치
```

**이 프로젝트 코드** (`join_dish_names`)

```python
return DISH_SEPARATOR.join(names)       # DISH_SEPARATOR는 " / "
```

**Java 비교**

```java
String.join(" / ", names);
```

Java는 `String.join(구분자, 목록)`입니다. Python은 구분자 문자열의 메서드입니다.

**자주 하는 실수: 리스트의 메서드라고 생각한다**

```python
names = ["흑미밥", "부대찌개", "백김치"]
print(names.join(" / "))
```

결과:

```
Traceback (most recent call last):
  File "예시.py", line 2, in <module>
    print(names.join(" / "))
          ^^^^^^^^^^
AttributeError: 'list' object has no attribute 'join'
```

`AttributeError`는 "그 객체에 그런 기능이 없다"는 오류입니다. `join`은 리스트가 아니라 **구분자 문자열**에 딸린 메서드입니다.

---

## 2-7. 리스트 타입 힌트: `list[str]`, `list[dict]`

**설명**

리스트를 돌려주는 함수는 리스트 **안에 무엇이 들었는지**까지 적을 수 있습니다.

- `list[str]`: 문자열이 든 리스트
- `list[dict]`: 딕셔너리가 든 리스트

타입 힌트이므로 실행할 때 검사하지는 않습니다. (step01 참고)

**작은 예시**

```python
def first_dish(dishes: list[str]) -> str:
    return dishes[0]


print(first_dish(["흑미밥", "백김치"]))
```

결과:

```
흑미밥
```

**이 프로젝트 코드**

```python
WEEKDAY_NAMES: list[str] = ["월", "화", "수", "목", "금", "토", "일"]

def split_dishes(ddish_text: str) -> list[str]:
def parse_dishes(ddish_text: str) -> list[dict]:
```

**Java 비교**

```java
List<String> splitDishes(String ddishText)
List<Map<String, Object>> parseDishes(String ddishText)
```

Java의 제네릭 `<String>`이 Python에서는 `[str]`입니다.

**자주 하는 실수: Java 습관으로 대문자 `List`를 쓴다**

```python
def first_dish(dishes: List[str]) -> str:
    return dishes[0]
```

결과:

```
Traceback (most recent call last):
  File "예시.py", line 1, in <module>
    def first_dish(dishes: List[str]) -> str:
                           ^^^^
NameError: name 'List' is not defined. Did you mean: 'list'?
```

Python 3.9부터는 소문자 `list`를 그대로 쓰면 됩니다.

---

# B. 날짜와 메시지 만들기

## 2-8. `datetime`: 날짜 글자를 날짜로

**설명**

`datetime`은 날짜와 시각을 다루는 표준 라이브러리입니다.

`datetime.strptime(글자, 형식)`은 날짜 모양의 **글자**를 진짜 **날짜 객체**로 바꿉니다.
형식은 글자가 어떻게 생겼는지 알려 주는 약속입니다.

| 형식 코드 | 뜻 | 예 |
| --- | --- | --- |
| `%Y` | 네 자리 연도 | 2026 |
| `%m` | 두 자리 월 | 11 |
| `%d` | 두 자리 일 | 05 |

날짜 객체는 `.month`(월), `.day`(일) 같은 값을 가지고 있습니다. 객체에 딸린 이런 값을 **속성**이라고 합니다. 메서드(step02 참고)와 달리 괄호 없이 씁니다.

`.weekday()`는 요일 번호를 돌려주는 메서드입니다. **월요일이 0, 일요일이 6**입니다.

**작은 예시**

```python
from datetime import datetime

meal_day = datetime.strptime("20261105", "%Y%m%d")
print(meal_day)
print(meal_day.month, meal_day.day)
print(meal_day.weekday())
```

결과:

```
2026-11-05 00:00:00
11 5
3
```

2026년 11월 5일은 목요일이라서 `3`입니다. (월 0, 화 1, 수 2, 목 3)

번호를 요일 이름으로 바꿀 때는 리스트를 씁니다.

```python
WEEKDAY_NAMES = ["월", "화", "수", "목", "금", "토", "일"]
print(WEEKDAY_NAMES[3])
```

결과:

```
목
```

**이 프로젝트 코드** (`format_date`)

```python
meal_day = datetime.strptime(yyyymmdd, "%Y%m%d")
weekday_name = WEEKDAY_NAMES[meal_day.weekday()]
return f"{meal_day.month}월 {meal_day.day}일({weekday_name})"
```

`meal_day.month`는 `11`, `meal_day.day`는 `5`처럼 **숫자**입니다. 그래서 `05`가 아니라 `5`로 나옵니다.

**Java 비교**

```java
LocalDate mealDay = LocalDate.parse("20261105", DateTimeFormatter.ofPattern("yyyyMMdd"));
mealDay.getMonthValue();       // 11
mealDay.getDayOfWeek();        // THURSDAY
```

Java의 `getDayOfWeek().getValue()`는 월요일이 **1**입니다. Python의 `weekday()`는 월요일이 **0**입니다.

**자주 하는 실수: 글자 모양과 형식이 다르다**

```python
from datetime import datetime

datetime.strptime("2026-11-05", "%Y%m%d")
```

결과 (마지막 줄):

```
ValueError: time data '2026-11-05' does not match format '%Y%m%d'
```

글자에는 `-`가 있는데 형식에는 없습니다. `ValueError`는 "값이 기대한 모양이 아니다"라는 오류입니다.

---

## 2-9. f-문자열: `f"{값}월"`

**설명**

문자열 앞에 `f`를 붙이면, 안에 쓴 `{ }` 자리에 변수의 값이 들어갑니다. 이것을 f-문자열이라고 합니다.

숫자도 문자열로 바꿔 넣어 줍니다. 그래서 step02에서 본 "문자열 + 숫자" 오류가 나지 않습니다.

**작은 예시**

```python
month = 11
day = 5
print(f"{month}월 {day}일")
```

결과:

```
11월 5일
```

**이 프로젝트 코드**

```python
return f"{meal_day.month}월 {meal_day.day}일({weekday_name})"     # format_date
title = f"[{format_date(meal_date)} 중식]"                          # format_lunch_message
```

`{ }` 안에는 변수뿐 아니라 `format_date(meal_date)` 같은 함수 호출도 쓸 수 있습니다.

**Java 비교**

```java
String.format("%d월 %d일", month, day);
```

**자주 하는 실수: 앞의 `f`를 빠뜨린다**

```python
month = 11
print("{month}월")
```

결과:

```
{month}월
```

`f`가 없으면 그냥 문자열이라서 `{month}`가 글자 그대로 나옵니다.

---

## 2-10. 줄바꿈 문자 `\n`과, 괄호로 긴 문자열 이어 쓰기

**설명**

문자열 안의 `\n`은 "여기서 줄을 바꿔라"라는 뜻의 글자 하나입니다. 화면에는 `\n` 대신 줄이 바뀌어 보입니다.

긴 문자열은 괄호 `( )` 안에서 여러 줄로 나눠 쓸 수 있습니다. 붙어 있는 문자열들은 하나로 이어집니다.

**작은 예시 1**

```python
print("[11월 5일(목) 중식]" + "\n" + "흑미밥 / 백김치")
```

결과:

```
[11월 5일(목) 중식]
흑미밥 / 백김치
```

**작은 예시 2**

```python
text = (
    "[11월 5일(목) 중식]\n"
    "흑미밥 / 백김치"
)
print(text)
```

결과:

```
[11월 5일(목) 중식]
흑미밥 / 백김치
```

**이 프로젝트 코드**

```python
return title + "\n" + join_dish_names(dishes)       # app/formatter.py
```

```python
assert format_lunch_message(MEAL_RESULT_WITH_LUNCH, "20261105") == (     # tests/test_formatter.py
    "[11월 5일(목) 중식]\n"
    "흑미밥 / 부대찌개 / 호박볶음 / 오지치즈스틱 / 고등어구이 / 백김치"
)
```

**Java 비교**

Java도 `"\n"`을 씁니다. Java는 긴 문자열을 `+`로 이어 쓰거나, 텍스트 블록(`"""`)을 씁니다.

**자주 하는 실수: 슬래시 방향을 바꿔 쓴다**

```python
print("[11월 5일(목) 중식]" + "/n" + "흑미밥 / 백김치")
```

결과:

```
[11월 5일(목) 중식]/n흑미밥 / 백김치
```

줄바꿈은 역슬래시 `\`(키보드에 따라 `₩`로 보임)입니다. `/n`은 그냥 글자 두 개입니다.

---

## 2-11. "없음"을 돌려주는 방법: `-1`, `[]`, `{}`

**설명**

함수가 찾는 것을 찾지 못했을 때도 무언가를 돌려줘야 합니다. 이 프로젝트에서는 돌려주는 타입에 맞춰 "없음" 표시를 정했습니다.

| 함수 | 돌려주는 타입 | "없음" 표시 |
| --- | --- | --- |
| `find_allergy_start` | 위치 번호 `int` | `-1` (`rfind`와 같은 약속) |
| `extract_allergy_numbers` | `list[str]` | 빈 리스트 `[]` |
| `find_lunch_row` | `dict` | 빈 딕셔너리 `{}` |

타입이 늘 같으니, 받는 쪽은 `None`(step01 참고)인지 따로 걱정하지 않아도 됩니다.

**작은 예시**

```python
lunch_row = {}
print(lunch_row == {})
print({"MMEAL_SC_CODE": "2"} == {})
```

결과:

```
True
False
```

**이 프로젝트 코드** (`format_lunch_message`)

```python
lunch_row = find_lunch_row(meal_result)
if lunch_row == {}:
    return title + "\n" + NO_MEAL_TEXT
```

**Java 비교**

```java
return Map.of();          // 빈 Map
if (lunchRow.isEmpty()) { ... }
```

Java에서도 `null` 대신 빈 컬렉션을 돌려주는 것을 좋은 습관으로 봅니다.

**자주 하는 실수: 빈 딕셔너리를 `None`과 비교한다**

```python
lunch_row = {}
print(lunch_row == None)
print(lunch_row == {})
```

결과:

```
False
True
```

`{}`는 `None`이 아닙니다. 함수가 무엇을 "없음"으로 돌려주는지 확인하고 그것과 비교해야 합니다.

---

# C. 테스트

## 2-12. pytest와 `assert`

**설명**

테스트는 "이 함수에 이것을 넣으면 이것이 나와야 한다"를 코드로 적어 두고, 자동으로 확인하는 것입니다.
코드를 고친 뒤에도 예전 기능이 그대로인지 한 번에 확인할 수 있습니다.

`assert 조건`은 조건이 참이면 아무 일도 하지 않고, 거짓이면 `AssertionError`를 냅니다.

pytest는 테스트를 찾아 실행해 주는 외부 라이브러리입니다. 아래 규칙으로 테스트를 찾습니다.

- 파일 이름이 `test_`로 시작한다. (예: `test_formatter.py`)
- 그 파일 안의 함수 이름이 `test_`로 시작한다. (예: `def test_format_date_sunday():`)

**작은 예시 1: `assert`**

```python
assert 1 + 1 == 2
print("첫 번째 assert 통과")
assert 1 + 1 == 3
print("여기는 실행되지 않음")
```

결과:

```
첫 번째 assert 통과
Traceback (most recent call last):
  File "예시.py", line 3, in <module>
    assert 1 + 1 == 3
           ^^^^^^^^^^
AssertionError
```

**작은 예시 2: 통과 1개, 실패 1개인 테스트 파일**

```python
# test_demo.py
def add_suffix(name: str) -> str:
    return name + "고등학교"


def test_add_suffix():
    assert add_suffix("서울") == "서울고등학교"


def test_add_suffix_wrong_expectation():
    assert add_suffix("서울") == "서울고"
```

`python -m pytest`로 실행한 결과:

```
collected 2 items

test_demo.py .F                                                          [100%]

================================== FAILURES ===================================
______________________ test_add_suffix_wrong_expectation ______________________

    def test_add_suffix_wrong_expectation():
>       assert add_suffix("서울") == "서울고"
E       AssertionError: assert '서울고등학교' == '서울고'
E         
E         - 서울고
E         + 서울고등학교

test_demo.py:10: AssertionError
=========================== short test summary info ===========================
FAILED test_demo.py::test_add_suffix_wrong_expectation - AssertionError: asse...
========================= 1 failed, 1 passed in 0.07s =========================
```

결과 화면 읽는 법은 다음과 같습니다.

| 부분 | 뜻 |
| --- | --- |
| `.F` | 테스트 하나당 한 글자. `.`은 통과, `F`는 실패 |
| `>` 표시 줄 | 실패한 줄 |
| `E  assert '서울고등학교' == '서울고'` | 왼쪽은 실제 값, 오른쪽은 기대한 값 |
| `- 서울고` / `+ 서울고등학교` | `-`는 기대한 값, `+`는 실제로 나온 값 |
| `1 failed, 1 passed` | 실패 1개, 통과 1개 |

**이 프로젝트 코드** (`tests/test_formatter.py`)

```python
def test_format_date_sunday():
    assert format_date("20261108") == "11월 8일(일)"
```

**실행 방법과 실제 결과** (프로젝트 최상위 폴더에서)

```powershell
python -m pytest
```

```
collected 20 items

tests\test_formatter.py ....................                             [100%]

============================= 20 passed in 0.12s ==============================
```

`-v`를 붙이면(`python -m pytest -v`) 테스트마다 이름과 `PASSED`가 한 줄씩 나옵니다.

**Java 비교** (JUnit)

```java
@Test
void formatDateSunday() {
    assertEquals("11월 8일(일)", Formatter.formatDate("20261108"));
}
```

JUnit은 `@Test`로 테스트를 표시합니다. pytest는 **이름**(`test_`)으로 찾습니다.

**자주 하는 실수: 함수 이름을 `test_`로 시작하지 않는다**

```python
def check_add_suffix():
    assert add_suffix("서울") == "서울고등학교"
```

결과:

```
collected 0 items

============================ no tests ran in 0.03s ============================
```

오류도 아니고 실패도 아닙니다. 테스트를 **하나도 찾지 못한 것**입니다. 테스트가 통과한 줄 알고 넘어가기 쉽습니다.

---

## 2-13. 괄호로 여러 줄에 걸쳐 import 하기

**설명**

한 모듈에서 가져올 이름이 많으면 괄호 `( )` 안에 한 줄에 하나씩 쓸 수 있습니다. (한 줄에 여러 이름 가져오기는 step02 참고)

**이 프로젝트 코드** (`tests/test_formatter.py`)

```python
from app.formatter import (
    extract_allergy_numbers,
    find_lunch_row,
    format_date,
    format_lunch_message,
    parse_dishes,
    remove_allergy_numbers,
    split_dishes,
)
```

이름을 가나다(알파벳)순으로 적어 두면, 무엇을 가져왔는지 찾기 쉽습니다.

**Java 비교**

Java는 한 줄에 하나씩 `import`를 씁니다. 괄호로 묶는 문법은 없습니다.

**자주 하는 실수: 줄 끝 쉼표를 빠뜨린다**

```python
from math import (
    ceil
    floor,
)
```

결과:

```
  File "예시.py", line 3
    floor,
    ^^^^^
SyntaxError: invalid syntax
```

`ceil` 뒤에 쉼표가 없습니다. 마지막 줄(`floor,`) 뒤의 쉼표는 있어도 되고 없어도 됩니다.

---

## 2-14. `pytest.ini` 설정 파일

**설명**

`pytest.ini`는 pytest가 실행될 때 먼저 읽는 설정 파일입니다. 프로젝트 최상위 폴더에 둡니다.

```
[pytest]
pythonpath = .
testpaths = tests
```

- `pythonpath = .`: 프로젝트 최상위 폴더(`.`은 "지금 폴더")에서 모듈을 찾게 합니다.
- `testpaths = tests`: 테스트는 `tests` 폴더에서만 찾습니다.
- `#`로 시작하는 줄은 주석입니다. 이 프로젝트의 `pytest.ini`에는 왜 이 설정을 넣었는지 주석으로 적어 두었습니다.

**왜 필요한가요?**

`python -m pytest`로 실행하면 Python이 지금 폴더를 모듈 찾는 곳에 넣어 줍니다. 그래서 `from app.formatter import ...`가 됩니다.
`pytest`만 치면 그렇게 해 주지 않습니다. 이 설정이 그 일을 대신 합니다.

**자주 하는 실수: 설정 없이 `pytest`만 친다**

이 설정을 넣기 전에 `pytest`만 쳤을 때 실제로 나온 결과입니다. (step03 개발 기록 문제 1)

```
ERROR collecting tests/test_formatter.py
...
E   ModuleNotFoundError: No module named 'app'
...
!!!!!!!!!!!!!!!!!!! Interrupted: 1 error during collection !!!!!!!!!!!!!!!!!!!!
```

지금은 `pytest.ini`가 있어서 `pytest`와 `python -m pytest` 모두 동작합니다.

---

## 3. 코드 줄 단위 해설: `app/formatter.py` (새 파일)

### 1~18줄: 설명과 상수

```python
from datetime import datetime

# MMEAL_SC_CODE 값 중 중식. 실제 응답에서 "2"가 중식, "3"이 석식이었다. (step02 개발 기록 6번)
LUNCH_CODE: str = "2"

# 급식 데이터가 없는 날(주말, 방학, 공휴일)에 보낼 문구. 오류가 아니라 정상 상황이다.
NO_MEAL_TEXT: str = "오늘은 급식이 없습니다."

# datetime의 weekday()는 월요일을 0, 일요일을 6으로 돌려준다. 그 번호 순서대로 적었다.
WEEKDAY_NAMES: list[str] = ["월", "화", "수", "목", "금", "토", "일"]

# 메시지에서 메뉴와 메뉴 사이에 넣을 구분자
DISH_SEPARATOR: str = " / "
```

| 줄 | 설명 |
| --- | --- |
| 6 | 표준 라이브러리 `datetime` 모듈에서 `datetime`을 가져옵니다. 모듈 이름과 가져오는 이름이 같아서 헷갈릴 수 있습니다. (2-8) |
| 9 | 중식을 뜻하는 식사코드입니다. 문자열 `"2"`입니다. NEIS가 숫자가 아니라 문자열로 보내기 때문입니다. |
| 12 | 급식이 없는 날 보낼 문구입니다. CLAUDE.md 변환 규칙의 문구 그대로입니다. |
| 15 | 요일 이름을 `weekday()` 번호 순서대로 담은 리스트입니다. (2-7, 2-8) |
| 18 | 메뉴 사이 구분자입니다. 앞뒤 빈칸까지 포함합니다. |

### 21~29줄: `split_dishes` — `<br/>`로 나누고 다듬기

```python
def split_dishes(ddish_text: str) -> list[str]:
    # NEIS는 메뉴 사이를 줄바꿈 태그 <br/>로 이어 보낸다. 예: "흑미밥 <br/>부대찌개 (1.2.5.6)"
    dishes = []
    for part in ddish_text.split("<br/>"):
        # 태그 앞뒤에 빈칸이 붙어 오는 경우가 있어서 양쪽 빈칸을 지운다.
        dish = part.strip()
        if dish != "":
            dishes.append(dish)
    return dishes
```

| 줄 | 설명 |
| --- | --- |
| 23 | 결과를 담을 빈 리스트입니다. (2-4) |
| 24 | `<br/>`로 잘라 생긴 조각을 하나씩 꺼냅니다. (2-1) |
| 26 | 조각 양쪽 빈칸을 지웁니다. |
| 27~28 | 빈 조각이 아닐 때만 결과에 넣습니다. 데이터가 `<br/>`로 끝나는 경우를 대비한 것입니다. |
| 29 | 메뉴 목록을 돌려줍니다. |

### 32~45줄: `find_allergy_start` — 알레르기 괄호의 위치 찾기

```python
def find_allergy_start(dish: str) -> int:
    # 메뉴 이름 맨 끝의 알레르기 번호 괄호가 시작하는 위치를 돌려준다. 없으면 -1을 돌려준다.
    # 실제 응답은 "부대찌개 (1.2.5.6)", CLAUDE.md 예시는 "된장찌개(5.6.9.)" 모양이라 둘 다 다룬다.
    if not dish.endswith(")"):
        return -1
    start = dish.rfind("(")
    if start == -1:
        return -1
    inside = dish[start + 1:-1]
    # "떡볶이(국물)"처럼 메뉴 이름의 일부인 괄호는 지우면 안 되므로,
    # 괄호 안이 숫자와 점으로만 되어 있을 때만 알레르기 번호로 본다.
    if inside.replace(".", "").isdigit():
        return start
    return -1
```

| 줄 | 설명 |
| --- | --- |
| 35~36 | `)`로 끝나지 않으면 알레르기 번호가 없는 것입니다. 바로 `-1`을 돌려주고 끝냅니다. (2-2, 2-5) |
| 37 | 마지막 `(`의 위치를 찾습니다. (2-2) |
| 38~39 | `(`가 없으면 `-1`입니다. `사과)`처럼 짝이 안 맞는 경우를 대비합니다. |
| 40 | 괄호 안쪽 글자만 잘라 냅니다. (2-3) |
| 43~44 | 점을 지웠을 때 숫자로만 되어 있으면 알레르기 번호입니다. 괄호 위치를 돌려줍니다. |
| 45 | 그 밖의 경우(`(국물)`, `(1/2)`, `(40g)` 등)는 메뉴 이름의 일부로 보고 `-1`을 돌려줍니다. |

함수가 중간에 `return`을 만나면 그 자리에서 끝납니다. 그래서 조건에 맞지 않는 경우를 위에서 하나씩 먼저 걸러 냅니다.

### 48~52줄: `remove_allergy_numbers` — 알레르기 번호 지우기

```python
def remove_allergy_numbers(dish: str) -> str:
    start = find_allergy_start(dish)
    if start == -1:
        return dish.strip()
    return dish[:start].strip()
```

| 줄 | 설명 |
| --- | --- |
| 49 | 알레르기 괄호의 위치를 찾습니다. |
| 50~51 | 없으면 메뉴 이름을 그대로(양쪽 빈칸만 지우고) 돌려줍니다. |
| 52 | 있으면 괄호 앞까지 잘라 낸 뒤 빈칸을 지웁니다. `부대찌개 (1.2)`의 괄호 앞 빈칸도 이때 지워집니다. |

### 55~66줄: `extract_allergy_numbers` — 알레르기 번호 따로 보관하기

```python
def extract_allergy_numbers(dish: str) -> list[str]:
    # 알레르기 번호는 버리지 않고 따로 보관한다. 나중에 "알레르기" 명령어로 확장할 수 있다.
    start = find_allergy_start(dish)
    if start == -1:
        return []
    inside = dish[start + 1:-1]
    numbers = []
    for part in inside.split("."):
        # "5.6.9."처럼 끝에 점이 있으면 마지막 조각이 빈 문자열이 되므로 건너뛴다.
        if part != "":
            numbers.append(part)
    return numbers
```

| 줄 | 설명 |
| --- | --- |
| 57~59 | 알레르기 괄호가 없으면 빈 리스트를 돌려줍니다. (2-11) |
| 60 | 괄호 안쪽(`5.6.9.`)만 잘라 냅니다. |
| 62~65 | 점으로 자른 조각 중 빈 것이 아닌 것만 모읍니다. (2-1, 2-4) |
| 66 | `['5', '6', '9']` 같은 리스트를 돌려줍니다. |

### 69~78줄: `parse_dishes` — 메뉴마다 이름과 번호를 짝짓기

```python
def parse_dishes(ddish_text: str) -> list[dict]:
    # 메뉴마다 이름과 알레르기 번호를 짝지어 담는다.
    dishes = []
    for raw_dish in split_dishes(ddish_text):
        dish = {
            "name": remove_allergy_numbers(raw_dish),
            "allergy_numbers": extract_allergy_numbers(raw_dish),
        }
        dishes.append(dish)
    return dishes
```

| 줄 | 설명 |
| --- | --- |
| 72 | `split_dishes`가 돌려준 리스트를 바로 `for`로 돕니다. |
| 73~76 | 메뉴 하나를 딕셔너리 하나로 만듭니다. 이름과 알레르기 번호가 함께 보관됩니다. (step02 딕셔너리) |
| 78 | `[{"name": "흑미밥", "allergy_numbers": []}, ...]` 모양의 리스트를 돌려줍니다. |

### 81~85줄: `format_date` — 날짜를 읽기 쉽게

```python
def format_date(yyyymmdd: str) -> str:
    # "20261105" → "11월 5일(목)"
    meal_day = datetime.strptime(yyyymmdd, "%Y%m%d")
    weekday_name = WEEKDAY_NAMES[meal_day.weekday()]
    return f"{meal_day.month}월 {meal_day.day}일({weekday_name})"
```

| 줄 | 설명 |
| --- | --- |
| 83 | 글자를 날짜 객체로 바꿉니다. (2-8) |
| 84 | 요일 번호(0~6)로 요일 이름 리스트에서 이름을 꺼냅니다. |
| 85 | f-문자열로 `11월 5일(목)`을 만듭니다. (2-9) |

### 88~97줄: `find_lunch_row` — 중식 고르기

```python
def find_lunch_row(meal_result: dict) -> dict:
    # 급식이 없는 날은 "mealServiceDietInfo" 키 없이 RESULT만 온다. (step02 개발 기록 4번 [C])
    # 그런 날과, 석식만 있고 중식이 없는 날은 빈 딕셔너리를 돌려준다.
    if "mealServiceDietInfo" not in meal_result:
        return {}
    rows = meal_result["mealServiceDietInfo"][1]["row"]
    for row in rows:
        if row["MMEAL_SC_CODE"] == LUNCH_CODE:
            return row
    return {}
```

| 줄 | 설명 |
| --- | --- |
| 91~92 | 급식이 없는 날 응답이면 빈 딕셔너리를 돌려줍니다. (2-5, 2-11) |
| 93 | 겹친 응답에서 급식 목록(`row`)을 꺼냅니다. (step02 2-6) |
| 94~96 | 목록을 돌며 식사코드가 중식인 것을 찾으면 바로 돌려줍니다. |
| 97 | 끝까지 돌았는데 중식이 없으면(석식만 있는 날) 빈 딕셔너리를 돌려줍니다. |

### 100~104줄: `join_dish_names` — 메뉴 이름만 이어 붙이기

```python
def join_dish_names(dishes: list[dict]) -> str:
    names = []
    for dish in dishes:
        names.append(dish["name"])
    return DISH_SEPARATOR.join(names)
```

메뉴 딕셔너리들에서 이름만 모아 ` / `로 이어 붙입니다. 알레르기 번호는 메시지에 넣지 않습니다. (2-4, 2-6)

### 107~116줄: `format_lunch_message` — 메시지 완성

```python
def format_lunch_message(meal_result: dict, meal_date: str) -> str:
    # 메시지 모양 (CLAUDE.md 예시):
    # [11월 5일(목) 중식]
    # 쌀밥 / 된장찌개 / 제육볶음 / 배추김치 / 요구르트
    title = f"[{format_date(meal_date)} 중식]"
    lunch_row = find_lunch_row(meal_result)
    if lunch_row == {}:
        return title + "\n" + NO_MEAL_TEXT
    dishes = parse_dishes(lunch_row["DDISH_NM"])
    return title + "\n" + join_dish_names(dishes)
```

| 줄 | 설명 |
| --- | --- |
| 111 | 제목 줄 `[11월 5일(목) 중식]`을 만듭니다. |
| 112 | 응답에서 중식을 찾습니다. |
| 113~114 | 중식이 없으면 제목 아래에 "오늘은 급식이 없습니다."를 붙여 돌려줍니다. |
| 115 | 중식 메뉴 글자를 메뉴 목록으로 바꿉니다. |
| 116 | 제목, 줄바꿈, 메뉴 이름들을 이어 메시지를 완성합니다. (2-10) |

다른 함수들을 차례로 불러 조립하는 함수입니다. 각 함수가 한 가지 일만 하니, 어디서 문제가 생겼는지 찾기 쉽습니다.

### 그 밖의 파일

- **`tests/test_formatter.py`**: 테스트 20개입니다. 줄 단위 모양은 2-12, 2-13과 같습니다.
  - 테스트 데이터 `MEAL_RESULT_WITH_LUNCH` 등은 실제 NEIS 응답을 테스트에 필요한 키만 남기고 줄인 딕셔너리입니다.
  - CLAUDE.md 예시 모양(`된장찌개(5.6.9.)`)과 실제 모양(`부대찌개 (1.2.5.6)`)을 모두 확인합니다.
- **`show_lunch_message.py`**: step02의 `show_meal_json.py`와 같은 모양입니다. 다른 점은 마지막 줄에서 `format_lunch_message`로 메시지를 만들어 출력한다는 것입니다.
- **`pytest.ini`**: 2-14.
- **`requirements.txt`**: `pytest==9.2.0`을 추가했습니다.

---

## 4. 사용한 라이브러리

| 라이브러리 | 종류 | 이번에 쓴 것 | 뜻 |
| --- | --- | --- | --- |
| datetime | 표준 라이브러리 | `datetime.strptime(글자, "%Y%m%d")` | 날짜 글자를 날짜 객체로 바꿉니다. |
| datetime | | `날짜.month`, `날짜.day` | 월, 일 숫자(속성)입니다. |
| datetime | | `날짜.weekday()` | 요일 번호입니다. 월요일 0 ~ 일요일 6. |
| pytest 9.2.0 | 따로 설치 (pip) | `python -m pytest`, `pytest` | `test_`로 시작하는 파일과 함수를 찾아 실행합니다. `-v`를 붙이면 자세히 보여 줍니다. |
| (문자열 메서드) | 기본 기능 | `split`, `strip`, `endswith`, `rfind`, `isdigit`, `join` | 2-1, 2-2, 2-6 |
| (리스트 메서드) | 기본 기능 | `append` | 2-4 |

---

## 5. 용어 정리

| 용어 | 쉬운 뜻 | 예시 |
| --- | --- | --- |
| 구분자 | 나누거나 이어 붙일 때 사이에 오는 글자 | `<br/>`, `" / "` |
| 슬라이싱 | `[시작:끝]`으로 일부를 잘라 내는 것. 끝 칸은 빠진다 | `dish[:4]` |
| 음수 번호 | 뒤에서부터 세는 번호. `-1`이 마지막 | `dish[-1]` |
| 속성 | 객체에 딸린 값. 괄호 없이 쓴다 | `meal_day.month` |
| 형식 코드 | 날짜 글자의 모양을 알려 주는 약속 | `%Y%m%d` |
| f-문자열 | `{ }` 자리에 값이 들어가는 문자열 | `f"{month}월"` |
| 줄바꿈 문자 | 줄을 바꾸라는 뜻의 글자 | `\n` |
| 테스트 | 함수의 기대 결과를 코드로 적어 자동으로 확인하는 것 | `test_format_date_sunday` |
| `assert` | 조건이 거짓이면 `AssertionError`를 내는 문법 | `assert 1 + 1 == 2` |
| 설정 파일 | 프로그램이 실행될 때 읽는 설정을 적은 파일 | `pytest.ini` |
| `AttributeError` | 객체에 그런 기능(메서드나 속성)이 없다는 오류 | `names.join(...)` |
| `ValueError` | 값이 기대한 모양이 아니라는 오류 | `strptime("2026-11-05", "%Y%m%d")` |
| `AssertionError` | `assert` 조건이 거짓이라는 오류 | 테스트 실패 |

---

## 6. 확인 문제

### 문제 1. 코드 읽기: 이 코드를 실행하면 화면에 무엇이 나올까요?

`app/formatter.py`의 함수를 그대로 쓴다고 가정합니다.

```python
print(remove_allergy_numbers("우유(급식용) (2)"))
print(extract_allergy_numbers("우유(급식용) (2)"))
print(remove_allergy_numbers("우유(급식용)"))
```

<details><summary>정답</summary>

```
우유(급식용)
['2']
우유(급식용)
```

- 첫 줄: 마지막 괄호 `(2)` 안이 숫자라서 알레르기 번호입니다. 그 앞까지 잘라 빈칸을 지웁니다. `(급식용)`은 남습니다.
- 둘째 줄: 알레르기 번호 `2`를 문자열 리스트로 돌려줍니다.
- 셋째 줄: 마지막 괄호 `(급식용)` 안이 숫자가 아니라서 메뉴 이름의 일부로 봅니다. 그대로 돌려줍니다.

`rfind`로 **마지막** 괄호를 찾기 때문에 이렇게 구별할 수 있습니다. (2-2)

</details>

### 문제 2. 빈칸 채우기

`format_date("20261108")`이 `"11월 8일(일)"`을 돌려주도록 빈칸을 채우세요.

```python
def format_date(yyyymmdd: str) -> str:
    meal_day = datetime.strptime(yyyymmdd, "______")
    weekday_name = WEEKDAY_NAMES[meal_day.______()]
    return _"{meal_day.month}월 {meal_day.day}일({weekday_name})"
```

<details><summary>정답</summary>

```python
def format_date(yyyymmdd: str) -> str:
    meal_day = datetime.strptime(yyyymmdd, "%Y%m%d")
    weekday_name = WEEKDAY_NAMES[meal_day.weekday()]
    return f"{meal_day.month}월 {meal_day.day}일({weekday_name})"
```

- `%Y%m%d`: 네 자리 연도, 두 자리 월, 두 자리 일이 붙어 있는 모양입니다.
- `weekday`: 요일 번호(월 0 ~ 일 6)를 돌려주는 메서드입니다. 일요일이라 6이고, `WEEKDAY_NAMES[6]`은 `"일"`입니다.
- `f`: 빠뜨리면 `{meal_day.month}`가 글자 그대로 나옵니다. (2-9)

</details>

### 문제 3. 작은 수정: 테스트가 실행되게 고치세요

`python -m pytest`를 실행했더니 `collected 0 items`, `no tests ran`이 나왔습니다.

```python
# tests/test_date.py
from app.formatter import format_date


def check_format_date_monday():
    assert format_date("20261102") == "11월 2일(월)"
```

<details><summary>정답</summary>

```python
def test_format_date_monday():
    assert format_date("20261102") == "11월 2일(월)"
```

pytest는 이름이 `test_`로 시작하는 함수만 테스트로 찾습니다. (2-12)
파일 이름 `test_date.py`는 규칙에 맞습니다. 함수 이름만 바꾸면 됩니다.

2026년 11월 2일은 월요일이라서, 고친 테스트는 통과합니다.

</details>

---

## 이번 단계 핵심 정리

1. `split`으로 나누고, `strip`으로 다듬고, `[시작:끝]`으로 자른다. 끝 번호 칸은 빠진다.
2. 알레르기 번호는 마지막 괄호 안이 숫자와 점으로만 되어 있을 때만 지우고, 리스트로 따로 보관한다.
3. `datetime.strptime`으로 날짜를 만들고, `weekday()`(월 0 ~ 일 6)와 f-문자열로 `11월 5일(목)`을 만든다.
4. 함수가 찾지 못했을 때는 타입에 맞는 "없음"(`-1`, `[]`, `{}`)을 돌려준다.
5. 테스트는 `test_`로 시작하는 함수에 `assert`로 쓰고, `python -m pytest`로 실행한다.
