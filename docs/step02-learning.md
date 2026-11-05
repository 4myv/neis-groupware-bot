# 2단계 학습 정리: 함수, 딕셔너리, 그리고 API 호출

## 이 문서를 다 읽으면 할 수 있게 되는 것

1. `def`로 함수를 만들고, 값을 넘겨받아 결과를 돌려주게 할 수 있다.
2. 딕셔너리와 리스트로 된 JSON 응답에서 원하는 값을 찾아 꺼낼 수 있다.
3. `requests`로 NEIS API를 호출하는 `app/neis.py`를 한 줄씩 설명할 수 있다.

## 읽기 전에

- 코드 예시는 모두 실제로 실행한 결과를 붙였습니다.
- 오류 메시지의 긴 파일 경로는 `예시.py`처럼 짧게 줄여 적었습니다.
- 예시에 나오는 학교는 공개된 예시 학교(서울고등학교)입니다.
- 1단계에서 설명한 것은 "step01 참고"라고만 적었습니다. ([1단계 학습 정리](step01-learning.md))

---

## 1. 이번 단계에서 새로 나온 것

**Python 문법**

1. 함수 만들기: `def`, 매개변수, `return`
2. 함수의 타입 힌트: `-> 반환 타입`
3. 딕셔너리
4. `for` 반복문
5. 리스트
6. 겹쳐 있는 딕셔너리·리스트에서 값 꺼내기
7. 문자열 이어 붙이기 `+`
8. 키워드 인자: `이름=값`
9. `input()`: 키보드로 입력받기
10. 한 줄에 여러 이름 가져오기: `from ... import A, B`
11. 객체와 메서드: `값.기능()`

**인터넷과 데이터**

12. HTTP 요청과 `requests` 라이브러리
13. JSON과 `json` 모듈

**1단계에서 이미 설명한 것 (step01 참고)**

`print`, 주석 `#`, 변수와 `=`, 타입 힌트 기초(`str`, `int`), `if`/`else`와 들여쓰기, `==`, `import`, 패키지, `None`, 대문자 상수 이름, 가상환경, pip, requirements.txt, .env

---

## 2. 하나씩 설명

### 2-1. 함수 만들기: `def`, 매개변수, `return`

**설명**

함수는 이름을 부르면 정해진 일을 하는 코드 묶음입니다. (step01의 `print`도 함수입니다.)
이번에는 함수를 **직접 만듭니다.**

`def 함수이름(매개변수):` 모양으로 만듭니다.
매개변수는 함수를 부를 때 넘겨받는 값에 붙이는 이름입니다.

함수 안의 코드는 4칸 들여씁니다. (step01의 `if` 블록과 같습니다.)

`return 값`은 "이 값을 결과로 돌려주고 함수를 끝내라"는 뜻입니다.
돌려준 값을 반환값이라고 합니다.

**비유**

자판기와 같습니다. 돈과 버튼(매개변수)을 넣으면 음료(반환값)가 나옵니다.
자판기를 만들어 두기만 하면 아무 일도 일어나지 않습니다. 버튼을 눌러야(함수를 불러야) 움직입니다.

**작은 예시**

```python
def make_school_name(area: str) -> str:
    return area + "고등학교"


print(make_school_name("서울"))
print(make_school_name("부산"))
```

결과:

```
서울고등학교
부산고등학교
```

- 1~2줄은 함수를 **만들기만** 합니다. 이때는 아무것도 출력되지 않습니다.
- 5줄에서 `make_school_name("서울")`로 함수를 **부릅니다.** `area`에 `"서울"`이 들어갑니다.
- 함수가 돌려준 `"서울고등학교"`를 `print`가 출력합니다.
- 함수 정의 뒤에 빈 줄 두 개를 두는 것은 Python의 관례입니다.

**이 프로젝트 코드** (`app/neis.py`)

```python
def fetch_schools(school_name: str) -> dict:
    # 학교 이름의 일부만 넣어도 여러 학교가 함께 나올 수 있다. (예: "서울고" → 9곳)
    search_conditions = {"SCHUL_NM": school_name}
    return call_neis_api("schoolInfo", search_conditions)
```

**Java 비교**

```java
static String makeSchoolName(String area) {
    return area + "고등학교";
}
```

| Java | Python |
| --- | --- |
| 반환 타입을 이름 앞에 쓴다 (`String makeSchoolName`) | 반환 타입을 `->` 뒤에 쓴다 (선택) |
| 메서드는 꼭 클래스 안에 있어야 한다 | 파일에 바로 함수를 만들 수 있다 |
| `{ }`로 몸통을 감싼다 | 콜론 `:`과 들여쓰기로 몸통을 표시한다 |

**자주 하는 실수: `return`을 빠뜨린다**

```python
def make_school_name(area: str) -> str:
    name = area + "고등학교"


print(make_school_name("서울"))
```

결과:

```
None
```

`return`이 없으면 함수는 `None`(값 없음, step01 참고)을 돌려줍니다.
오류가 나지 않아서 더 찾기 어려운 실수입니다.

---

### 2-2. 함수의 타입 힌트: `-> 반환 타입`

**설명**

1단계에서 변수에 붙였던 타입 힌트를 함수에도 붙입니다. (step01 2-9 참고)

- `area: str`: "매개변수 `area`에는 문자열이 들어온다"
- `-> str`: "이 함수는 문자열을 돌려준다"

이번 단계에서 새로 나온 타입은 `dict`(딕셔너리, 2-3)입니다.

**이 프로젝트 코드**

```python
def fetch_meals(office_code: str, school_code: str, meal_date: str) -> dict:
```

매개변수 세 개는 모두 문자열입니다. 반환값은 딕셔너리입니다.

**Java 비교**

```java
static Map<String, Object> fetchMeals(String officeCode, String schoolCode, String mealDate)
```

**자주 하는 실수: 힌트가 틀린 값을 막아 준다고 생각한다**

