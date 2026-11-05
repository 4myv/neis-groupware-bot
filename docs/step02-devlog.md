# 2단계 개발 기록: 데이터 조회

## 이 문서를 다 읽으면 할 수 있게 되는 것

1. NEIS 학교기본정보·급식식단정보 API에 무엇을 보내고 무엇을 받는지 설명할 수 있다.
2. 내 학교 코드를 찾아 `.env`에 넣고, 내 학교 급식의 JSON 원본을 직접 확인할 수 있다.
3. 2단계에서 실제로 겪은 문제와, 3단계에서 조심해야 할 응답 모양을 알 수 있다.

---

## 1. 목표

- `requests`로 NEIS 급식 API를 호출해 JSON 원본을 확인한다.
- 학교 이름으로 학교 코드(시도교육청코드, 행정표준코드)를 찾는 방법을 만든다.
- NEIS 호출 코드는 `app/neis.py` 한 곳에 모은다. 나중에 정기 알림과 명령어 응답이 함께 쓰게 하기 위해서다.

---

## 2. 한 일 (순서대로)

1. **1단계 push 확인**: GitHub의 `main`이 로컬 커밋 `7134649`와 같은 것을 확인했다.
2. **NEIS 공식 명세 확인**
   - 포털의 명세 표가 웹 페이지를 읽는 도구로는 비어 보였다. (5번 문제 1)
   - 그래서 포털 화면이 표를 그릴 때 쓰는 명세 데이터를 직접 받아 확인했다. (6번에 명세 요약)
3. **라이브러리 설치**: `requests`를 설치하고(2.34.2) `requirements.txt`에 추가했다.
4. **응답 모양 확인**
   - 공개된 예시 학교(서울고등학교)로 학교 조회와 급식 조회를 해 봤다.
   - 개발자의 학교 정보는 쓰지 않았다.
5. **코드 작성**: 아래 파일을 만들거나 고쳤다.
   - `app/neis.py`, `app/config.py`
   - `find_school.py`, `show_meal_json.py`
   - `requirements.txt`, `.env.example`
6. **동작 확인**
   - 네 가지 경우를 실행했다. (4번)
   - 시험 중에 한글 입력이 깨지는 문제를 겪었다. (5번 문제 2)
7. **문서 작성과 커밋**: 학습 정리와 개발 기록을 쓰고, 비밀 파일이 커밋 대상에 없는지 확인한 뒤 커밋한다.

---

## 3. 바뀐 파일

| 파일 | 추가·수정 | 내용 |
| --- | --- | --- |
| `app/neis.py` | 새 파일 | 공통 호출 함수 `call_neis_api`, 학교 찾기 `fetch_schools`, 급식 조회 `fetch_meals` |
| `app/config.py` | 수정 | `.env`에서 `NEIS_OFFICE_CODE`, `NEIS_SCHOOL_CODE`를 읽는 두 줄 추가 |
| `find_school.py` | 새 파일 | 학교 이름을 입력받아 NEIS 학교기본정보 응답을 그대로 출력 |
| `show_meal_json.py` | 새 파일 | 날짜를 입력받아 `.env`에 적은 학교의 급식식단정보 응답을 그대로 출력 |
| `requirements.txt` | 수정 | `requests==2.34.2` 추가 |
| `.env.example` | 수정 | `NEIS_OFFICE_CODE`, `NEIS_SCHOOL_CODE` 항목 추가 |
| `docs/step02-learning.md` | 새 파일 | 2단계 학습 정리 |
| `docs/step02-devlog.md` | 새 파일 | 이 문서 |

---

## 4. 실행 방법과 결과

### 개발자가 따라 할 순서

**① 가상환경을 켜고 새 라이브러리를 설치합니다.**

