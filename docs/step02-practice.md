# 2단계 실습 과제: 함수, 딕셔너리, 리스트, `for`, requests

## 이 문서를 다 풀면 할 수 있게 되는 것

1. 값을 받아 결과를 돌려주는 함수를 직접 만들 수 있다.
2. NEIS 응답처럼 겹쳐 있는 딕셔너리·리스트에서 원하는 값을 꺼낼 수 있다.
3. requests로 NEIS에 직접 요청하고, 결과를 `for`로 하나씩 출력할 수 있다.

## 시작하기 전에

- 함께 볼 문서: [`step02-learning.md`](step02-learning.md)
- 실습 파일은 `practice\step02\` 폴더에 만듭니다. (`New-Item -ItemType Directory -Force practice\step02`)
- 가상환경을 켜고 프로젝트 맨 위 폴더에서 실행합니다.
  - 보통 파일: `python practice\step02\파일.py`
  - `app`을 가져오는 파일: `python -m practice.step02.파일` (이유는 step01 실습 과제 6)
- 결과는 모두 실제로 실행해 확인했습니다. 과제 5, 6은 NEIS 자료라서 나중에 학교 정보가 바뀌면 결과도 달라질 수 있습니다.
- 인증키는 화면에 출력하지 않습니다.

---

## 과제 1. 결과를 돌려주는 함수 (★)

**다지는 개념**: `def`, 매개변수, `return`(2-1), 함수의 타입 힌트(2-2), 문자열 이어 붙이기 `+`(2-7)

**할 일**

`practice\step02\p1_function.py`를 만듭니다.

1. 함수 `add_dish`를 만듭니다. 메뉴 글자 `menu`와 반찬 이름 `dish`를 받아, 둘 사이에 `" / "`를 넣어 이어 붙인 글자를 **돌려줍니다.**
2. 매개변수와 반환값에 타입 힌트를 붙입니다.
3. 아래처럼 써서 결과를 출력합니다.
   ```python
   menu = "쌀밥"
   menu = add_dish(menu, "된장찌개")
   menu = add_dish(menu, "배추김치")
   print(menu)
   ```

**확인 방법**

```
쌀밥 / 된장찌개 / 배추김치
```

**더 해 보기**: 함수 안의 `return`을 지우고 실행해 봅니다. 무엇이 나오나요?

<details><summary>정답 예시</summary>

```python
# 함수 만들기 연습
def add_dish(menu: str, dish: str) -> str:
    return menu + " / " + dish


menu = "쌀밥"
menu = add_dish(menu, "된장찌개")
menu = add_dish(menu, "배추김치")
print(menu)
```

**더 해 보기**의 결과:

```
None
```

`return`이 없으면 함수는 계산만 하고 아무것도 돌려주지 않습니다. 돌려준 것이 없으면 `None`입니다. (step01 2-14)

</details>

---

## 과제 2. 딕셔너리와 리스트, 그리고 `for` (★)

**다지는 개념**: 딕셔너리(2-3), `for`(2-4), 리스트(2-5)

**할 일**

`practice\step02\p2_meal.py`를 만듭니다.

1. 딕셔너리 `meal`을 만듭니다. 키는 `"date"`(`"20261105"`), `"meal_name"`(`"중식"`), `"dishes"`(리스트 `["흑미밥", "부대찌개", "호박볶음"]`)입니다.
2. `meal_name`의 값을 출력합니다.
3. 새 키 `"calories"`에 `"812.4 Kcal"`를 넣습니다.
4. `for`로 `dishes`의 메뉴를 하나씩 꺼내, **번호와 함께** 출력합니다. 번호는 변수 `number`를 1부터 하나씩 늘려서 만듭니다.
5. 마지막에 `meal` 전체를 출력합니다.

**확인 방법**

```
중식
1 흑미밥
2 부대찌개
3 호박볶음
{'date': '20261105', 'meal_name': '중식', 'dishes': ['흑미밥', '부대찌개', '호박볶음'], 'calories': '812.4 Kcal'}
```

**더 해 보기**: 3번(새 키 넣기) 줄을 지우고 `print(meal["calories"])`를 실행해 보세요.

<details><summary>힌트</summary>

- 키로 값 꺼내기: `meal["meal_name"]`
- 새 키 넣기: `meal["calories"] = "812.4 Kcal"`
- 번호 늘리기: `number = number + 1`을 `for` 블록 **안에** 씁니다.

</details>

<details><summary>정답 예시</summary>

```python
# 딕셔너리, 리스트, for 연습
meal = {
    "date": "20261105",
    "meal_name": "중식",
    "dishes": ["흑미밥", "부대찌개", "호박볶음"],
}

print(meal["meal_name"])
meal["calories"] = "812.4 Kcal"

number = 1
for dish in meal["dishes"]:
    print(number, dish)
    number = number + 1