```python
def double(count: int) -> int:
    return count * 2


print(double(3))
print(double("밥"))
```

결과:

```
6
밥밥
```

`int`라고 적었는데 문자열을 넣어도 실행됩니다.
문자열에 `* 2`를 하면 두 번 이어 붙인 문자열이 됩니다. 1단계와 마찬가지로, 타입 힌트는 검사하지 않는 약속입니다.

---

### 2-3. 딕셔너리

**설명**

딕셔너리는 **이름(키)과 값을 짝지어** 담는 상자입니다.
`{키: 값, 키: 값}` 모양으로 만듭니다.

값을 꺼낼 때는 `딕셔너리[키]`로 씁니다.

같은 모양으로 `딕셔너리[키] = 값`이라고 쓰면 값을 넣습니다.
없던 키면 새로 생기고, 있던 키면 값이 바뀝니다.

**비유**

국어사전과 같습니다. 단어(키)를 알면 뜻(값)을 바로 찾을 수 있습니다.

**작은 예시**

```python
school = {"SCHUL_NM": "서울고등학교", "SD_SCHUL_CODE": "7010083"}
print(school["SCHUL_NM"])
school["ATPT_OFCDC_SC_CODE"] = "B10"
print(school)
```

결과:

```
서울고등학교
{'SCHUL_NM': '서울고등학교', 'SD_SCHUL_CODE': '7010083', 'ATPT_OFCDC_SC_CODE': 'B10'}
```

딕셔너리를 통째로 `print`하면 문자열이 작은따옴표 `'...'`로 표시됩니다.

**이 프로젝트 코드** (`app/neis.py`)

```python
params = {
    "KEY": NEIS_API_KEY,
    "Type": "json",
    "pIndex": 1,
    "pSize": 100,
}
```

키와 값이 많을 때는 이렇게 한 줄에 하나씩 적어도 됩니다. 마지막 줄 끝의 쉼표는 있어도 괜찮습니다.

**Java 비교**

```java
Map<String, Object> school = new HashMap<>();
school.put("SCHUL_NM", "서울고등학교");
school.get("SCHUL_NM");
```

| Java `Map` | Python 딕셔너리 |
| --- | --- |
| `map.get(키)` | `딕셔너리[키]` |
| `map.put(키, 값)` | `딕셔너리[키] = 값` |
| 없는 키를 `get`하면 `null` | 없는 키를 꺼내면 **오류** (아래 실수) |

**자주 하는 실수: 키의 대소문자를 틀린다**

```python
school = {"SCHUL_NM": "서울고등학교"}
print(school["schul_nm"])
```

결과:

```
Traceback (most recent call last):
  File "예시.py", line 2, in <module>
    print(school["schul_nm"])
          ~~~~~~^^^^^^^^^^^^
KeyError: 'schul_nm'
```

`KeyError`는 "그런 키가 없다"는 오류입니다. 키는 대문자와 소문자를 구별합니다.
NEIS 응답의 키는 모두 대문자입니다.

---

### 2-4. `for` 반복문

**설명**

`for 이름 in 묶음:`은 묶음 안의 것을 하나씩 꺼내 같은 일을 반복합니다.
반복할 코드는 4칸 들여씁니다.

딕셔너리를 `for`로 돌면 **키**가 하나씩 나옵니다.
값이 필요하면 꺼낸 키로 `딕셔너리[키]`를 씁니다.

**작은 예시**

```python
conditions = {"SCHUL_NM": "서울고등학교", "Type": "json"}
for name in conditions:
    print(name, "→", conditions[name])
```

결과:

```
SCHUL_NM → 서울고등학교
Type → json
```

**이 프로젝트 코드** (`app/neis.py`)

```python
for name in search_conditions:
    params[name] = search_conditions[name]
```

`search_conditions`의 키를 하나씩 꺼내, 같은 키와 값을 `params`에 넣습니다.
결과적으로 `search_conditions`의 내용이 모두 `params`에 덧붙습니다.

**Java 비교**

```java
for (String name : searchConditions.keySet()) {
    params.put(name, searchConditions.get(name));
}
```

Java의 향상된 for문(`for (... : ...)`)과 같은 모양입니다.

**자주 하는 실수: 값이 나올 거라고 생각한다**

```python
conditions = {"SCHUL_NM": "서울고등학교", "Type": "json"}
for name in conditions:
    print(name)
```

결과:

```
SCHUL_NM
Type
```

값(`서울고등학교`, `json`)이 아니라 키만 나옵니다. 값은 `conditions[name]`으로 꺼내야 합니다.

---

### 2-5. 리스트

**설명**

리스트는 값을 **순서대로** 담는 상자입니다. `[값, 값, 값]` 모양입니다.

꺼낼 때는 `리스트[번호]`로 씁니다. 번호는 **0부터** 셉니다.
이 번호를 인덱스라고 부릅니다.

이번 단계 코드에서 리스트를 직접 만들지는 않습니다.
하지만 NEIS 응답 안에 리스트가 들어 있어서, 응답을 읽으려면 알아야 합니다.

**비유**

번호표가 붙은 사물함입니다. 첫 번째 칸의 번호가 1이 아니라 0입니다.

**작은 예시**

```python
meals = ["중식", "석식"]
print(meals[0])
print(meals[1])
```

결과:

```
중식
석식
```

**NEIS 응답에서** (`row`의 값이 리스트입니다)

```
"row": [
  { ... 중식 정보 ... },
  { ... 석식 정보 ... }
]
```

**Java 비교**

```java
List<String> meals = List.of("중식", "석식");
meals.get(0);
```

Java의 `List`나 배열처럼 0부터 셉니다.

**자주 하는 실수: 없는 번호를 꺼낸다**

```python
meals = ["중식", "석식"]
print(meals[2])
```

결과:

```
Traceback (most recent call last):
  File "예시.py", line 2, in <module>
    print(meals[2])
          ~~~~~^^^
IndexError: list index out of range
```

