# 3단계 실습 과제: 문자열 다루기, f-문자열, 날짜, pytest

## 이 문서를 다 풀면 할 수 있게 되는 것

1. `split`, `strip`, `join`, 슬라이싱으로 글자를 원하는 모양으로 다듬을 수 있다.
2. 날짜 글자를 날짜로 바꾸고, f-문자열로 새 모양의 글자를 만들 수 있다.
3. 직접 만든 함수를 pytest 테스트로 확인할 수 있다.

## 시작하기 전에

- 함께 볼 문서: [`step03-learning.md`](step03-learning.md)
- 실습 파일은 `practice\step03\` 폴더에 만듭니다. (`New-Item -ItemType Directory -Force practice\step03`)
- 가상환경을 켜고 프로젝트 맨 위 폴더에서 실행합니다.
  - 보통 파일: `python practice\step03\파일.py`
  - `app`을 가져오는 파일: `python -m practice.step03.파일`
- 결과는 모두 실제로 실행해 확인했습니다.

---

## 과제 1. 나누고, 다듬고, 다시 잇기 (★)

**다지는 개념**: `split`과 `strip`(2-1), 빈 리스트와 `append`(2-4), `join`(2-6)

**할 일**

`practice\step03\p1_split_join.py`를 만듭니다.

1. `text = "  쌀밥 / 김치찌개 /  깍두기 "`를 `/`로 나눠 출력합니다.
2. 빈 리스트 `dishes`를 만들고, 나눈 조각마다 앞뒤 빈칸을 지워 `append`합니다. 결과를 출력합니다.
3. `dishes`를 `", "`로 이어 하나의 글자로 출력합니다.

**확인 방법**

```
['  쌀밥 ', ' 김치찌개 ', '  깍두기 ']
['쌀밥', '김치찌개', '깍두기']
쌀밥, 김치찌개, 깍두기
```

첫 줄을 보면 `split`은 빈칸까지 그대로 남깁니다. 그래서 `strip`이 필요합니다.

<details><summary>정답 예시</summary>

```python
# split, strip, append, join 연습
text = "  쌀밥 / 김치찌개 /  깍두기 "
pieces = text.split("/")
print(pieces)

dishes = []
for piece in pieces:
    dishes.append(piece.strip())
