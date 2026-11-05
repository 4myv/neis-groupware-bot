# test_sender.py: Slack 응답을 보고 "새 토큰을 받아 다시 보낼지" 판단하는 규칙을 확인하는 테스트
# 실행 방법(가상환경을 켠 상태에서, 프로젝트 최상위 폴더에서): python -m pytest
#
# Slack에 실제로 요청하지 않는다. 오류 코드는 Slack 공식 문서와 4단계에서 실제로 받은 응답을 썼다.

from app.sender import needs_new_token


def test_expired_token_needs_new_token():
    assert needs_new_token({"ok": False, "error": "token_expired"})


def test_invalid_auth_needs_new_token():
    assert needs_new_token({"ok": False, "error": "invalid_auth"})


def test_channel_not_found_does_not_need_new_token():
    assert not needs_new_token({"ok": False, "error": "channel_not_found"})


def test_success_does_not_need_new_token():
    # 성공 응답에는 error 키가 없다. not True 에서 바로 False가 정해져서 error를 꺼내지 않는다.
    assert not needs_new_token({"ok": True, "channel": "C123", "ts": "1.0"})