두 개짜리 리스트의 번호는 0과 1뿐입니다. `IndexError`는 "번호가 범위를 벗어났다"는 오류입니다.

---

### 2-6. 겹쳐 있는 딕셔너리·리스트에서 값 꺼내기

**설명**

NEIS 응답은 딕셔너리 안에 리스트가 있고, 그 리스트 안에 또 딕셔너리가 있는 모양입니다.
바깥에서 안쪽으로 한 겹씩 꺼내 들어가면 됩니다.

**비유**

큰 상자 → 그 안의 서랍 → 서랍 안의 봉투 → 봉투 안의 쪽지 순서로 여는 것과 같습니다.

**작은 예시** (실제 응답을 줄인 모양)

```python
result = {"mealServiceDietInfo": [{"head": []}, {"row": [{"MMEAL_SC_NM": "중식", "DDISH_NM": "흑미밥"}]}]}

info = result["mealServiceDietInfo"]
second = info[1]
rows = second["row"]
first_meal = rows[0]
print(first_meal["DDISH_NM"])
print(result["mealServiceDietInfo"][1]["row"][0]["DDISH_NM"])
```

결과:

```
흑미밥
흑미밥
```

| 줄 | 꺼낸 것 | 종류 |
| --- | --- | --- |
| `info = result["mealServiceDietInfo"]` | `[{"head": ...}, {"row": ...}]` | 리스트 |
| `second = info[1]` | `{"row": [...]}` (두 번째 칸) | 딕셔너리 |
| `rows = second["row"]` | `[{"MMEAL_SC_NM": "중식", ...}]` | 리스트 |
| `first_meal = rows[0]` | `{"MMEAL_SC_NM": "중식", "DDISH_NM": "흑미밥"}` | 딕셔너리 |
| `first_meal["DDISH_NM"]` | `"흑미밥"` | 문자열 |

마지막 줄처럼 한 줄로 이어 쓸 수도 있습니다. 처음에는 한 겹씩 나눠 쓰는 편이 읽기 쉽습니다.

**이 프로젝트에서**

이번 단계 코드는 응답을 그대로 출력만 합니다. 이렇게 값을 꺼내는 일은 3단계(데이터 변환)에서 합니다.

**Java 비교** (Jackson 라이브러리의 `JsonNode`)

```java
root.get("mealServiceDietInfo").get(1).get("row").get(0).get("DDISH_NM").asText();
```

**자주 하는 실수: 급식이 없는 날의 응답에도 같은 길로 들어간다**

급식이 없는 날(일요일)의 실제 응답은 모양이 완전히 다릅니다.

```
{
  "RESULT": {
    "CODE": "INFO-200",
    "MESSAGE": "해당하는 데이터가 없습니다."
  }
}
```

`mealServiceDietInfo` 키가 아예 없습니다.
그래서 `result["mealServiceDietInfo"]`를 꺼내면 2-3의 `KeyError`가 납니다.
이 경우를 나눠 처리하는 일은 3단계에서 합니다.

---

### 2-7. 문자열 이어 붙이기 `+`

**설명**

문자열끼리 `+`를 쓰면 하나로 이어 붙습니다.

**작은 예시**

```python
base = "https://open.neis.go.kr/hub/"
print(base + "schoolInfo")
```

결과:

```
https://open.neis.go.kr/hub/schoolInfo
```

**이 프로젝트 코드**

```python
NEIS_BASE_URL + service_name
```

공통 앞부분 `https://open.neis.go.kr/hub/` 뒤에 서비스 이름(`schoolInfo`, `mealServiceDietInfo`)을 붙여 요청 주소를 만듭니다.

**Java 비교**

```java
String url = NEIS_BASE_URL + serviceName;
```

모양은 같습니다. 차이는 아래 실수에서 볼 수 있습니다.

**자주 하는 실수: 문자열에 숫자를 바로 이어 붙인다**

```python
print("pSize=" + 100)
```

결과:

```
Traceback (most recent call last):
  File "예시.py", line 1, in <module>
    print("pSize=" + 100)
          ~~~~~~~~~^~~~~
TypeError: can only concatenate str (not "int") to str
```

Java는 `"pSize=" + 100`을 `"pSize=100"`으로 자동으로 바꿔 줍니다.
Python은 바꿔 주지 않고 `TypeError`를 냅니다. 숫자를 문자열로 바꾸는 방법은 필요한 단계에서 배웁니다.

---

### 2-8. 키워드 인자: `이름=값`

**설명**

함수를 부를 때 값을 `이름=값` 모양으로 넘길 수 있습니다. 이것을 키워드 인자라고 합니다.
어떤 값이 무슨 뜻인지 이름으로 알 수 있어서 읽기 쉽습니다.

**작은 예시**

```python
import json

school = {"SCHUL_NM": "서울고등학교", "FOND_SC_NM": "공립"}
print(json.dumps(school, ensure_ascii=False, indent=2))
```

결과:

```
{
  "SCHUL_NM": "서울고등학교",
  "FOND_SC_NM": "공립"
}
```

`school`은 순서로 넘긴 값입니다. `ensure_ascii=False`와 `indent=2`는 이름으로 넘긴 값입니다. (뜻은 2-13)

**이 프로젝트 코드** (`app/neis.py`)

```python
response = requests.get(
    NEIS_BASE_URL + service_name,
    params=params,
    timeout=REQUEST_TIMEOUT_SECONDS,
)
```

- 첫 번째 값(주소)은 순서로 넘깁니다.
- `params=`와 `timeout=`은 이름으로 넘깁니다.
- 괄호 안이 길면 이렇게 여러 줄로 나눠 써도 됩니다.

`params=params`가 헷갈릴 수 있습니다. 왼쪽 `params`는 `requests.get`이 정해 둔 **인자 이름**이고, 오른쪽 `params`는 우리가 만든 **변수**입니다.