```powershell
cd C:\neis_groupware_bot
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

> 에이전트가 같은 `.venv`에 이미 설치해 두어서 `Requirement already satisfied`가 나올 것입니다. 정상입니다.

**② 내 학교 코드를 찾습니다.**

```powershell
python find_school.py
```

- 학교 이름을 입력하고 Enter를 누릅니다.
- 이름 일부만 넣으면 여러 학교가 나올 수 있으니 정확한 이름을 넣으세요.
- 결과에서 내 학교의 `"ATPT_OFCDC_SC_CODE"` 값과 `"SD_SCHUL_CODE"` 값을 찾습니다.

**③ `.env`에 두 줄을 추가합니다.**

```powershell
notepad .env
```

아래 두 줄을 추가하고 저장합니다. 값은 ②에서 찾은 것을 넣습니다.

```
NEIS_OFFICE_CODE=찾은_시도교육청코드
NEIS_SCHOOL_CODE=찾은_행정표준코드
```

> 학교 코드는 비밀값은 아닙니다. 하지만 어느 학교인지 드러나므로, 저장소에 올리지 않도록 코드 대신 `.env`에 둡니다.
> 에이전트에게 학교 이름이나 코드를 알려 줄 필요는 없습니다.

**④ 내 학교 급식 JSON을 확인합니다.**

```powershell
python show_meal_json.py
```

- 날짜를 `20261105`처럼 8자리로 입력합니다.
- 급식이 있는 평일 날짜를 넣어 보고, 주말 날짜도 넣어 보세요.

### 에이전트가 실행한 결과 (예시 학교)

> 아래 [A]~[F]는 에이전트가 확인한 결과입니다. 개발자가 따로 할 일이 아닙니다.
> 개발자는 위의 ①~④만 하고, 아래 결과는 내 화면과 비교할 때 봅니다.

| 결과 | 해당하는 순서 |
| --- | --- |
| [A] | ② `find_school.py` |
| [B], [C], [D] | ④ `show_meal_json.py` |
| [E] | 없음 (에이전트가 확인용으로만 해 본 것) |
| [F] | ① `python -m pip install -r requirements.txt` |

**[A] `find_school.py`에 `서울고등학교` 입력**

```
학교 이름을 입력하세요: {
  "schoolInfo": [
    {
      "head": [
        {
          "list_total_count": 1
        },
        {
          "RESULT": {
            "CODE": "INFO-000",
            "MESSAGE": "정상 처리되었습니다."
          }
        }
      ]
    },
    {
      "row": [
        {
          "ATPT_OFCDC_SC_CODE": "B10",
          "ATPT_OFCDC_SC_NM": "서울특별시교육청",
          "SD_SCHUL_CODE": "7010083",
          "SCHUL_NM": "서울고등학교",
          "ENG_SCHUL_NM": "Seoul High School",
          "SCHUL_KND_SC_NM": "고등학교",
          "LCTN_SC_NM": "서울특별시",
          "JU_ORG_NM": "서울특별시교육청",
          "FOND_SC_NM": "공립",
          "ORG_RDNZC": "06669 ",
          "ORG_RDNMA": "서울특별시 서초구 효령로 197",
          "ORG_RDNDA": "(서초동,서울고등학교)",
          "ORG_TELNO": "02-582-8151",
          "HMPG_ADRES": "http://seoul.sen.hs.kr",
          "COEDU_SC_NM": "남",
          "ORG_FAXNO": "02-587-3933",
          "HS_SC_NM": "일반고",
          "INDST_SPECL_CCCCL_EXST_YN": "N",
          "HS_GNRL_BUSNS_SC_NM": "일반계",
          "SPCLY_PURPS_HS_ORD_NM": null,
          "ENE_BFE_SEHF_SC_NM": "후기",
          "DGHT_SC_NM": "주간",
          "FOND_YMD": "19460201",
          "FOAS_MEMRD": "19460201",
          "LOAD_DTM": "20260423"
        }
      ]
    }
  ]
}
```

- 입력 안내 문구 바로 뒤에 결과가 붙어 나온 것은, 에이전트가 키보드 대신 자동으로 입력을 넣었기 때문입니다.
- 개발자가 직접 입력하면 입력한 이름 다음 줄부터 결과가 나옵니다.
- 이 학교의 코드는 시도교육청코드 `B10`, 행정표준코드 `7010083`입니다.

학교 이름 일부(`서울고`)로 찾았을 때는 `list_total_count`가 9였습니다.
서울고덕초등학교, 서울고등학교, 서울고명초등학교 등이 함께 나왔습니다.

**[B] `show_meal_json.py`, 예시 학교 코드, 날짜 `20261105`(목요일)**

이 실행에서만 학교 코드를 임시 환경 변수로 넣었습니다. 개발자의 `.env`는 건드리지 않았습니다.

```
날짜를 YYYYMMDD 형식으로 입력하세요 (예: 20261105): {
  "mealServiceDietInfo": [
    {
      "head": [
        {
          "list_total_count": 2
        },
        {
          "RESULT": {
            "CODE": "INFO-000",
            "MESSAGE": "정상 처리되었습니다."
          }
        }
      ]
    },
    {
      "row": [
        {
          "ATPT_OFCDC_SC_CODE": "B10",
          "ATPT_OFCDC_SC_NM": "서울특별시교육청",
          "SD_SCHUL_CODE": "7010083",
          "SCHUL_NM": "서울고등학교",
          "MMEAL_SC_CODE": "2",
          "MMEAL_SC_NM": "중식",
          "MLSV_YMD": "20261105",
          "MLSV_FGR": 1295.0,
          "DDISH_NM": "흑미밥 <br/>부대찌개 (1.2.5.6.9.10.12.13.15.16)<br/>호박볶음 (5.6)<br/>오지치즈스틱 (1.2.5.6.10.12.13)<br/>고등어구이 (1.5.6.7.13)<br/>백김치 (9)",
          "ORPLC_INFO": "쇠고기(종류) : 국내산(한우)<br/>쇠고기 식육가공품 : 국내산<br/>돼지고기 : 국내산<br/>돼지고기 식육가공품 : 국내산<br/>닭고기 : 국내산<br/>닭고기 식육가공품 : 국내산<br/>오리고기 : 국내산<br/>오리고기 가공품 : 국내산<br/>쌀 : 국내산<br/>배추 : 국내산<br/>고춧가루 : 국내산<br/>콩 : 국내산<br/>낙지 : 국내산<br/>고등어 : 국내산<br/>갈치 : 국내산<br/>오징어 : 국내산<br/>꽃게 : 국내산<br/>참조기 : 국내산<br/>비고 : ",
          "CAL_INFO": "625.4 Kcal",
          "NTR_INFO": "탄수화물(g) : 47.2<br/>단백질(g) : 37.6<br/>지방(g) : 30.7<br/>비타민A(R.E) : 33.3<br/>티아민(mg) : 0.5<br/>리보플라빈(mg) : 0.7<br/>비타민C(mg) : 36.8<br/>칼슘(mg) : 303.3<br/>철분(mg) : 2.8",
          "MLSV_FROM_YMD": "20261105",
          "MLSV_TO_YMD": "20261105",
          "LOAD_DTM": "20261105"
        },
        {
          "ATPT_OFCDC_SC_CODE": "B10",
          "ATPT_OFCDC_SC_NM": "서울특별시교육청",
          "SD_SCHUL_CODE": "7010083",
          "SCHUL_NM": "서울고등학교",
          "MMEAL_SC_CODE": "3",
          "MMEAL_SC_NM": "석식",
          "MLSV_YMD": "20261105",
          "MLSV_FGR": 250.0,
          "DDISH_NM": "돈육갈릭필라프 (1.5.6.10.12.13.16.18)<br/>고르곤조각피자 (1.2.5.6)<br/>감자양파국 (5.6)<br/>황도그린샐러드 (1.2.5.6.11.12)<br/>토마토소스펜네 (1.2.5.6.10.12.13.15.16.18)<br/>배추김치 (9)<br/>딸기요거트 (2)",
          "ORPLC_INFO": "(중식과 같은 내용이라 생략)",
          "CAL_INFO": "695.4 Kcal",
          "NTR_INFO": "탄수화물(g) : 108.6<br/>단백질(g) : 33.3<br/>지방(g) : 14.5<br/>비타민A(R.E) : 108.2<br/>티아민(mg) : 0.7<br/>리보플라빈(mg) : 0.6<br/>비타민C(mg) : 28.1<br/>칼슘(mg) : 252.1<br/>철분(mg) : 3.1",
          "MLSV_FROM_YMD": "20261105",
          "MLSV_TO_YMD": "20261105",
          "LOAD_DTM": "20261105"
        }
      ]
    }
  ]
}
```

석식의 `ORPLC_INFO`는 중식과 글자까지 같아서 문서에서만 줄였습니다.

**[C] 같은 학교, 날짜 `20261108`(일요일)**

```
날짜를 YYYYMMDD 형식으로 입력하세요 (예: 20261105): {
  "RESULT": {
    "CODE": "INFO-200",
    "MESSAGE": "해당하는 데이터가 없습니다."
  }
}
```

**[D] `.env`에 학교 코드가 없을 때**

개발자가 ③을 하기 전에 ④를 실행하면 이렇게 나옵니다.

```
날짜를 YYYYMMDD 형식으로 입력하세요 (예: 20261105): {
  "RESULT": {
    "CODE": "ERROR-300",
    "MESSAGE": "필수 값이 누락되어 있습니다. 요청인자를 참고 하십시오."
  }
}
```

**[E] 한 달 단위 조회 (확인용, 프로젝트 코드에는 없음)**

`MLSV_YMD`에 `202611`처럼 월만 넣었더니 11월 한 달 치 39건(중식 20건, 석식 19건)이 왔습니다.

**[F] `requirements.txt`로 설치 (①을 실행하면 나오는 화면)**

이 컴퓨터에서는 에이전트가 같은 `.venv`에 이미 설치해 두어서, 모두 `already satisfied`(이미 설치됨)로 나옵니다.

```
Requirement already satisfied: python-dotenv==1.2.4 in .\.venv\Lib\site-packages (from -r requirements.txt (line 7)) (1.2.4)
Requirement already satisfied: requests==2.34.2 in .\.venv\Lib\site-packages (from -r requirements.txt (line 11)) (2.34.2)
Requirement already satisfied: charset_normalizer<4,>=2 in .\.venv\Lib\site-packages (from requests==2.34.2->-r requirements.txt (line 11)) (3.5.2)
Requirement already satisfied: idna<4,>=2.5 in .\.venv\Lib\site-packages (from requests==2.34.2->-r requirements.txt (line 11)) (3.20)
Requirement already satisfied: urllib3<3,>=1.26 in .\.venv\Lib\site-packages (from requests==2.34.2->-r requirements.txt (line 11)) (2.8.0)
Requirement already satisfied: certifi>=2023.5.7 in .\.venv\Lib\site-packages (from requests==2.34.2->-r requirements.txt (line 11)) (2026.10.23)
```

---

## 5. 발생한 문제와 해결

### 문제 1. NEIS 포털의 명세 표가 비어 보임

- **상황**
  - 웹 페이지를 읽는 도구로 급식식단정보와 학교기본정보의 "Open API" 탭을 읽었다.
  - 그런데 요청 주소, 요청 인자, 출력값, 메시지 표가 모두 "해당 자료가 없습니다."로 나왔다.
  - 같은 데이터셋의 다른 탭 하나는 "시스템 작업중입니다."였다.
- **원인**
  - 포털 HTML에는 빈 표만 있다.
  - 실제 내용은 페이지의 스크립트(`/js/ggportal/data/service/selectOpenApi.js`)가 나중에 따로 받아 와서 채운다.
  - 웹 페이지를 읽는 도구는 스크립트를 실행하지 않아서 빈 표만 보였다.
- **해결**
  - 그 스크립트를 읽어, 표의 내용을 받아 오는 주소를 찾았다. (`/portal/data/openapi/selectOpenApiMeta.do`)
  - 그 주소에 데이터셋 번호(`infId`)를 보내 명세 데이터를 직접 받았다.
  - 포털 화면이 보여 주는 것과 같은 공식 데이터다. 요약은 6번에 있다.

### 문제 2. 시험 중 한글 학교 이름이 깨져서 학교를 찾지 못함

- **상황**
  - 에이전트가 PowerShell에서 `'서울고등학교' | python find_school.py`처럼 입력을 자동으로 넘겼다.
  - 그랬더니 `INFO-200 해당하는 데이터가 없습니다.`가 나왔다.
  - 같은 이름으로 직접 호출했을 때는 학교를 찾았다.
- **원인**
  - Python이 받은 글자를 확인해 보니 맨 앞에 BOM(파일 맨 앞에 붙는 보이지 않는 표시, `\ufeff`)이 붙어 있었다.

    ```
    bytes: b'\xef\xbb\xbf\xec\x84\x9c\xec\x9a\xb8\xea\xb3\xa0\xeb\x93\xb1\xed\x95\x99\xea\xb5\x90\r\n'
    decoded: '\ufeff서울고등학교\r\n'
    ```

  - Windows PowerShell 5.1이 파이프로 글자를 넘길 때 BOM을 붙였다. 그래서 NEIS는 `\ufeff서울고등학교`라는 학교를 찾았다.
- **해결**
  - 시험할 때는 Python에서 프로젝트 스크립트를 실행하며 BOM 없는 글자를 넘겼다.
  - 프로젝트 코드는 바꾸지 않았다. 개발자가 키보드로 직접 입력할 때는 생기지 않는 문제이기 때문이다.

---

## 6. 확인한 NEIS 공식 명세 요약

### 공통 기본 인자

| 인자 | 설명 | 기본값 |
| --- | --- | --- |
| `KEY` | 인증키 | sample key (인증키가 없으면 5건만 샘플로 출력) |
| `Type` | 호출 문서(xml, json) | xml |
| `pIndex` | 페이지 위치 | 1 |
| `pSize` | 페이지 당 신청 숫자 | 100 |

### 학교기본정보 (`https://open.neis.go.kr/hub/schoolInfo`)

