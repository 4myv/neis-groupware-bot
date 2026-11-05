# python practice step01\p4 - if/else, 들여쓰기, == 비교연산자, 문자열

# 오류 고쳐보기 -> python 오류 메시지를 읽고 한 곳씩 고치기
# 초기 코드
# school_code = "7010083"
# if school_code = "7010083"
#     print(학교 코드가 맞습니다)
# else:
#     print("학교 코드가 다릅니다")

# 오류 메시지 1
# File "C:\neis_groupware_bot\practice\step01\p4_fix.py", line 5
#     if school_code = "7010083"
#        ^^^^^^^^^^^^^^^^^^^^^^^
# SyntaxError: invalid syntax. Maybe you meant '==' or ':=' instead of '='?
# 메시지를 보고 파악한 오류 -> 비교연산자 ==가 아닌 대입연산자 = 사용

# 1차 수정 후 코드
# school_code = "7010083"
# if school_code == "7010083"
#     print(학교 코드가 맞습니다)
# else:
# print("학교 코드가 다릅니다")

# 오류 메시지 2
# File "C:\neis_groupware_bot\practice\step01\p4_fix.py", line 20
#     if school_code == "7010083"
#                                ^
# SyntaxError: expected ':'
# 메시지를 보고 파악한 오류 -> if절 끝에 콜론(:)이 빠짐

# 2차 수정 후 코드
# school_code = "7010083"
# if school_code == "7010083":
#     print(학교 코드가 맞습니다)
# else:
# print("학교 코드가 다릅니다")

# 오류 메시지 3
# File "C:\neis_groupware_bot\practice\step01\p4_fix.py", line 35
#     print(학교 코드가 맞습니다)
#           ^^^^^^
# SyntaxError: invalid syntax. Perhaps you forgot a comma?
# 메시지를 보고 파악한 오류 -> print(학교 코드가 맞습니다)에 ""이 빠짐

# 3차 수정 후 코드
# school_code = "7010083"
# if school_code == "7010083":
#     print("학교 코드가 맞습니다")
# else:
# print("학교 코드가 다릅니다")

# 오류 메시지 4
# File "C:\neis_groupware_bot\practice\step01\p4_fix.py", line 51
#     print("학교 코드가 다릅니다")
#     ^^^^^
# IndentationError: expected an indented block after 'else' statement on line 50
# 메시지를 보고 파악한 오류 -> else 절 print("학교 코드가 다릅니다")에 들여쓰기가 없음

# 4차 수정 후 코드
school_code = "7010083"
if school_code == "7010083":
    print("학교 코드가 맞습니다")
else:
    print("학교 코드가 다릅니다")

# 결과 - 정상 작동
# 학교 코드가 맞습니다