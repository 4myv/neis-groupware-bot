# test_auth.py: 토큰을 새로 발급받을 때가 되었는지 판단하는 규칙을 확인하는 테스트
# 실행 방법(가상환경을 켠 상태에서, 프로젝트 최상위 폴더에서): python -m pytest
#
# Slack에 실제로 요청을 보내는 함수는 여기서 시험하지 않는다. 시간 계산만 확인한다.

from app.auth import REFRESH_MARGIN_SECONDS, needs_refresh

EXPIRES_AT = 100000.0


def test_no_refresh_when_plenty_of_time_left():
    assert not needs_refresh(EXPIRES_AT, EXPIRES_AT - 3600)


def test_refresh_when_inside_margin():
    assert needs_refresh(EXPIRES_AT, EXPIRES_AT - REFRESH_MARGIN_SECONDS + 1)


def test_refresh_exactly_at_margin():
    assert needs_refresh(EXPIRES_AT, EXPIRES_AT - REFRESH_MARGIN_SECONDS)


def test_refresh_when_already_expired():
    assert needs_refresh(EXPIRES_AT, EXPIRES_AT + 10)