- 요청 인자는 6개이며, 모두 필수가 아닙니다.
  - `ATPT_OFCDC_SC_CODE`(시도교육청코드)
  - `SD_SCHUL_CODE`(행정표준코드)
  - `SCHUL_NM`(학교명)
  - `SCHUL_KND_SC_NM`(학교종류명)
  - `LCTN_SC_NM`(시도명)
  - `FOND_SC_NM`(설립명)
- 출력값은 25개입니다. 이번에 쓰는 것은 `ATPT_OFCDC_SC_CODE`(시도교육청코드), `SD_SCHUL_CODE`(행정표준코드), `SCHUL_NM`(학교명)입니다.

### 급식식단정보 (`https://open.neis.go.kr/hub/mealServiceDietInfo`)

| 요청 인자 | 이름 | 필수 |
| --- | --- | --- |
| `ATPT_OFCDC_SC_CODE` | 시도교육청코드 | 필수 |
| `SD_SCHUL_CODE` | 행정표준코드 | 필수 |
| `MMEAL_SC_CODE` | 식사코드 | 선택 |
| `MLSV_YMD` | 급식일자 | 선택 |
| `MLSV_FROM_YMD` | 급식시작일자 | 선택 |
| `MLSV_TO_YMD` | 급식종료일자 | 선택 |

