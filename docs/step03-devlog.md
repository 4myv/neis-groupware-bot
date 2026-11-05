# 3단계 개발 기록: 데이터 변환

## 이 문서를 다 읽으면 할 수 있게 되는 것

1. NEIS 급식 응답이 어떤 규칙으로 메시지가 되는지 설명할 수 있다.
2. 변환 함수의 테스트를 직접 실행하고, 내 학교 급식을 메시지 모양으로 볼 수 있다.
3. 3단계에서 실제로 겪은 문제와, 아직 남아 있는 한계를 알 수 있다.

---

## 1. 목표

CLAUDE.md의 데이터 변환 규칙대로 메시지를 만드는 함수와, 그 함수의 pytest 테스트를 작성한다.

| 원본 | 변환 후 | 규칙 |
| --- | --- | --- |
| `된장찌개(5.6.9.)` | `된장찌개` | 괄호 안 알레르기 번호 제거 (번호는 따로 보관) |
| `쌀밥<br/>된장찌개` | `쌀밥 / 된장찌개` | 줄바꿈 태그를 구분자로 변경 |
| `20261105` | `11월 5일(목)` | 날짜를 읽기 쉬운 형식으로 |
| 데이터 없음 | `오늘은 급식이 없습니다.` | 주말·방학·공휴일은 오류가 아닌 정상 상황 |

2단계에서 확인한 **실제 응답 모양**(`부대찌개 (1.2.5.6)`, `흑미밥 <br/>...`)도 함께 다룬다.

---

## 2. 한 일 (순서대로)

1. `pytest`를 설치했다(9.2.0). `datetime`의 요일 번호(월요일 0 ~ 일요일 6)를 실제로 확인했다.
2. `app/formatter.py`를 만들었다. 함수 9개가 한 가지 일씩 맡는다.
   - 메뉴 나누기, 알레르기 괄호 찾기, 알레르기 번호 지우기, 알레르기 번호 꺼내기
   - 메뉴 정리, 날짜 바꾸기, 중식 고르기, 메뉴 이름 잇기, 메시지 완성
3. `tests/test_formatter.py`에 테스트 18개를 썼다. CLAUDE.md 예시 모양과 실제 응답 모양을 모두 넣었다.
4. 테스트를 실행했다. `python -m pytest`는 통과했지만 `pytest`만 치면 실패했다. (5번 문제 1) `pytest.ini`를 추가해 고쳤다.
5. **여러 지역 실제 데이터로 시험**
   - 공개 학교 6곳(서울·부산·경기·대구·제주·광주)의 2026년 9~10월 급식 메뉴 2,935개를 변환해 봤다.
   - 알레르기 번호를 놓치거나 이름이 빈 칸이 된 경우는 없었다. (4번 결과 3)
   - 그 과정에서 찾은 모양 두 가지를 테스트로 추가해 테스트가 20개가 되었다.
6. `show_lunch_message.py`를 만들어 예시 학교로 메시지를 확인했다.
7. NEIS가 오류를 돌려줄 때의 동작을 확인했다. 지금은 오류도 "급식이 없습니다"로 보인다. (5번 문제 2, 5단계에서 고침)
8. 빈 `tests` 폴더를 Git에 남기려고 넣었던 `tests/.gitkeep`을 지웠다. 이제 `tests`에 실제 파일이 있기 때문이다.
9. 학습 정리와 개발 기록을 쓰고, 비밀 파일이 커밋 대상에 없는지 확인한 뒤 커밋한다.

---

## 3. 바뀐 파일

| 파일 | 추가·수정 | 내용 |
| --- | --- | --- |
| `app/formatter.py` | 새 파일 | 변환 함수 9개와 상수 4개 |
| `tests/test_formatter.py` | 새 파일 | 테스트 20개 |
| `pytest.ini` | 새 파일 | `pythonpath = .`, `testpaths = tests` |
| `show_lunch_message.py` | 새 파일 | `.env`의 학교 중식을 메시지 모양으로 출력 |
| `requirements.txt` | 수정 | `pytest==9.2.0` 추가 |
| `tests/.gitkeep` | 삭제 | 더 이상 필요 없음 |
| `docs/step03-learning.md` | 새 파일 | 3단계 학습 정리 |
| `docs/step03-devlog.md` | 새 파일 | 이 문서 |

---

## 4. 실행 방법과 결과

### 개발자가 따라 할 순서