**Java 비교**

Java에는 키워드 인자가 없습니다. 모든 인자를 순서대로만 넘깁니다.

```java
mapper.writerWithDefaultPrettyPrinter().writeValueAsString(school);
```

옵션이 많을 때 Java는 위처럼 메서드를 이어 붙이거나 빌더(builder)를 쓰는 경우가 많습니다.

**자주 하는 실수: 인자 이름에 오타를 낸다**

```python
import json

print(json.dumps({"SCHUL_NM": "서울고등학교"}, ensure_ascii=False, indnet=2))
```

결과 (마지막 줄):

```
TypeError: JSONEncoder.__init__() got an unexpected keyword argument 'indnet'. Did you mean 'indent'?
```

"모르는 키워드 인자 `indnet`이 들어왔다"는 뜻입니다. `Did you mean 'indent'?`가 바른 이름을 알려 줍니다.

---

### 2-9. `input()`: 키보드로 입력받기

**설명**

`input("안내 문구")`는 안내 문구를 화면에 보여 주고, 사용자가 키보드로 입력하고 Enter를 칠 때까지 기다립니다.
입력한 내용은 **문자열**로 돌려줍니다.

**작은 예시**

```python
school_name = input("학교 이름을 입력하세요: ")
print("입력한 학교:", school_name)
```

실행 화면 (`서울고등학교`는 키보드로 입력한 부분):

```
학교 이름을 입력하세요: 서울고등학교
입력한 학교: 서울고등학교
```

**이 프로젝트 코드**

```python
school_name = input("학교 이름을 입력하세요: ")          # find_school.py
meal_date = input("날짜를 YYYYMMDD 형식으로 입력하세요 (예: 20261105): ")   # show_meal_json.py
```

**Java 비교**

```java
Scanner scanner = new Scanner(System.in);
System.out.print("학교 이름을 입력하세요: ");
String schoolName = scanner.nextLine();
```

**자주 하는 실수: 숫자를 입력하면 숫자로 받는다고 생각한다**

```python
year = input("연도를 입력하세요: ")
print(year + 1)
```

`2026`을 입력했을 때의 결과:

```
Traceback (most recent call last):
  File "예시.py", line 2, in <module>
    print(year + 1)
          ~~~~~^~~
TypeError: can only concatenate str (not "int") to str
```

`2026`을 입력해도 `year`에는 숫자 2026이 아니라 문자열 `"2026"`이 들어 있습니다.
그래서 2-7과 같은 오류가 납니다.

---

### 2-10. 한 줄에 여러 이름 가져오기: `from ... import A, B`

**설명**

같은 모듈에서 여러 개를 가져올 때는 쉼표로 이어 한 줄에 씁니다. (`import` 자체는 step01 참고)

**작은 예시** (`math`는 계산 기능을 모은 표준 라이브러리입니다)

```python
from math import ceil, floor

print(floor(625.4))
print(ceil(625.4))
```

결과:

```
625
626
```

`floor`는 내림, `ceil`은 올림입니다. 이 예시에만 쓰고 프로젝트에서는 쓰지 않습니다.

**이 프로젝트 코드** (`show_meal_json.py`)

```python
from app.config import NEIS_OFFICE_CODE, NEIS_SCHOOL_CODE
```

**Java 비교**

```java
import static app.Config.NEIS_OFFICE_CODE;
import static app.Config.NEIS_SCHOOL_CODE;
```

Java는 한 줄에 하나씩 씁니다.

**자주 하는 실수: 쉼표를 빠뜨린다**

```python
from math import ceil floor
```

결과:

```
  File "예시.py", line 1
    from math import ceil floor
                          ^^^^^
SyntaxError: invalid syntax
```

---

### 2-11. 객체와 메서드: `값.기능()`

**설명**

Python에서는 모든 값이 **객체**입니다. 객체는 데이터와, 그 데이터로 할 수 있는 기능을 함께 가진 것입니다.

객체에 딸린 기능을 **메서드**라고 합니다. `값.메서드이름()` 모양으로 부릅니다.

**작은 예시** (문자열의 `replace` 메서드)

```python
name = "서울고등학교"
print(name.replace("고등학교", "고"))
```

결과:

```
서울고
```

문자열 객체 `name`에 딸린 `replace` 기능을 불렀습니다. "고등학교"를 "고"로 바꾼 새 문자열을 돌려줍니다.

**이 프로젝트 코드** (`app/neis.py`)

```python
return response.json()
```

`requests.get`이 돌려준 응답 객체 `response`의 `json` 메서드를 부릅니다.
응답 내용(JSON 글자)을 딕셔너리로 바꿔 돌려줍니다.

**Java 비교**

Java와 같습니다.

```java
name.replace("고등학교", "고");
response.getBody();
```

**자주 하는 실수: 괄호 `()`를 빠뜨린다**

```python
print(response.json)
```

결과 (2-12의 예시에서 실행):

```
<bound method Response.json of <Response [200]>>
```

괄호가 없으면 메서드를 **부르지 않고**, 메서드 자체를 가리킵니다. 그래서 딕셔너리 대신 이상한 글자가 나옵니다.

---

### 2-12. HTTP 요청과 `requests` 라이브러리

**설명**

HTTP는 인터넷에서 프로그램끼리 요청과 응답을 주고받는 약속입니다. 웹 브라우저도 HTTP로 웹 페이지를 받아 옵니다.

GET 요청은 "이 주소의 정보를 주세요"라는 요청입니다.
조건은 주소 뒤에 `?이름=값&이름=값` 모양으로 붙입니다. 이 부분을 쿼리 문자열이라고 합니다.

`requests`는 HTTP 요청을 쉽게 보내게 해 주는 외부 라이브러리입니다. pip로 설치했습니다. (step01 pip 참고)

**작은 예시** (인증키 없이 보낸 요청)