출력값은 15개입니다.

| 출력값 | 이름 |
| --- | --- |
| `ATPT_OFCDC_SC_CODE` | 시도교육청코드 |
| `ATPT_OFCDC_SC_NM` | 시도교육청명 |
| `SD_SCHUL_CODE` | 행정표준코드 |
| `SCHUL_NM` | 학교명 |
| `MMEAL_SC_CODE` | 식사코드 |
| `MMEAL_SC_NM` | 식사명 |
| `MLSV_YMD` | 급식일자 |
| `MLSV_FGR` | 급식인원수 |
| `DDISH_NM` | 요리명 |
| `ORPLC_INFO` | 원산지정보 |
| `CAL_INFO` | 칼로리정보 |
| `NTR_INFO` | 영양정보 |
| `MLSV_FROM_YMD` | 급식시작일자 |
| `MLSV_TO_YMD` | 급식종료일자 |
| `LOAD_DTM` | 수정일자 |

알레르기 번호(데이터셋 설명)는 아래와 같습니다.

```
1.난류, 2.우유, 3.메밀, 4.땅콩, 5.대두, 6.밀, 7.고등어, 8.게, 9.새우, 10.돼지고기,
11.복숭아, 12.토마토, 13.아황산류, 14.호두, 15.닭고기, 16.쇠고기, 17.오징어,
18.조개류(굴, 전복, 홍합 포함), 19.잣
```

