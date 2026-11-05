# python practice step01\p3 - 변수, 타입 힌트, if/else, == 비교연산자, 상수

MAX_DISHES: int = 7 # 상수는 대문자로 작성하는 것이 관례
school_name: str = "서울고등학교"
dish_count: int = 6

print("학교:", school_name)
print("메뉴 수:", dish_count)

if dish_count == MAX_DISHES:
    print("메뉴가 가득 찼습니다.")
else:
    print("메뉴를 더 넣을 수 있습니다")

# 실행 결과
# 메뉴를 더 넣을 수 있습니다
# dish_count를 7로 바꾸고 실행
# 메뉴가 가득 찼습니다