```python
import requests

response = requests.get(
    "https://open.neis.go.kr/hub/schoolInfo",
    params={"Type": "json", "SCHUL_NM": "서울고등학교"},
    timeout=10,
)
print(response.status_code)
print(response.url)
```

결과:

```
200
https://open.neis.go.kr/hub/schoolInfo?Type=json&SCHUL_NM=%EC%84%9C%EC%9A%B8%EA%B3%A0%EB%93%B1%ED%95%99%EA%B5%90
```

- `status_code`는 상태 코드(서버가 붙여 주는 결과 번호)입니다. `200`은 "요청을 잘 받았다"는 뜻입니다.
- `params`에 넣은 딕셔너리가 `?Type=json&SCHUL_NM=...` 쿼리 문자열로 바뀌었습니다.
- 한글은 주소에 그대로 넣을 수 없습니다. 그래서 `requests`가 `%EC%84%9C...` 같은 글자로 바꿔 줍니다. 이것을 퍼센트 인코딩이라고 합니다.

> 실제 프로그램의 주소에는 `KEY=인증키`도 붙습니다.
> 그래서 `response.url`을 화면이나 로그에 그대로 출력하면 인증키가 드러납니다. 이 프로젝트 코드는 주소를 출력하지 않습니다.

`timeout=10`은 "10초 안에 답이 없으면 기다리지 마라"라는 뜻입니다. 정하지 않으면 서버가 답하지 않을 때 프로그램이 끝없이 기다립니다.

**이 프로젝트 코드** (`app/neis.py`)

```python
response = requests.get(
    NEIS_BASE_URL + service_name,
    params=params,
    timeout=REQUEST_TIMEOUT_SECONDS,
)
return response.json()
```

**Java 비교** (Spring의 `RestTemplate`)

```java
String url = UriComponentsBuilder.fromHttpUrl("https://open.neis.go.kr/hub/schoolInfo")
        .queryParam("Type", "json")
        .queryParam("SCHUL_NM", "서울고등학교")
        .toUriString();
Map<String, Object> result = restTemplate.getForObject(url, Map.class);
```

**자주 하는 실수: `Type=json`을 빠뜨린다**

NEIS 공식 명세에서 `Type`의 기본값은 `xml`입니다. 빠뜨리면 XML로 답이 옵니다.

```python
import requests

response = requests.get(
    "https://open.neis.go.kr/hub/schoolInfo",
    params={"SCHUL_NM": "서울고등학교"},
    timeout=10,
)
print(response.headers["Content-Type"])
data = response.json()
```

결과 (첫 줄과 마지막 줄):

```
application/xml;charset=UTF-8
...
requests.exceptions.JSONDecodeError: Expecting value: line 1 column 1 (char 0)
```

응답이 XML이라서 `.json()`이 JSON으로 읽지 못했습니다. 그래서 `app/neis.py`는 `"Type": "json"`을 항상 넣습니다.

---

### 2-13. JSON과 `json` 모듈

**설명**

JSON은 데이터를 글자로 주고받는 약속된 모양입니다. `{ }`, `[ ]`, `"키": 값`으로 이루어져 있습니다.
Python의 딕셔너리, 리스트와 모양이 거의 같습니다.

`response.json()`은 JSON 글자를 Python 값으로 바꿉니다. 바뀌는 모양은 아래와 같습니다.

| JSON | Python |
| --- | --- |
| `{ }` | 딕셔너리 |
| `[ ]` | 리스트 |
| `"글자"` | 문자열 |
| `1295.0` | 소수점 있는 숫자 (`float`) |
| `null` | `None` (step01 참고) |
| `true` / `false` | `True` / `False` |

**작은 예시 1: JSON 글자 → Python 값**

```python
import json

text = '{"SPCLY_PURPS_HS_ORD_NM": null, "MLSV_FGR": 1295.0}'
data = json.loads(text)
print(data["SPCLY_PURPS_HS_ORD_NM"])
print(data["MLSV_FGR"])
```

결과:

```
None
1295.0
```

`json.loads`는 `response.json()`이 안에서 하는 일과 같습니다. 프로젝트에서는 `response.json()`을 씁니다.

**작은 예시 2: Python 값 → 보기 좋은 JSON 글자** (2-8의 예시)

`json.dumps(값, ensure_ascii=False, indent=2)`는 반대로 Python 값을 JSON 글자로 바꿉니다.

- `indent=2`: 2칸씩 들여 써서 줄을 나눕니다. 사람이 읽기 좋아집니다.
- `ensure_ascii=False`: 한글을 글자 그대로 둡니다. (아래 실수 참고)

**이 프로젝트 코드** (`find_school.py`, `show_meal_json.py`)

```python
print(json.dumps(result, ensure_ascii=False, indent=2))
```

**Java 비교** (Jackson)

```java
ObjectMapper mapper = new ObjectMapper();
Map<String, Object> data = mapper.readValue(text, Map.class);                     // json.loads
String pretty = mapper.writerWithDefaultPrettyPrinter().writeValueAsString(data);  // json.dumps(..., indent=2)
```

**자주 하는 실수: `ensure_ascii=False`를 빠뜨린다**

```python
import json

print(json.dumps({"SCHUL_NM": "서울고등학교"}))
```

결과:

```
{"SCHUL_NM": "서울고등학교"}
```

틀린 값은 아닙니다. 한글을 `서` 같은 기호로 바꿔 적은 것입니다. 하지만 사람이 읽을 수 없습니다.

---

## 3. 코드 줄 단위 해설

### 3-1. `app/neis.py` (새 파일)

**1~5줄: 파일 설명 주석**

```python
# neis.py: NEIS 교육정보 개방 포털의 Open API를 호출하는 파일
#
# 정기 알림과 명령어 응답이 모두 이 파일을 거쳐 NEIS 데이터를 가져온다.
# 그래서 NEIS 주소나 요청 방식이 바뀌어도 이 파일만 고치면 된다.
# 요청 주소, 요청 인자 이름은 NEIS 포털의 Open API 명세에서 확인했다. (docs/step02-devlog.md 참고)
```