```powershell
cd C:\neis_groupware_bot
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt     # 이 컴퓨터에서는 already satisfied가 나옵니다
python -m pytest -v                           # 테스트 20개 실행
python show_lunch_message.py                  # 날짜를 넣으면 내 학교 중식 메시지가 나옵니다
```

> `show_lunch_message.py`는 2단계에서 `.env`에 넣은 `NEIS_OFFICE_CODE`, `NEIS_SCHOOL_CODE`를 씁니다.

### 결과 1: 테스트 (`python -m pytest -v`)

```
platform win32 -- Python 3.13.16, pytest-9.2.0, pluggy-1.7.0 -- C:\neis_groupware_bot\.venv\Scripts\python.exe
cachedir: .pytest_cache
rootdir: C:\neis_groupware_bot
configfile: pytest.ini
testpaths: tests
collecting ... collected 20 items

tests/test_formatter.py::test_split_dishes_claude_md_example PASSED      [  5%]
tests/test_formatter.py::test_split_dishes_removes_spaces_around_tag PASSED [ 10%]
tests/test_formatter.py::test_remove_allergy_numbers_claude_md_example PASSED [ 15%]
tests/test_formatter.py::test_remove_allergy_numbers_real_format PASSED  [ 20%]
tests/test_formatter.py::test_remove_allergy_numbers_without_numbers PASSED [ 25%]
tests/test_formatter.py::test_remove_allergy_numbers_keeps_parentheses_in_name PASSED [ 30%]
tests/test_formatter.py::test_remove_allergy_numbers_keeps_amount_in_parentheses PASSED [ 35%]
tests/test_formatter.py::test_allergy_numbers_after_name_with_parentheses PASSED [ 40%]
tests/test_formatter.py::test_extract_allergy_numbers_claude_md_example PASSED [ 45%]
tests/test_formatter.py::test_extract_allergy_numbers_real_format PASSED [ 50%]
tests/test_formatter.py::test_extract_allergy_numbers_without_numbers PASSED [ 55%]
tests/test_formatter.py::test_parse_dishes_keeps_name_and_allergy_numbers PASSED [ 60%]
tests/test_formatter.py::test_format_date_claude_md_example PASSED       [ 65%]
tests/test_formatter.py::test_format_date_sunday PASSED                  [ 70%]
tests/test_formatter.py::test_format_date_new_year PASSED                [ 75%]
tests/test_formatter.py::test_find_lunch_row_picks_lunch PASSED          [ 80%]
tests/test_formatter.py::test_find_lunch_row_when_no_data PASSED         [ 85%]
tests/test_formatter.py::test_find_lunch_row_when_only_dinner PASSED     [ 90%]
tests/test_formatter.py::test_format_lunch_message_real_data PASSED      [ 95%]
tests/test_formatter.py::test_format_lunch_message_no_data_is_normal PASSED [100%]

============================= 20 passed in 0.12s ==============================
```

### 결과 2: 메시지 (`show_lunch_message.py`, 예시 학교 서울고등학교)

이 실행에서만 예시 학교 코드를 임시 환경 변수로 넣었습니다. 개발자의 `.env`는 건드리지 않았습니다.

날짜 `20261105`(목요일):

```
날짜를 YYYYMMDD 형식으로 입력하세요 (예: 20261105): [11월 5일(목) 중식]
흑미밥 / 부대찌개 / 호박볶음 / 오지치즈스틱 / 고등어구이 / 백김치
```

날짜 `20261108`(일요일):

```
날짜를 YYYYMMDD 형식으로 입력하세요 (예: 20261105): [11월 8일(일) 중식]
오늘은 급식이 없습니다.
```

### 결과 3: 여러 지역 실제 데이터로 시험

| 학교 (공개 예시) | 교육청 코드 | 2026년 9~10월에 있던 식사 |
| --- | --- | --- |
| 서울고등학교 | B10 | 중식("2"), 석식("3") |
| 부산고등학교 | C10 | 조식("1"), 중식("2"), 석식("3") |
| 경기고등학교 | B10 | 중식, 석식 |
| 대구고등학교 | D10 | 중식 |
| 제주고등학교 | T10 | 중식 |
| 광주고등학교 | F10 | 조식, 중식, 석식 |

- 확인한 메뉴: 2,935개 (조식·중식·석식 모두)
- 알레르기 번호를 지운 뒤 이름이 빈 칸이 된 메뉴: 0개
- 괄호 안에 숫자가 있는데 알레르기 번호로 보지 않은 메뉴: 3개. 셋 다 메뉴 이름의 일부라서 남기는 것이 맞다.
  - `사과(1/2)`: 반쪽
  - `골드파인애플스틱(40g)`: 무게
  - `하우스귤(5~)`: 개수