### 결과 코드 (두 서비스 공통)

| 코드 | 메시지 |
| --- | --- |
| INFO-000 | 정상 처리되었습니다. |
| INFO-100 | (해당 자료는 단순 참고용으로만 활용하시기 바랍니다.) |
| INFO-200 | 해당하는 데이터가 없습니다. |
| INFO-300 | 관리자에 의해 인증키 사용이 제한되었습니다. |
| ERROR-290 | 인증키가 유효하지 않습니다. 인증키가 없는 경우, 홈페이지에서 인증키를 신청하십시오. |
| ERROR-300 | 필수 값이 누락되어 있습니다. 요청인자를 참고 하십시오. |
| ERROR-310 | 해당하는 서비스를 찾을 수 없습니다. 요청인자 중 SERVICE를 확인하십시오. |
| ERROR-333 | 요청위치 값의 타입이 유효하지 않습니다.요청위치 값은 정수를 입력하세요. |
| ERROR-336 | 데이터요청은 한번에 최대 1,000건을 넘을 수 없습니다. |
| ERROR-337 | 일별 트래픽 제한을 넘은 호출입니다. 오늘은 더이상 호출할 수 없습니다. |
| ERROR-500 | 서버 오류입니다. 지속적으로 발생시 홈페이지로 문의(Q&A) 바랍니다. |
| ERROR-600 | 데이터베이스 연결 오류입니다. 지속적으로 발생시 홈페이지로 문의(Q&A) 바랍니다. |
| ERROR-601 | SQL 문장 오류 입니다. 지속적으로 발생시 홈페이지로 문의(Q&A) 바랍니다. |

