# commands.py: 사용자가 봇에게 보낸 말을 명령어로 해석하는 파일
#
# CLAUDE.md 규칙: 앞뒤 공백과 띄어쓰기 차이는 무시한다. (내일급식 = 내일 급식)
# 7단계에서는 어떤 명령어인지 고르기만 하고, 답장을 만드는 일은 8단계에서 한다.

# 명령어의 이름. 글자를 여러 곳에 직접 쓰면 오타가 나기 쉬워서 이름을 붙여 둔다.
TODAY_LUNCH: str = "today_lunch"
TOMORROW_LUNCH: str = "tomorrow_lunch"
THIS_WEEK_SCHEDULE: str = "this_week_schedule"
HELP: str = "help"

# 사용자가 보내는 말 → 명령어 이름. 띄어쓰기를 모두 지운 모양으로 적어 둔다.
COMMANDS: dict[str, str] = {
    "오늘급식": TODAY_LUNCH,
    "내일급식": TOMORROW_LUNCH,
    "이번주일정": THIS_WEEK_SCHEDULE,
    "도움말": HELP,
}


def remove_spaces(text: str) -> str:
    # split()은 빈칸·줄바꿈·탭을 모두 기준으로 자른다. 잘린 조각을 다시 이어 붙이면 띄어쓰기가 모두 사라진다.
    return "".join(text.split())


def parse_command(text: str) -> str:
    key = remove_spaces(text)
    if key in COMMANDS:
        return COMMANDS[key]
    # 목록에 없는 말은 도움말로 답한다. (CLAUDE.md: "도움말 또는 그 밖의 말")
    return HELP
