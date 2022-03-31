from django.shortcuts import render
from django.http import HttpResponse
import random  # import 파일 최상단에 위치하는게 윈칙

# Create your views here.
def calculator(reqeust):        # django 규칙 : 요청을 처리하는 함수는 항상 request를 매개변수로 받아야 함.
    # return HttpResponse("계산기 기능 구현 시작!")

    # request 출력
    print(f'request = {reqeust}')
    print(f'request type = {type(reqeust)}')
    print(f'request __dict__ = {reqeust.__dict__}')


    # 1. 데이터 확인
    num1 = reqeust.GET.get('num1')
    num2 = reqeust.GET.get('num2')
    operators = reqeust.GET.get('operators')
    if num1 is not None and num2 is not None:
        num1 = int(num1)
        num2 = int(num2)

        # 2. 계산
        if operators == "+":
            result = num1 + num2
        elif operators == "-":
            result = num1 - num2
        elif operators == "*":
            result = num1 * num2
        elif operators == "/":
            result = num1 / num2
        else:
            result = 0
    else:
        result = 0

    # 3. 응답
    return render(reqeust, 'calculator.html', {'result': result})   # result값을 result 이름으로 넘겨주기

def lotto(request):
    return render(request, 'lotto.html')

def lottoresult(request):
    #게임수 받기
    games = int(request.GET.get('games'))

    #전체 로또번호 받을 리스트
    lotto_numbers = None
    lotto_numbers = list()

    for _ in range(games):
        # 게임별 로또번호 받을 리스트
        lotto_number = list()
        for _ in range(7):
            number = random.randint(1, 45)
            while True:

                # 이미 나왔던 숫자면 다시 숫자 추출
                if number in lotto_number:
                    number = random.randint(1, 45)
                else:
                    break
            lotto_number.append(number)
        lotto_numbers.append(lotto_number)
    return render(request, 'lottoresult.html',{'lotto_number': lotto_numbers, 'games': games})