이 파일이 왜 따로 있는지 적었습니다. 나중에 정기 알림(스케줄러)과 명령어 응답(콜백 서버)이 같은 이 파일을 씁니다.

**7~9줄: 필요한 것 가져오기**

```python
import requests

from app.config import NEIS_API_KEY
```

| 줄 | 설명 |
| --- | --- |
| 7 | 따로 설치한 `requests` 라이브러리를 가져옵니다. (2-12) |
| 9 | `.env`에서 읽어 둔 인증키를 가져옵니다. (step01) |

**11~16줄: 바뀌지 않는 설정값**

```python
# 모든 NEIS Open API 주소의 공통 앞부분. 뒤에 서비스 이름을 붙여 쓴다.
NEIS_BASE_URL: str = "https://open.neis.go.kr/hub/"

# 응답을 기다릴 최대 시간(초).
# 정해 두지 않으면 서버가 답하지 않을 때 프로그램이 끝없이 기다린다.
REQUEST_TIMEOUT_SECONDS: int = 10
```

| 줄 | 설명 |
| --- | --- |
| 12 | 요청 주소의 공통 앞부분입니다. 대문자 이름은 "바꾸지 않을 값"이라는 약속입니다. (step01) |
| 16 | 응답을 기다릴 최대 시간 10초입니다. `int`는 정수라는 타입 힌트입니다. |

**19~38줄: 공통 호출 함수 `call_neis_api`**

```python
def call_neis_api(service_name: str, search_conditions: dict) -> dict:
    # 모든 NEIS API에 똑같이 붙는 기본 인자.
    # Type을 json으로 정하지 않으면 NEIS는 기본값인 xml로 답한다.
    params = {
        "KEY": NEIS_API_KEY,
        "Type": "json",
        "pIndex": 1,
        "pSize": 100,
    }

    # 서비스마다 다른 조건(학교 이름, 날짜 등)을 기본 인자에 덧붙인다.
    for name in search_conditions:
        params[name] = search_conditions[name]

    response = requests.get(
        NEIS_BASE_URL + service_name,
        params=params,
        timeout=REQUEST_TIMEOUT_SECONDS,
    )
    return response.json()
```

| 줄 | 설명 |
| --- | --- |
| 19 | 함수를 만듭니다. 서비스 이름(문자열)과 검색 조건(딕셔너리)을 받아, 딕셔너리를 돌려줍니다. (2-1, 2-2) |
| 22~27 | 모든 NEIS API에 공통으로 붙는 기본 인자를 딕셔너리로 만듭니다. (2-3) |
| 23 | `KEY`: 인증키입니다. |
| 24 | `Type`: 응답 형식입니다. `json`으로 받습니다. |
| 25 | `pIndex`: 몇 번째 페이지를 받을지입니다. 첫 페이지인 1입니다. |
| 26 | `pSize`: 한 페이지에 몇 건을 받을지입니다. 100건입니다. NEIS는 한 번에 최대 1,000건까지 줍니다. |
| 30~31 | 검색 조건의 키를 하나씩 꺼내 `params`에 같은 키와 값으로 넣습니다. (2-4) |
| 33~37 | 주소에 GET 요청을 보냅니다. 결과(응답 객체)를 `response`에 담습니다. (2-7, 2-8, 2-12) |
| 38 | 응답 JSON을 딕셔너리로 바꿔 돌려줍니다. (2-11, 2-13) |

**41~44줄: 학교 찾기 함수 `fetch_schools`**

```python
def fetch_schools(school_name: str) -> dict:
    # 학교 이름의 일부만 넣어도 여러 학교가 함께 나올 수 있다. (예: "서울고" → 9곳)
    search_conditions = {"SCHUL_NM": school_name}
    return call_neis_api("schoolInfo", search_conditions)
```

| 줄 | 설명 |
| --- | --- |
| 41 | 학교 이름을 받아 딕셔너리를 돌려주는 함수입니다. |
| 43 | NEIS 명세의 요청 인자 `SCHUL_NM`(학교명)에 받은 이름을 넣습니다. |
| 44 | 서비스 `schoolInfo`(학교기본정보)를 호출하고, 그 결과를 그대로 돌려줍니다. |

함수가 다른 함수를 부르고, 받은 결과를 다시 돌려주는 모양입니다.

**47~55줄: 급식 조회 함수 `fetch_meals`**

```python
def fetch_meals(office_code: str, school_code: str, meal_date: str) -> dict:
    # 중식·석식을 가리지 않고 그날의 급식을 모두 가져온다.
    # 중식만 고르는 일은 3단계(데이터 변환)에서 한다.
    search_conditions = {
        "ATPT_OFCDC_SC_CODE": office_code,
        "SD_SCHUL_CODE": school_code,
        "MLSV_YMD": meal_date,
    }
    return call_neis_api("mealServiceDietInfo", search_conditions)
```

| 줄 | 설명 |
| --- | --- |
| 47 | 시도교육청코드, 학교 코드, 날짜를 받는 함수입니다. |
| 50~54 | NEIS 명세의 요청 인자 이름으로 검색 조건을 만듭니다. `ATPT_OFCDC_SC_CODE`(시도교육청코드)와 `SD_SCHUL_CODE`(행정표준코드)는 필수, `MLSV_YMD`(급식일자)는 선택입니다. |
| 55 | 서비스 `mealServiceDietInfo`(급식식단정보)를 호출합니다. |

### 3-2. `app/config.py` (바뀐 부분)

```python
# 급식을 조회할 학교의 코드.
# 비밀값은 아니지만, 개발자가 다니는 학교를 저장소에 남기지 않으려고 코드 대신 .env에 둔다.
NEIS_OFFICE_CODE: str = os.getenv("NEIS_OFFICE_CODE", "")
NEIS_SCHOOL_CODE: str = os.getenv("NEIS_SCHOOL_CODE", "")
```

