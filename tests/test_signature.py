# test_signature.py: Slack 요청 서명을 계산하고 확인하는 규칙을 확인하는 테스트
# 실행 방법(가상환경을 켠 상태에서, 프로젝트 최상위 폴더에서): python -m pytest
#
# 정답 값은 Slack 공식 문서 "Verifying requests from Slack"에 실린 계산 예시 그대로다.
# (예시용 가짜 Signing Secret이라 비밀값이 아니다.)

from app.auth import MAX_REQUEST_AGE_SECONDS, is_valid_slack_request, make_slack_signature

DOC_SECRET = "8f742231b10e8888abcd99yyyzzz85a5"
DOC_TIMESTAMP = "1531420618"
DOC_BODY = (
    b"token=xyzz0WbapA4vBCDEFasx0q6G&team_id=T1DC2JH3J&team_domain=testteamnow&channel_id=G8PSS9T3V"
    b"&channel_name=foobar&user_id=U2CERLKJA&user_name=roadrunner&command=%2Fwebhook-collect&text="
    b"&response_url=https%3A%2F%2Fhooks.slack.com%2Fcommands%2FT1DC2JH3J%2F397700885554%2F96rGlfmibIGlgcZRskXaIFfN"
    b"&trigger_id=398738663015.47445629121.803a0bc887a14d10d2c447fce8b6703c"
)
DOC_SIGNATURE = "v0=a2114d57b48eac39b9ad189dd8316235a7b4a8d21a10bd27519666489c69b503"
DOC_TIME = float(DOC_TIMESTAMP)


def test_signature_matches_official_example():
    assert make_slack_signature(DOC_SECRET, DOC_TIMESTAMP, DOC_BODY) == DOC_SIGNATURE


def test_valid_request_is_accepted():
    assert is_valid_slack_request(DOC_SECRET, DOC_TIMESTAMP, DOC_SIGNATURE, DOC_BODY, DOC_TIME + 10)


def test_changed_body_is_rejected():
    assert not is_valid_slack_request(DOC_SECRET, DOC_TIMESTAMP, DOC_SIGNATURE, DOC_BODY + b"&x=1", DOC_TIME)


def test_wrong_secret_is_rejected():
    assert not is_valid_slack_request("wrong-secret", DOC_TIMESTAMP, DOC_SIGNATURE, DOC_BODY, DOC_TIME)


def test_old_request_is_rejected_even_with_correct_signature():
    # 재전송 공격: 서명은 맞지만 5분보다 오래된 요청
    assert not is_valid_slack_request(DOC_SECRET, DOC_TIMESTAMP, DOC_SIGNATURE, DOC_BODY, DOC_TIME + MAX_REQUEST_AGE_SECONDS + 1)


def test_missing_headers_are_rejected():
    assert not is_valid_slack_request(DOC_SECRET, "", "", DOC_BODY, DOC_TIME)
