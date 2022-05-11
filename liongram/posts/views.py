from django.shortcuts import redirect, render, get_object_or_404
from django.http import Http404, HttpResponse, JsonResponse
from django.views.generic import ListView
from .models import Post
from django.contrib.auth.decorators import login_required
from .forms import PostBaseForm, PostCreateForm

def index(request):
    post_list = Post.objects.all().order_by('-created_at')      # object 전체 불러 담기. 작성일 역순으로
    context = {         # render 인자 중 하나인 context와 이름 동일하게 설정
        'post_list': post_list,
    }
    return render(request, 'index.html', context)

def post_list_view(request):
    post_list = Post.objects.all()      # object 전체 불러 담기
    post_list = Post.objects.filter(writer=request.user)      # object 필터해서 불러 담기. foreign key로 설정한 writer가 현재 로그인 user와 같은 것 필터
    context = {         # render 인자 중 하나인 context와 이름 동일하게 설정
        'post_list': post_list,
    }
    return render(request, 'posts/post_list.html', context)


def post_detail_view(request, id):
    try:
        post = Post.objects.get(id=id)      # object 전체 불러 담기
    except Post.DoesNotExist:
        return redirect('index')    # 게시글이 없을 경우 redirect해서 root로
    context = {
        'post': post,
    }
    return render(request, 'posts/post_detail.html', context)

def post_create_view(request):
    if request.method == 'GET': # GET이면 그냥 form 보여줘서 글쓰게 하고,
        return render(request, 'posts/post_form.html')
    else:
        image = request.FILES.get('image')  # image는 파일로 날라와서 file로 받아야 함
        content = request.POST.get('content')  # POST로 날리니 POST로 받아야 함
        print(image, content)
        Post.objects.create(image=image,    # 이제 db에 실질적으로 data생성하기. 간단하네 디게
        content=content,
        writer=request.user,     # 현재 사용자페이지에는 login 없어서 에러남. admin에서 로그인하고 글작성해야 됨. 이게 머지? 왜 admin에서 로그인했는데 사용자페이지도 로그인되지???
        )
        return redirect('index')    # POST로 데이터 전송이면 저장되게. 지금은 그냥 index로

def post_create_form_view(request):
    if request.method == 'GET':
        # form = PostBaseForm()
        form = PostCreateForm() #CreateForm으로 받아보기
        context = {'form': form}
        return render(request, 'posts/post_form2.html', context)
    else:
        form = PostCreateForm(request.POST, request.FILES)

        if form.is_valid():     # cleand_data 쓰기 위해, 내가 받은 image와 content가 유효성검사가 적합한지 판단해야 함
            Post.objects.create(
                image=form.cleaned_data['image'],   # cleaned_data : 유효성 검사. form은 rendering 외에도 유효성 검사, 후처리(제대로 수행했을때 처리라는디?)도 해줌
                content=form.cleaned_data['content'],
                writer=request.user
            )
        else:
            return redirect('posts:post-create')
        return redirect('index')    # POST로 데이터 전송이면 저장되게. 지금은 그냥 index로
    
def post_update_view(request, id):  # create, detail이 합쳐졌따 볼 수 있음
    # post = Post.objects.get(id=id)
    post = get_object_or_404(Post, id=id, writer=request.user)   # 위와 같지만, object 없을 경우 404 page로 뿌려주게. 나중에 404 페이지도 만들거라서 이렇게 하는게 안전한 코딩이래 오호
    if request.method == "GET": # update 폼에 미리 작성되어있던 내용 전달해주기
        context = { 'post': post}
        return render(request, 'posts/post_form.html', context)
    elif request.method == "POST":
        new_image = request.FILES.get('image')
        content = request.POST.get('content')
        if new_image:   # 새로운 이미지가 들어올 때, 기존 이미지는 삭제하고 저장. 이렇게 안하면 기존 게시글의 이미지가 계속 남아있어서. 이미지 교체임
            post.image.delete()
            post.image = new_image
        post.content = content
        post.save()
        return redirect('posts:post-detail', post.id)