### 명세에 없고 실제 응답으로만 확인한 것

- `MMEAL_SC_CODE`의 값: `"2"`는 중식, `"3"`은 석식이었다. 조식은 예시 학교에 없어서 확인하지 못했다.
- 정상 응답의 모양: `{"서비스이름": [{"head": [...]}, {"row": [...]}]}`
- 데이터가 없거나 오류일 때의 모양: `{"RESULT": {"CODE": ..., "MESSAGE": ...}}` (서비스 이름 키가 없다)
- `MLSV_YMD`에 `YYYYMM`(월)을 넣으면 한 달 치가 온다. 공식 예시 주소에도 `MLSV_YMD=202202`가 있다.

---

## 7. 결정한 것과 이유

| 결정 | 다른 선택지 | 고른 이유 |
| --- | --- | --- |
| NEIS 호출을 `app/neis.py` 한 파일에 모음 | 스크립트마다 `requests.get`을 직접 쓰기 | 정기 알림과 명령어 응답이 같은 모듈을 쓰게 하라는 CLAUDE.md 구조를 따랐다. |
| 공통 함수 `call_neis_api` 하나와, 서비스별 함수 두 개(`fetch_schools`, `fetch_meals`) | 서비스별 함수마다 기본 인자와 `requests.get`을 반복 | 인증키, `Type`, 타임아웃을 한 곳에서만 관리한다. |
| 검색 조건을 `for`로 `params`에 덧붙임 | 딕셔너리의 `update` 메서드나 `|` 연산자 | 새 문법을 늘리지 않고, 이미 배워야 하는 `for`와 `[키] = 값`만으로 쓸 수 있다. |
| `Type=json`을 항상 넣음 | 생략 | 명세상 기본값이 xml이다. 빠뜨리면 `.json()`이 실패하는 것을 실제로 확인했다. |
| `pIndex=1`, `pSize=100` (첫 페이지만 받기) | 여러 페이지를 돌며 모두 받기 | 하루 급식은 몇 건뿐이다. 학교 검색도 정확한 이름이면 1건이다. 100건이 넘는 경우는 지금 다루지 않는다. |
| `timeout=10` | 타임아웃 없음 | 서버가 답하지 않을 때 프로그램이 멈추지 않게 한다. 실패했을 때의 처리(재시도, 관리자 알림)는 5단계에서 한다. |
| 2단계에서는 예외 처리를 하지 않음 | 지금 `try`로 감싸기 | CLAUDE.md 개발 단계상 예외 처리는 5단계다. 지금은 네트워크가 끊기면 Python 오류가 그대로 보인다. |
| `fetch_meals`는 식사 구분 없이 그날 급식을 모두 받음 | `MMEAL_SC_CODE=2`(중식)만 요청 | 원본 응답 전체를 먼저 보기 위해서다. 중식만 고르는 일은 3단계에서 정한다. |
| 학교 코드를 `.env`에 둠 | 코드나 설정 파일에 직접 쓰기 | 비밀값은 아니지만, 미성년 개발자가 다니는 학교가 저장소에 남지 않게 한다. |
| 시험은 공개된 예시 학교로 함 | 개발자에게 학교 이름을 물어보기 | 에이전트가 개발자의 학교를 알 필요가 없다. 개발자가 직접 찾아 `.env`에 넣으면 된다. |
| 실행 스크립트(`find_school.py`, `show_meal_json.py`)를 최상위에 둠 | `scripts/` 폴더 | 1단계 `check_setup.py`와 같은 이유다. 최상위에 있어야 `from app...` import가 바로 동작한다. |
| 날짜를 `input`으로 받음 | 오늘 날짜를 자동으로 계산 | 오늘 날짜 계산에는 `datetime`이 필요하다. 날짜 다루기는 3단계(날짜 형식 변환)에서 함께 배운다. |
| `requirements.txt`에는 `requests`만 고정 | `pip freeze` 결과 전체(딸려 오는 4개 포함) 고정 | 우리가 직접 쓰는 라이브러리만 관리한다. 딸려 오는 4개는 `requests`가 맞는 버전을 고른다. |
| 응답 JSON을 가공 없이 출력 | 필요한 값만 골라 출력 | CLAUDE.md 2단계 목표가 "JSON 원본 확인"이다. 가공은 3단계에서 한다. |
| 새 개념 13개를 한 단계에 다룸 | 2단계를 둘로 나누기 | 모두 "API를 한 번 호출해 결과를 보는" 하나의 흐름에 필요하다. 나누면 앞쪽 단계에는 동작하는 결과물이 없다. 다만 CLAUDE.md는 이럴 때 먼저 나누자고 제안하라고 했는데, 이번에는 제안 없이 진행했다. |