print(meal)
```

**더 해 보기**의 결과 (맨 아래 줄):

```
KeyError: 'calories'
```

없는 키로 값을 꺼내면 `KeyError`가 납니다. 6단계에서 배우는 `dict.get`을 쓰면 오류 대신 기본값을 받을 수 있습니다.

</details>

---

## 과제 3. 겹쳐 있는 응답에서 값 꺼내기 (★★)

**다지는 개념**: 겹쳐 있는 딕셔너리·리스트에서 값 꺼내기(2-6)

**할 일**

아래 코드를 `practice\step02\p3_nested.py`에 붙여 넣습니다. NEIS 급식 응답을 줄인 것입니다.

```python
response_body = {
    "mealServiceDietInfo": [
        {"head": [{"list_total_count": 2}, {"RESULT": {"CODE": "INFO-000", "MESSAGE": "정상 처리되었습니다."}}]},
        {
            "row": [
                {"SCHUL_NM": "서울고등학교", "MMEAL_SC_NM": "중식", "MLSV_YMD": "20261105", "DDISH_NM": "흑미밥 <br/>부대찌개 (1.2.5.6.9.10.12.13.15.16)"},
                {"SCHUL_NM": "서울고등학교", "MMEAL_SC_NM": "석식", "MLSV_YMD": "20261105", "DDISH_NM": "배추김치 (9)"},
            ]
        },
    ]
}
```

그 아래에 코드를 더해, 다음을 차례로 출력합니다.

1. 자료 개수(`list_total_count`)
2. 결과 코드(`RESULT` 안의 `CODE`)
3. **두 번째** 줄(`row`)의 메뉴(`DDISH_NM`)
4. `for`로 모든 `row`의 `MMEAL_SC_NM`과 `MLSV_YMD`

**확인 방법**

```
2
INFO-000
배추김치 (9)
중식 20261105
석식 20261105
```

<details><summary>힌트</summary>

바깥부터 한 겹씩 벗깁니다.

| 꺼내는 코드 | 결과 |
| --- | --- |
| `response_body["mealServiceDietInfo"]` | 리스트 (칸 2개) |
| `...[0]` | `head`가 든 딕셔너리 |
| `...[0]["head"]` | 리스트 (칸 2개) |
| `...[1]["row"]` | 급식 줄들의 리스트 |

리스트의 첫 칸은 `[0]`, 두 번째 칸은 `[1]`입니다.

</details>

<details><summary>정답 예시</summary>

```python
print(response_body["mealServiceDietInfo"][0]["head"][0]["list_total_count"])
print(response_body["mealServiceDietInfo"][0]["head"][1]["RESULT"]["CODE"])
print(response_body["mealServiceDietInfo"][1]["row"][1]["DDISH_NM"])

for row in response_body["mealServiceDietInfo"][1]["row"]:
    print(row["MMEAL_SC_NM"], row["MLSV_YMD"])
```

`app/formatter.py`의 `find_lunch_row`도 같은 방법으로 `["mealServiceDietInfo"][1]["row"]`를 꺼내 중식을 찾습니다.

</details>

---

## 과제 4. 키보드로 입력받아 요청 값 만들기 (★★)

**다지는 개념**: `input()`(2-9), 함수(2-1), 딕셔너리(2-3)

**할 일**

`practice\step02\p4_input.py`를 만듭니다.

1. 함수 `build_params`를 만듭니다. 학교 이름을 받아 아래 딕셔너리를 돌려줍니다.
   - `"Type"`: `"json"`, `"pIndex"`: `1`, `"pSize"`: `100`, `"SCHUL_NM"`: 받은 학교 이름
2. `input("학교 이름: ")`으로 학교 이름을 받습니다.
3. `build_params`의 결과를 출력하고, 그 안의 학교 이름 뒤에 `을(를) 찾습니다`를 붙여 출력합니다.
4. 실행한 뒤 `부산고등학교`를 입력하고 Enter를 누릅니다.

**확인 방법**

```
학교 이름: 부산고등학교
{'Type': 'json', 'pIndex': 1, 'pSize': 100, 'SCHUL_NM': '부산고등학교'}
부산고등학교을(를) 찾습니다
```

<details><summary>정답 예시</summary>

```python
# input과 함수 연습: 학교 찾기 요청에 넣을 값 만들기
def build_params(school_name: str) -> dict:
    return {"Type": "json", "pIndex": 1, "pSize": 100, "SCHUL_NM": school_name}


school_name = input("학교 이름: ")
params = build_params(school_name)
print(params)
print(params["SCHUL_NM"] + "을(를) 찾습니다")
```

- `input`은 Enter를 누를 때까지 기다렸다가, 입력한 글자를 돌려줍니다.
- `app/neis.py`도 이렇게 딕셔너리로 요청 값을 만들어 requests에 넘깁니다.

</details>

---

## 과제 5. requests로 NEIS 직접 불러 보기 (★★★)

**다지는 개념**: HTTP 요청과 requests(2-12), 키워드 인자(2-8), JSON(2-13)

**할 일**

`practice\step02\p5_requests.py`를 만듭니다. 프로젝트의 `app/neis.py`를 쓰지 않고, requests로 직접 요청합니다.

1. `requests`와, `app.config`의 `NEIS_API_KEY`를 가져옵니다.
2. `requests.get`으로 `https://open.neis.go.kr/hub/schoolInfo`에 요청합니다.
   - `params=`: `KEY`(인증키), `Type`(`json`), `pIndex`(1), `pSize`(100), `SCHUL_NM`(`서울고등학교`)
   - `timeout=10`