- 메뉴 이름 안에 괄호가 있는 경우도 많았다. 이런 괄호는 그대로 남고, 끝의 알레르기 번호만 지워졌다.
  - 예: `혼합잡곡밥(연) (5)` → `혼합잡곡밥(연)`
  - 예: `알타리무김치(급식용) (9)` → `알타리무김치(급식용)`
- 2단계에서는 확인하지 못했던 **조식 코드 `"1"`**을 부산·광주 학교에서 확인했다.

### 결과 4: NEIS가 오류를 돌려줄 때 (인증키를 일부러 틀리게 넣은 실행)

원본 응답:

```
{
  "RESULT": {
    "CODE": "ERROR-290",
    "MESSAGE": "인증키가 유효하지 않습니다. 인증키가 없는 경우, 홈페이지에서 인증키를 신청하십시오."
  }
}
```

메시지:

```
[11월 5일(목) 중식]
오늘은 급식이 없습니다.
```

---

## 5. 발생한 문제와 해결

### 문제 1. `pytest`만 치면 테스트 파일을 불러오지 못함

- **에러** (`pytest` 실행)

  ```
  ERROR collecting tests/test_formatter.py
  ImportError while importing test module 'C:\neis_groupware_bot\tests\test_formatter.py'.
  ...
  E   ModuleNotFoundError: No module named 'app'
  ...
  !!!!!!!!!!!!!!!!!!! Interrupted: 1 error during collection !!!!!!!!!!!!!!!!!!!!
  ```

- **원인**
  - `python -m pytest`는 지금 폴더(프로젝트 최상위)를 모듈 찾는 곳에 넣는다. 그래서 `app`을 찾는다.
  - `pytest`만 치면 그렇게 하지 않는다. 그래서 `tests` 안의 파일이 `app`을 찾지 못했다.
- **해결**
  - 프로젝트 최상위에 `pytest.ini`를 만들고 `pythonpath = .`을 넣었다.
  - 그 뒤 `pytest`와 `python -m pytest` 모두 테스트를 통과하는 것을 확인했다.

### 문제 2. NEIS 오류 응답도 "오늘은 급식이 없습니다."로 보임 (아직 남은 한계)

- **상황**: 인증키가 틀려 NEIS가 `ERROR-290`을 돌려줬는데, 메시지는 "오늘은 급식이 없습니다."였다. (4번 결과 4)
- **원인**: `find_lunch_row`는 `mealServiceDietInfo` 키가 없으면 모두 "급식 없음"으로 본다. 데이터 없음(`INFO-200`)과 오류(`ERROR-...`)를 구별하지 않는다.
- **해결 계획**
  - 오류 처리는 CLAUDE.md 개발 단계상 5단계다.
  - 5단계에서 `app/neis.py`가 결과 코드를 먼저 확인하게 한다. 오류면 재시도하고, 그래도 실패하면 관리자에게 알린다.
  - 그러면 변환 함수에는 정상 응답(`INFO-000`)이나 데이터 없음(`INFO-200`)만 오게 된다.
  - 3단계 변환 함수는 그대로 둔다.

---

## 6. 결정한 것과 이유