1단계의 `NEIS_API_KEY`와 같은 방법으로 두 값을 읽습니다. (step01 3-2 참고)

### 3-3. `find_school.py` (새 파일)

```python
import json

from app.neis import fetch_schools

school_name = input("학교 이름을 입력하세요: ")
result = fetch_schools(school_name)

# NEIS가 돌려준 응답을 손대지 않고 그대로 보여 준다.
# ensure_ascii=False는 한글을 서 같은 기호 대신 글자 그대로 보여 주려고 넣는다.
print(json.dumps(result, ensure_ascii=False, indent=2))
```

| 줄 | 설명 |
| --- | --- |
| `import json` | 표준 라이브러리 `json`을 가져옵니다. |
| `from app.neis import fetch_schools` | 우리가 만든 `app/neis.py`에서 `fetch_schools` 함수를 가져옵니다. |
| `school_name = input(...)` | 키보드로 학교 이름을 입력받습니다. (2-9) |
| `result = fetch_schools(school_name)` | NEIS에 학교를 찾아 달라고 요청하고, 결과 딕셔너리를 받습니다. |
| `print(json.dumps(...))` | 결과를 보기 좋은 JSON 글자로 바꿔 출력합니다. (2-13) |

### 3-4. `show_meal_json.py` (새 파일)

```python
import json

from app.config import NEIS_OFFICE_CODE, NEIS_SCHOOL_CODE
from app.neis import fetch_meals

meal_date = input("날짜를 YYYYMMDD 형식으로 입력하세요 (예: 20261105): ")
result = fetch_meals(NEIS_OFFICE_CODE, NEIS_SCHOOL_CODE, meal_date)

# 3단계에서 이 응답을 보기 좋은 메시지로 바꾼다. 지금은 원본의 모양을 그대로 확인한다.
print(json.dumps(result, ensure_ascii=False, indent=2))
```

`find_school.py`와 같은 모양입니다. 다른 점은 두 가지입니다.

- `.env`의 학교 코드 두 개를 한 줄로 가져옵니다. (2-10)
- 입력받은 날짜와 학교 코드로 `fetch_meals`를 부릅니다.

### 3-5. 설정 파일

**`requirements.txt`**에 한 줄을 추가했습니다.

```
requests==2.34.2
```

설치하면 `requests`가 쓰는 라이브러리 4개(certifi, charset-normalizer, idna, urllib3)도 함께 설치됩니다.

**`.env.example`**에 두 항목을 추가했습니다.

```
NEIS_OFFICE_CODE=
NEIS_SCHOOL_CODE=
```

---

## 4. 사용한 라이브러리

| 라이브러리 | 종류 | 이번에 쓴 것 | 뜻 |
| --- | --- | --- | --- |
| requests 2.34.2 | 따로 설치 (pip) | `requests.get(주소, params=딕셔너리, timeout=초)` | GET 요청을 보내고 응답 객체를 돌려줍니다. `params`는 쿼리 문자열로 바뀝니다. |
| requests | | `응답.json()` | 응답 JSON을 딕셔너리로 바꿔 돌려줍니다. |
| requests | (예시에서만) | `응답.status_code`, `응답.url` | 상태 코드와 실제로 요청한 주소입니다. |
| json | 표준 라이브러리 | `json.dumps(값, ensure_ascii=False, indent=2)` | Python 값을 보기 좋은 JSON 글자로 바꿉니다. |
| json | (예시에서만) | `json.loads(글자)` | JSON 글자를 Python 값으로 바꿉니다. |
| (기본 기능) | 내장 함수 | `input(안내 문구)` | 키보드 입력을 문자열로 돌려줍니다. 내장 함수는 `import` 없이 쓸 수 있는 함수입니다. |
| math | 표준 라이브러리 (예시에서만) | `floor`, `ceil` | 내림, 올림입니다. |

---

## 5. 용어 정리

| 용어 | 쉬운 뜻 | 예시 |
| --- | --- | --- |
| 함수 정의 | `def`로 함수를 새로 만드는 것 | `def fetch_schools(...):` |
| 매개변수 | 함수가 넘겨받는 값에 붙인 이름 | `school_name` |
| `return` | 결과를 돌려주고 함수를 끝내는 명령 | `return response.json()` |
| 딕셔너리 | 키와 값을 짝지어 담는 상자 | `{"SCHUL_NM": "서울고등학교"}` |
| 키 | 딕셔너리에서 값을 찾는 이름 | `"SCHUL_NM"` |
| 리스트 | 값을 순서대로 담는 상자 | `["중식", "석식"]` |
| 인덱스 | 리스트의 칸 번호. 0부터 센다 | `meals[0]` |
| 반복문 | 같은 일을 여러 번 하게 하는 문법 | `for name in conditions:` |
| 키워드 인자 | `이름=값`으로 넘기는 인자 | `timeout=10` |
| 내장 함수 | `import` 없이 쓸 수 있는 함수 | `print`, `input` |
| 객체 | 데이터와 기능을 함께 가진 값 | 문자열, 응답(`response`) |
| 메서드 | 객체에 딸린 기능 | `response.json()` |
| HTTP | 프로그램끼리 인터넷으로 요청과 응답을 주고받는 약속 | 웹 브라우저, `requests` |
| GET 요청 | "이 주소의 정보를 달라"는 HTTP 요청 | `requests.get(...)` |
| API | 프로그램끼리 정해진 방식으로 요청하고 답을 받는 창구 | NEIS Open API |
| 엔드포인트 | API 요청을 보내는 주소 | `https://open.neis.go.kr/hub/schoolInfo` |
| 쿼리 문자열 | 주소 뒤 `?` 다음에 붙는 `이름=값&이름=값` | `?Type=json&SCHUL_NM=...` |
| 퍼센트 인코딩 | 한글 같은 글자를 주소에 넣으려고 `%EC...`로 바꾸는 것 | `%EC%84%9C` |
| 상태 코드 | 서버가 응답에 붙이는 결과 번호 | `200` |
| 타임아웃 | 응답을 기다리는 최대 시간 | `timeout=10` |
| JSON | 데이터를 글자로 주고받는 약속된 모양 | `{"CODE": "INFO-000"}` |
| `float` | 소수점이 있는 숫자 | `1295.0` |