@login_required
def post_delete_view(request, id):
    post = get_object_or_404(Post, id=id, writer=request.user)  # 여기서 writer로 검증시켜도 아래 작성한 코드처럼 Http404 오류 나타냄.
    # if request.user != post.writer:
    #    raise Http404('잘못된 접근')

    if request.method == 'GET':
        context = {'post': post}
        return render(request, 'posts/post_confirm_delete.html', context)
    else:
        post.delete()
        return redirect('index')


# Create your views here.

# 응답예시 확인 중
def url_view(request):
    print('url_view()') # 함수 실행중인거 확인하게
    # return HttpResponse('<h1>url_view<h1>') # <h1> 같이 tag를 넣어도 작동함. html로 작동한다는 의미.
    #HttpResponse에서 content(받은 변수)를 text html로 날려주게 돼있어서

    data = {'code' : '001', 'msg' : 'OK'}
    return JsonResponse(data)   # Json은 key:value의 dict 형태의 값을 넣어줘야 함



# view에서는 data를 받을 때, url, form 등으로 받거나 get, post 방식으로 받게?요청?될 수 있음. 모든 받는 방법 알아야 함.


def url_parameter_view(request, username):  # username : urls에서 받은 변수명. 이렇게 reuqeust 뒤에 매개변수로 추가해서 받을 수 있음
    print('url_parameter_view')

    # 1. 경로로 받기 << 이게 pathvariable
    print(username)


    # 2. query parameter로 받기
    # ?where=nexearch&a=? << 이런거
    print(request.GET)  # url에 key=value로 넣은거 고대로 key : 'value' 형태로 출력

    # f 스트링으로 받아서 출력해보기. terminal에서 좀 더 직관적으로 볼 수 있게
    print(f'username: {username}')
    print(f'request.GET: {request.GET}')

    return HttpResponse(username)


def function_view(request):

    # view에서 data를 받을 수 있는 3가지 방법(현재는 3개만 배움) 1. 경로변수(path variable)   2. query string(key:value)   3. form(post로 data 쏘는 등의 형식)
    print(f'request.method: {request.method}')
    print(f'request.GET: {request.GET}')    # GET은 일반적으로 data, resource 받을때 사용
    print(f'request.POST: {request.POST}')  # Post는 데이터 추가/삭제 등을 할때 사용


    # 보통 이렇게 GET/POST마다 다른 방식으로 처리한대.
    if request.method == 'GET':
        print(f'request.GET: {request.GET}')
    elif request.method == 'POST':
        print(f'request.POST: {request.POST}') 

    # html 담는 폴더명은 꼭 templates여야 함. django에서 설정한 약속
    return render(request, 'view.html') # html file을 응답해줄때 render 쓰나봐. request, template name 넣어서 응답


class class_view(ListView): # listView 들어가보면 또 내부에서 계~~속 상속받는데 쨌든 model 있어야 해서 이전에 만든 model 사용
    model = Post        # model(데이터) 는 Post에서
    order_by = ['-id']  # order 정렬도 해줄 수 있음
    template_name = 'cbv_view.html' # 위 데이터를 이 템플릿으로. 이거 안쓰면 default 값으로 모델명(post) + "_list.html"로 들어감
    # 클래스 기반 뷰의 장점 : 간단한 두줄만으로 list 출력해낼 정도로 굉장한 생산성과 안정적인 코드 작성


# 위 listView 클래스를 함수기반 뷰로 짠다면?
def function_list_view(request):
    object_list = Post.objects.all().order_by('-id')    # 모델을 직접 all로 불러서 order시켜야 하는 반복작업 필요.
    return render(request, 'cbv_view.html', {'object_list' : object_list})  # 그 받은 모델을 또 키:value로 넘겨줘야 하는 반복작업 필요
    # 이뿐만 아니라, 다양한 기능이 있고 이 기능들 쓰려면 엄청 많은 코드를 써야하는데 클래스기반 뷰는 이를 줄여줌