---

## 8. 다음 단계에서 할 일 (3단계: 데이터 변환)

1. **`DDISH_NM`의 실제 모양이 CLAUDE.md 예시와 다르다.** 변환 함수와 테스트는 두 모양을 모두 다뤄야 한다.

   | | 모양 |
   | --- | --- |
   | CLAUDE.md 예시 | `된장찌개(5.6.9.)` (괄호 앞 빈칸 없음, 끝에 점) |
   | 실제 응답 | `부대찌개 (1.2.5.6.9.10.12.13.15.16)` (괄호 앞 빈칸, 끝에 점 없음) |
   | 실제 응답 | `흑미밥 <br/>부대찌개` (`<br/>` 앞에 빈칸) |

2. 중식만 고른다. 실제 응답에서 `MMEAL_SC_CODE`가 `"2"`인 것이 중식이었다.
3. 데이터가 없는 날의 응답(`{"RESULT": {"CODE": "INFO-200", ...}}`)이면 `오늘은 급식이 없습니다.`를 만든다.
4. 날짜 `20261105`를 `11월 5일(목)`로 바꾼다.
5. 알레르기 번호는 버리지 않고 따로 보관한다.
6. `pytest`를 설치하고 변환 함수의 테스트를 쓴다.

---

## 확인한 공식 문서

- NEIS 급식식단정보 Open API: https://open.neis.go.kr/portal/data/service/selectServicePage.do?infId=OPEN17320190722180924242823&infSeq=2
- NEIS 학교기본정보 Open API: https://open.neis.go.kr/portal/data/service/selectServicePage.do?infId=OPEN17020190531110010104913&infSeq=2
- 위 두 페이지가 표를 그릴 때 쓰는 명세 데이터: `https://open.neis.go.kr/portal/data/openapi/selectOpenApiMeta.do` (POST, `infId`와 `infSeq=2`를 보냄)
- NEIS 개발자 가이드: https://open.neis.go.kr/portal/guide/apiGuidePage.do

## 이번 단계 핵심 정리

1. NEIS 호출은 `app/neis.py`의 `call_neis_api` 한 곳을 거친다. 인증키, `Type=json`, 타임아웃이 여기서 붙는다.
2. `find_school.py`로 학교 코드를 찾고, `.env`의 `NEIS_OFFICE_CODE`, `NEIS_SCHOOL_CODE`에 넣는다.
3. `show_meal_json.py`로 급식 JSON 원본을 확인한다. 급식이 없는 날은 `INFO-200`만 담긴 다른 모양이 온다.
4. 요청 인자와 출력값 이름은 NEIS 포털의 공식 명세 데이터로 확인했다.
5. 실제 `DDISH_NM` 모양이 CLAUDE.md 예시와 달라서, 3단계 변환 함수는 실제 모양을 기준으로 만든다.