3. 응답을 `.json()`으로 딕셔너리로 바꿉니다.
4. 첫 번째 학교의 이름(`SCHUL_NM`), 교육청 코드와 학교 코드(`ATPT_OFCDC_SC_CODE`, `SD_SCHUL_CODE`), 도로명 주소(`ORG_RDNMA`)를 출력합니다.
5. `python -m practice.step02.p5_requests`로 실행합니다.

**확인 방법**

```
서울고등학교
B10 7010083
서울특별시 서초구 효령로 197
```

<details><summary>힌트</summary>

- 학교기본정보 응답의 모양은 급식과 같습니다. `["schoolInfo"][1]["row"][0]`이 첫 번째 학교입니다.
- 응답 전체가 궁금하면 `print(response_body)`로 한 번 봅니다. 응답에는 인증키가 들어 있지 않습니다.

</details>

<details><summary>정답 예시</summary>

```python
# requests로 NEIS 학교기본정보를 직접 불러 보기
import requests

from app.config import NEIS_API_KEY

response = requests.get(
    "https://open.neis.go.kr/hub/schoolInfo",
    params={"KEY": NEIS_API_KEY, "Type": "json", "pIndex": 1, "pSize": 100, "SCHUL_NM": "서울고등학교"},
    timeout=10,
)
response_body = response.json()
school = response_body["schoolInfo"][1]["row"][0]
print(school["SCHUL_NM"])
print(school["ATPT_OFCDC_SC_CODE"], school["SD_SCHUL_CODE"])
print(school["ORG_RDNMA"])
```

- `print(response.url)`은 하지 않습니다. 요청 주소에 `KEY=인증키`가 붙어 있기 때문입니다. (5단계 문제 1)

</details>

---

## 과제 6. 도전: 이름이 겹치는 학교 모두 출력하기 (★★★)

**다지는 개념**: `for`(2-4), 겹친 자료(2-6), requests(2-12)

**할 일**

`practice\step02\p6_many_schools.py`를 만듭니다.

1. 과제 5와 같은 방법으로 `동성고등학교`를 찾습니다. NEIS는 이름에 `동성고등학교`가 **들어간** 학교를 모두 돌려줍니다.
2. `for`로 모든 학교의 이름, 교육청 이름(`ATPT_OFCDC_SC_NM`), 학교 코드를 `/`로 나눠 출력합니다.
3. 학교가 몇 곳인지 세어 마지막에 출력합니다. (변수로 하나씩 셉니다)

**확인 방법**

```
동성고등학교 / 서울특별시교육청 / 7010155
부산동성고등학교 / 부산광역시교육청 / 7150139
광주동성고등학교 / 전남광주통합특별시교육청(광주) / 7140368
동성고등학교 / 충청북도교육청 / 8000530
포항동성고등학교 / 경상북도교육청 / 8750542
모두 5 곳
```

같은 이름(`동성고등학교`)이 두 곳입니다. 그래서 2단계에서 학교를 고를 때 **교육청 코드와 학교 코드를 함께** 저장했습니다.

<details><summary>정답 예시</summary>

```python
# 이름이 같은(비슷한) 학교 여러 곳을 for로 모두 출력하기
import requests

from app.config import NEIS_API_KEY

response = requests.get(
    "https://open.neis.go.kr/hub/schoolInfo",
    params={"KEY": NEIS_API_KEY, "Type": "json", "pIndex": 1, "pSize": 100, "SCHUL_NM": "동성고등학교"},
    timeout=10,
)
rows = response.json()["schoolInfo"][1]["row"]

count = 0
for row in rows:
    print(row["SCHUL_NM"], "/", row["ATPT_OFCDC_SC_NM"], "/", row["SD_SCHUL_CODE"])
    count = count + 1
print("모두", count, "곳")
```

</details>

---

## 다 풀었다면

- [ ] `return`이 있는 함수와 없는 함수의 차이를 말할 수 있다.
- [ ] `["키"]`와 `[번호]`를 이어 써서 겹친 자료의 값을 꺼낼 수 있다.
- [ ] requests의 `params=`, `timeout=`, `.json()`이 각각 무엇인지 말할 수 있다.

## 이번 단계 핵심 정리

1. 함수는 `def 이름(매개변수: 타입) -> 반환 타입:`으로 만들고, 결과는 `return`으로 돌려준다.
2. 딕셔너리는 `["키"]`, 리스트는 `[번호]`(0부터)로 값을 꺼낸다. 없는 키는 `KeyError`다.
3. `for 이름 in 리스트:`는 리스트의 값을 하나씩 꺼내 같은 일을 반복한다.
4. `requests.get(주소, params=..., timeout=...)`로 요청하고 `.json()`으로 딕셔너리를 받는다.
5. 인증키가 붙은 요청 주소는 출력하지 않는다.