---

## 6. 개발자 질문

**질문: 개발 기록 4번의 [F](`requirements.txt`로 설치)도 해야 해?**

[F]는 따로 할 일이 아닙니다.
개발 기록 4번의 "개발자가 따라 할 순서" ①을 실행하면 나오는 화면입니다.
[A]~[F]는 모두 에이전트가 실행해 본 결과입니다.

이 컴퓨터에서는 ①을 실행해도 바뀌는 것이 없습니다.

- 가상환경은 프로젝트 폴더 안의 `.venv` 하나입니다. 에이전트와 개발자가 같은 `.venv`를 씁니다. (step01 2-2 참고)
- 에이전트가 이미 `requests`를 설치했으므로, `Requirement already satisfied`(이미 설치되어 있음)만 나옵니다.
- 여러 번 실행해도 이미 설치된 것은 건너뛰므로 안전합니다. 습관 삼아 실행해 두면 좋습니다.

다른 컴퓨터에서 저장소를 받았다면 ①은 꼭 해야 합니다.
그 컴퓨터의 `.venv`에는 `requests`가 없습니다. 빠뜨리면 `import requests` 줄에서 아래 오류가 납니다. (requests가 없는 Python으로 실제 실행한 결과)

```
Traceback (most recent call last):
  File "<string>", line 1, in <module>
    import requests
ModuleNotFoundError: No module named 'requests'
```

`.venv` 폴더는 `.gitignore`로 GitHub에 올리지 않습니다. 그래서 저장소에는 "무엇을 설치해야 하는지"를 적은 `requirements.txt`만 있고, 설치는 컴퓨터마다 직접 해야 합니다. (step01 2-4 참고)

---

## 7. 확인 문제

### 문제 1. 코드 읽기: 이 코드를 실행하면 화면에 무엇이 나올까요?

```python
params = {"Type": "json", "pIndex": 1}
search_conditions = {"MLSV_YMD": "20261105", "Type": "xml"}
for name in search_conditions:
    params[name] = search_conditions[name]
print(params)
```

<details><summary>정답</summary>

```
{'Type': 'xml', 'pIndex': 1, 'MLSV_YMD': '20261105'}
```

- `for`는 `search_conditions`의 키 `MLSV_YMD`, `Type`을 차례로 꺼냅니다.
- `MLSV_YMD`는 `params`에 없던 키라서 새로 생깁니다. 맨 뒤에 붙습니다.
- `Type`은 이미 있던 키라서 값이 `json`에서 `xml`로 **바뀝니다.** 자리는 원래 자리 그대로입니다.

그래서 `app/neis.py`에서 검색 조건에 `Type`을 넣으면 기본값 `json`을 덮어쓰게 됩니다. 그런 일이 없도록 검색 조건에는 서비스별 조건만 넣습니다.

(실제로 실행해 확인한 결과입니다.)

</details>

### 문제 2. 빈칸 채우기

`app/neis.py`의 `call_neis_api` 함수 마지막 부분입니다. 빈칸 세 곳을 채우세요.

```python
    response = requests.get(
        NEIS_BASE_URL + service_name,
        ______=params,
        ______=REQUEST_TIMEOUT_SECONDS,
    )
    return response.______()
```

<details><summary>정답</summary>

```python
    response = requests.get(
        NEIS_BASE_URL + service_name,
        params=params,
        timeout=REQUEST_TIMEOUT_SECONDS,
    )
    return response.json()
```

- `params`: 쿼리 문자열로 바뀔 딕셔너리를 넘기는 키워드 인자 이름입니다.
- `timeout`: 응답을 기다릴 최대 시간을 넘기는 키워드 인자 이름입니다.
- `json`: 응답 JSON을 딕셔너리로 바꾸는 메서드입니다. 괄호 `()`까지 써야 실제로 불립니다.

</details>

### 문제 3. 작은 수정: `https://open.neis.go.kr/hub/schoolInfo`가 출력되게 고치세요

```python
def make_url(service_name: str) -> str:
    url = "https://open.neis.go.kr/hub/" + service_name


print(make_url("schoolInfo"))
```

지금은 `None`이 출력됩니다.

<details><summary>정답</summary>

```python
def make_url(service_name: str) -> str:
    url = "https://open.neis.go.kr/hub/" + service_name
    return url


print(make_url("schoolInfo"))
```

결과:

```
https://open.neis.go.kr/hub/schoolInfo
```

함수 안에서 주소를 만들기만 하고 돌려주지 않았습니다. `return url`을 함수 안쪽(4칸 들여쓰기)에 넣어야 합니다.
`return`이 없는 함수는 `None`을 돌려줍니다. (2-1)

</details>

---

## 이번 단계 핵심 정리

1. `def 이름(매개변수: 타입) -> 반환 타입:`으로 함수를 만들고, `return`으로 결과를 돌려준다.
2. 딕셔너리는 `{키: 값}`, 리스트는 `[값, 값]`이다. 꺼낼 때는 `[키]`, `[번호(0부터)]`를 쓴다.
3. `for 키 in 딕셔너리:`로 키를 하나씩 꺼내 같은 일을 반복한다.
4. `requests.get(주소, params=..., timeout=...)`으로 요청하고, `.json()`으로 응답을 딕셔너리로 바꾼다.
5. NEIS 응답은 겹친 딕셔너리·리스트이고, 급식이 없는 날은 `RESULT`만 있는 다른 모양이 온다.