print(dishes)
print(", ".join(dishes))
```

- `join`은 **구분자**에 붙는 메서드입니다: `", ".join(리스트)`. `리스트.join(", ")`이 아닙니다.
- `app/formatter.py`의 `split_dishes`도 같은 방법으로 `<br/>`를 기준으로 나누고 다듬습니다.

</details>

---

## 과제 2. 맨 뒤 괄호 안의 글자 꺼내기 (★★)

**다지는 개념**: `endswith`, `rfind`, `isdigit`(2-2), 슬라이싱(2-3), `not`(2-5)

**할 일**

`practice\step03\p2_last_paren.py`를 만듭니다.

1. 함수 `get_last_paren_text(dish: str) -> str`
   - 글자가 `)`로 끝나지 않으면 빈 글자 `""`를 돌려줍니다.
   - 끝나면, **맨 뒤** `(`의 위치를 찾아 괄호 **안쪽** 글자만 잘라 돌려줍니다.
2. 함수 `is_allergy_text(text: str) -> bool`
   - 점(`.`)을 모두 지운 뒤 숫자뿐이면 `True`입니다.
3. 아래 네 메뉴로 확인합니다.
   ```python
   for dish in ["혼합잡곡밥(연) (5)", "된장찌개(5.6.9.)", "사과(1/2)", "흑미밥"]:
       inside = get_last_paren_text(dish)
       print(dish, "→", inside, is_allergy_text(inside))
   ```

**확인 방법**

```
혼합잡곡밥(연) (5) → 5 True
된장찌개(5.6.9.) → 5.6.9. True
사과(1/2) → 1/2 False
흑미밥 →  False
```

- 첫 줄: 괄호가 두 개지만 **맨 뒤** 괄호만 봅니다. 그래서 `rfind`입니다.
- 마지막 줄: 빈 글자의 `isdigit()`은 `False`입니다.

<details><summary>힌트</summary>

- `rfind("(")`: 뒤에서부터 찾은 `(`의 번호
- `dish[시작:-1]`: 시작부터 마지막 글자 `)` 바로 앞까지
- `text.replace(".", "")`: 점을 모두 지운 새 글자

</details>

<details><summary>정답 예시</summary>

```python
# rfind, endswith, 슬라이싱, isdigit 연습
def get_last_paren_text(dish: str) -> str:
    # 맨 뒤 괄호 안의 글자를 돌려준다. 괄호로 끝나지 않으면 빈 글자.
    if not dish.endswith(")"):
        return ""
    start = dish.rfind("(")
    return dish[start + 1:-1]


def is_allergy_text(text: str) -> bool:
    # 점을 지우고 남은 것이 숫자뿐이면 알레르기 번호다.
    return text.replace(".", "").isdigit()


for dish in ["혼합잡곡밥(연) (5)", "된장찌개(5.6.9.)", "사과(1/2)", "흑미밥"]:
    inside = get_last_paren_text(dish)
    print(dish, "→", inside, is_allergy_text(inside))
```

`app/formatter.py`의 `find_allergy_start`가 하는 일과 거의 같습니다. 비교해 읽어 보세요.

</details>

---

## 과제 3. 짧은 날짜 모양 만들기 (★★)

**다지는 개념**: `datetime`(2-8), f-문자열(2-9), 리스트 타입 힌트(2-7)

**할 일**

`practice\step03\p3_short_date.py`를 만듭니다.

1. 요일 이름 리스트 상수 `WEEKDAY_NAMES`를 만듭니다. (타입 힌트 `list[str]`)
2. 함수 `format_short_date(yyyymmdd: str) -> str`: `"20261225"`를 `"12/25(금)"` 모양으로 바꿉니다.
3. `"20261225"`와 `"20270101"`로 확인합니다.

**확인 방법**

```
12/25(금)
1/1(금)
```

`1/1`처럼 월과 일 앞에 0이 붙지 않습니다. `day.month`, `day.day`는 숫자라서 그렇습니다.

<details><summary>정답 예시</summary>

```python
# datetime과 f-문자열 연습
from datetime import datetime

WEEKDAY_NAMES: list[str] = ["월", "화", "수", "목", "금", "토", "일"]


def format_short_date(yyyymmdd: str) -> str:
    day = datetime.strptime(yyyymmdd, "%Y%m%d")
    return f"{day.month}/{day.day}({WEEKDAY_NAMES[day.weekday()]})"


print(format_short_date("20261225"))
print(format_short_date("20270101"))
```

- f-문자열의 `{}` 안에는 `WEEKDAY_NAMES[day.weekday()]`처럼 계산식도 쓸 수 있습니다.
- `f`를 빠뜨리면 `{day.month}/...`가 글자 그대로 나옵니다.

</details>

---

## 과제 4. 내 함수를 pytest로 확인하기 (★★)

**다지는 개념**: pytest와 `assert`(2-12), `not`(2-5), "없음"을 `[]`로 돌려주기(2-11)

**할 일**

`practice\step03\test_practice.py`를 만듭니다. **파일 이름이 `test_`로 시작해야** pytest가 찾습니다.

1. `app.formatter`의 `extract_allergy_numbers`를 가져옵니다.
2. 함수 `has_allergy(dish: str) -> bool`: 알레르기 번호가 하나라도 있으면 `True`. (`extract_allergy_numbers`가 `[]`를 돌려주면 번호가 없는 것)
3. 테스트 함수 세 개를 만듭니다. 이름은 `test_`로 시작합니다.
   - `"고등어구이 (1.5.6.7.13)"` → 있음
   - `"흑미밥"` → 없음
   - `"사과(1/2)"` → 없음
4. 실행합니다. **폴더를 적어 주어야** 이 폴더의 테스트를 실행합니다. (`pytest.ini`가 평소에는 `tests` 폴더만 보게 되어 있기 때문)
   ```powershell
   python -m pytest practice\step03 -v
   ```

**확인 방법**

```
practice/step03/test_practice.py::test_dish_with_allergy_numbers PASSED
practice/step03/test_practice.py::test_dish_without_allergy_numbers PASSED
practice/step03/test_practice.py::test_parentheses_that_are_not_allergy PASSED
============================== 3 passed ==============================
```

**더 해 보기**: 셋째 테스트의 `not`을 지우고 다시 실행해 보세요. `FAILED`와 함께 어디가 틀렸는지 나옵니다.

<details><summary>정답 예시</summary>

```python
# pytest 연습: 직접 만든 함수를 직접 만든 테스트로 확인한다
from app.formatter import extract_allergy_numbers


def has_allergy(dish: str) -> bool:
    return extract_allergy_numbers(dish) != []


def test_dish_with_allergy_numbers():
    assert has_allergy("고등어구이 (1.5.6.7.13)")


def test_dish_without_allergy_numbers():
    assert not has_allergy("흑미밥")


def test_parentheses_that_are_not_allergy():
    assert not has_allergy("사과(1/2)")
```

- `assert 조건`: 조건이 `True`면 통과, `False`면 실패입니다.
- 테스트 함수 이름이 `test_`로 시작하지 않으면 pytest가 테스트로 보지 않습니다. (step03 확인 문제 3)

</details>

---

## 과제 5. 프로젝트 함수로 메뉴와 알레르기 번호 출력하기 (★★★)

**다지는 개념**: f-문자열(2-9), `join`(2-6), 딕셔너리가 든 리스트(2-7), `if` / `else`

**할 일**

`practice\step03\p5_parse_menu.py`를 만듭니다.

1. `app.formatter`의 `parse_dishes`를 가져옵니다.
2. 아래 글자를 `parse_dishes`에 넣으면, 메뉴마다 `{"name": ..., "allergy_numbers": [...]}`가 든 리스트가 나옵니다.
   ```python
   ddish_text = "흑미밥 <br/>부대찌개 (1.2.5.6.9.10.12.13.15.16)<br/>호박볶음 (5.6)<br/>백김치 (9)"
   ```
3. 메뉴마다 한 줄씩, 알레르기 번호가 없으면 `알레르기 번호 없음`, 있으면 번호를 `", "`로 이어 출력합니다. f-문자열을 씁니다.
4. `python -m practice.step03.p5_parse_menu`로 실행합니다.

**확인 방법**

```
흑미밥 - 알레르기 번호 없음
부대찌개 - 알레르기 번호 1, 2, 5, 6, 9, 10, 12, 13, 15, 16
호박볶음 - 알레르기 번호 5, 6
백김치 - 알레르기 번호 9
```

3단계부터 따로 보관해 둔 알레르기 번호를, 이렇게 사람이 읽기 좋게 보여 줄 수 있습니다.

<details><summary>정답 예시</summary>

```python
# 프로젝트 함수 parse_dishes로 메뉴와 알레르기 번호를 함께 출력하기
from app.formatter import parse_dishes

ddish_text = "흑미밥 <br/>부대찌개 (1.2.5.6.9.10.12.13.15.16)<br/>호박볶음 (5.6)<br/>백김치 (9)"

for dish in parse_dishes(ddish_text):
    if dish["allergy_numbers"] == []:
        print(f"{dish['name']} - 알레르기 번호 없음")
    else:
        print(f"{dish['name']} - 알레르기 번호 {', '.join(dish['allergy_numbers'])}")
```

- f-문자열이 큰따옴표 `"..."`라서, 안쪽 키는 작은따옴표 `'name'`으로 씁니다.

</details>

---

## 과제 6. 도전: 못 찾으면 `-1`을 돌려주는 함수 (★★★)

**다지는 개념**: "없음"을 돌려주는 방법(2-11), `in`(2-5), `for` 안의 `return`

**할 일**

`practice\step03\p6_find_dish.py`를 만듭니다.

1. 함수 `find_dish_index(dishes: list[str], word: str) -> int`
   - `word`가 **들어 있는** 첫 메뉴의 번호(0부터)를 돌려줍니다.
   - 없으면 `-1`을 돌려줍니다.
   - 번호는 변수로 하나씩 셉니다.
2. `["흑미밥", "부대찌개", "호박볶음", "고등어구이"]`에서 `"찌개"`, `"구이"`, `"피자"`를 찾아 출력합니다.

**확인 방법**

```
1
3
-1
```

<details><summary>힌트</summary>

- `"찌개" in "부대찌개"`는 `True`입니다. 글자 안에 다른 글자가 들어 있는지도 `in`으로 확인합니다.
- `for` 안에서 `return`을 만나면 반복과 함수가 함께 끝납니다. 끝까지 못 찾으면 `for` 다음 줄로 내려옵니다.

</details>

<details><summary>정답 예시</summary>

```python
# "없음"을 -1로 돌려주는 함수 만들기
def find_dish_index(dishes: list[str], word: str) -> int:
    index = 0
    for dish in dishes:
        if word in dish:
            return index
        index = index + 1
    return -1


dishes = ["흑미밥", "부대찌개", "호박볶음", "고등어구이"]
print(find_dish_index(dishes, "찌개"))
print(find_dish_index(dishes, "구이"))
print(find_dish_index(dishes, "피자"))
```

- 문자열의 `rfind`도 못 찾으면 `-1`을 돌려줍니다. 같은 약속입니다.

</details>

---

## 다 풀었다면

- [ ] `split` → `strip` → `join` 순서로 글자를 다듬을 수 있다.
- [ ] `strptime`으로 날짜를 읽고, f-문자열로 원하는 모양을 만들 수 있다.
- [ ] `test_`로 시작하는 파일과 함수를 만들어 pytest로 실행할 수 있다.

## 이번 단계 핵심 정리

1. `split`은 나누기, `strip`은 앞뒤 빈칸 지우기, `"구분자".join(리스트)`는 잇기다.
2. `rfind`는 뒤에서부터 찾고, 못 찾으면 `-1`이다. 슬라이싱 `[시작:끝]`은 끝 칸을 넣지 않는다.
3. f-문자열은 `f"...{값}..."`이고, `f`를 빠뜨리면 `{}`가 글자 그대로 나온다.
4. pytest는 `test_`로 시작하는 파일·함수를 찾고, `assert`가 `False`면 실패다.
5. 프로젝트 함수(`parse_dishes` 등)를 가져와 새 기능을 만들어 볼 수 있다.