| 결정 | 다른 선택지 | 고른 이유 |
| --- | --- | --- |
| 정규식(`re`) 대신 문자열 메서드(`split`, `strip`, `rfind`, `isdigit`)와 슬라이싱 사용 | `re.sub(r"\s*\([\d.]+\)$", "", dish)` 한 줄 | 정규식은 짧지만 초보자가 읽기 어렵다. CLAUDE.md의 "초보자가 읽을 수 있는 코드" 규칙을 따랐다. |
| 마지막 괄호 안이 **숫자와 점으로만** 되어 있을 때만 알레르기 번호로 봄 | 마지막 괄호를 무조건 지우기 | 실제 데이터에 `(연)`, `(급식용)`, `(1/2)`, `(40g)`처럼 메뉴 이름의 일부인 괄호가 많았다. |
| 알레르기 번호를 문자열 리스트(`["5", "6"]`)로 보관 | 정수 리스트(`[5, 6]`) | 지금은 숫자 계산을 하지 않는다. 숫자로 바꾸는 문법을 이번 단계에 더하지 않으려고 했다. |
| 메뉴마다 `{"name": ..., "allergy_numbers": [...]}` 딕셔너리로 정리(`parse_dishes`) | 이름 리스트와 번호 리스트를 따로 | 이름과 번호가 짝으로 붙어 있어야 나중에 "알레르기" 명령어로 확장하기 쉽다. 이미 배운 딕셔너리만으로 만들 수 있다. |
| 함수가 "없음"을 알릴 때 `-1`, `[]`, `{}` 사용 | `None` | 돌려주는 타입이 늘 같아서, 받는 쪽이 `None` 처리를 따로 하지 않아도 된다. |
| 급식이 없을 때도 제목 줄(`[11월 8일(일) 중식]`)을 붙임 | "오늘은 급식이 없습니다."만 보내기 | 어느 날짜의 안내인지 알 수 있다. 메시지 모양도 급식이 있는 날과 같아진다. |
| "급식 없음" 문구는 CLAUDE.md 그대로(`오늘은 급식이 없습니다.`) | "이날은 급식이 없습니다." 등으로 바꾸기 | 규칙 문구를 그대로 따랐다. 다만 8단계 `내일 급식` 명령에서는 "오늘은"이 어색하다. 그때 문구를 다시 정한다. (7번) |
| 테스트 데이터는 실제 응답을 줄인 딕셔너리를 테스트 파일 안에 직접 씀 | 응답 JSON 파일을 따로 두고 읽기 | 파일 읽기 문법을 더하지 않는다. 테스트를 읽는 사람이 데이터를 한 파일에서 바로 볼 수 있다. |
| `pytest`를 `requirements.txt`에 함께 적음 | 개발용 목록 파일(`requirements-dev.txt`)을 따로 | 파일을 하나로 유지하는 편이 초보자에게 단순하다. |
| `pytest.ini` 추가 | `python -m pytest`만 쓰라고 안내 | 개발자가 어느 쪽으로 쳐도 동작하게 한다. (5번 문제 1) |
| 오류 응답을 구별하는 일은 5단계로 미룸 | 3단계에서 바로 처리 | CLAUDE.md는 한 단계에 한 가지만 하고 순서를 바꾸지 말라고 했다. 대신 한계를 기록했다. (5번 문제 2) |
| 단계를 나누지 않고, 학습 정리를 A·B·C 세 부분으로 나눔 | 3단계를 둘로 나누자고 제안하기 | 새 개념이 14개로 많다. 하지만 개발자가 "마지막 단계까지 계속하고, 문제나 내 역할이 생길 때만 멈추라"고 했다. 그래서 멈추지 않고 문서를 나눠 읽기 쉽게 했다. |

---

## 7. 다음 단계에서 할 일

**4단계: 메시지 전송 (Slack)**

1. Slack 공식 문서에서 `chat.postMessage`의 주소, 토큰 전달 방식, 응답 모양을 확인한다.
2. 메시지를 보낼 채널 ID가 필요하다. 채널 ID는 개발자의 Slack 화면에서 찾아야 하므로 **개발자의 역할**이 생긴다.
3. CLAUDE.md의 "토큰 발급, 만료되면 새로 발급"을 Slack에서 어떻게 할지 정해야 한다. Slack 봇 토큰은 토큰 자동 교체를 켜지 않으면 만료되지 않는다. 이것을 켤지는 **개발자가 정할 일**이다.

**나중 단계에서 다시 볼 것**

- 5단계: NEIS 결과 코드가 `ERROR-`이면 재시도하고, 관리자 오류 알림을 보낸다. (5번 문제 2)
- 8단계: `내일 급식` 응답에서 "오늘은 급식이 없습니다." 문구가 어색하지 않은지 정한다.

---

## 확인한 문서

- 입력 데이터 모양은 2단계에서 확인한 NEIS 공식 명세와 실제 응답이다. (`docs/step02-devlog.md`)
- 이번 단계에 새로 쓴 외부 API는 없다.

## 이번 단계 핵심 정리

1. `app/formatter.py`가 NEIS 응답을 `[11월 5일(목) 중식]` + 메뉴 이름 목록 메시지로 바꾼다.
2. 알레르기 번호는 마지막 괄호 안이 숫자와 점일 때만 지우고, 메뉴마다 따로 보관한다.
3. 테스트 20개가 CLAUDE.md 예시 모양과 실제 응답 모양을 모두 확인한다. 6개 지역 메뉴 2,935개로도 시험했다.
4. `pytest.ini` 덕분에 `pytest`와 `python -m pytest` 모두 동작한다.
5. NEIS 오류도 지금은 "급식이 없습니다"로 보인다. 5단계에서 고친다.
