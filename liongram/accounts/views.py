from django.shortcuts import redirect, render
from .forms import UserCreateForm, SignUpForm
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm  # 장고에서 제공하는 기본 회원가입과 로그인 폼
from users.models import User

# Create your views here.

def signup_view(request):
    #GET 요청시 HTML 응답
    if request.method == 'GET':
        form = SignUpForm
        context = {'form': form}
        return render(request, 'accounts/signup.html', context)

    #POST 요청시 데이터 확인 후 회원 생상
    else:
        form = SignUpForm(request.POST)

        if form.is_valid(): #회원가입처리
            instance = form.save()
            return redirect('index')
            # username = form.cleaned_data['username']
            # email = form.cleaned_data['email']
            # password2 = form.cleaned_data['password2']

        else:   #리다이렉트
            print("ERROR")
            return redirect('accounts:signup')

def login_view(request):
    # GET, POST 분리
    if request.method == 'GET':
        # 로그인 HTML 응답
        form = AuthenticationForm
        context = {'form': form}
        return render(request, 'accounts/login.html', context)
    else:
        # 로그인 실행

        # 데이터 유효성 검사

        # 아래처럼 우리가 유효성 검사(전화번호면 re쓰거나 뭐 그런식으로) 할 수도 있는데, form에서 다 지원해주기에 우린 이거 써볼거.
        # username = request.POST.get('username')
        # password = request.POST.get('password')
        # if username == '' or username == None:
        #     pass
        # user = User.objects.get(username=username)  # username 필드가 username인 경우 가져와라
        # if user == None:    # 저 조회한 user가 없을 경우 
        #     pass

        # form 활용해서 유효성검사
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            # 비지니스 로직 처리 - 로그인 처리
            login(request, form.user_cache) # AuthenticationForm의 user_cache 돌아서 정상적으로 return되면 User가 들어가서 login처리 됨
            # 응답
            return redirect('index')

        else:
            # 비지니스 로직 처리 - 로그인 실패
            # 응답
            return render(request, 'accounts/login.html', {'form': form})   # 실패하면 form 그대로 주면 됨. form 그대로 날리면 실패 이유도 날려줌
            # form 자체에 실패사유, 로그인시도 정보 등 다 포함되어 있어서 그대로 보여주는 거임


def logout_view(request):
    #유효성 검사 - 로그인일 경우에만 해야 하는 유효성검사
    if request.user.is_authenticated:
    #비지니스 로직 처리 - 로그아웃
        logout(request)
    #응답
    return redirect('index')