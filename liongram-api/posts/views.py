from ast import operator
from django.shortcuts import redirect, render
from rest_framework.viewsets import ModelViewSet
from .serializers import CommentHyperlinkedModelSerializer, CommentListModelSerializer, PostListModelSerializer, PostBaseModelSerializer, PostCreateModelSerializer, PostRetrieveModelSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view, action
from rest_framework.views import APIView
from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from core.permissions import IsOwnerOnly


from posts.models import Post, Comment

# Create your views here.

# 게시글 목록 + 게시글 생성 한번에
class PostListCreateView(generics.ListAPIView, generics.CreateAPIView):   # ListAPIView에 작성된 get 함수와 return하는 list. APIView라고 명명하는게 좋은데 지금은 그냥 이렇게
    # list는 또 queryset, page 등을 담고있음. 이것들을 상속받아서 정의해줘야 함.
    # 즉, queryset과 serializer_class 는 항상 필수래
    # Create는 Post, List는 get형태로 짜여져있어서 하나의 class에 두개 기능 처리 가능. 이렇게 기능이 다 합쳐진게 ViewSet이래
    # 나중에 직접 사용해볼수록 직접 못만들어서 막히는 경우가 생긴대. 다 들어가서 보고 공부하고 그래야 한대
    queryset = Post.objects.all()
    serializer_class = PostListModelSerializer

    # 생성자 만들어주기. overriding으로
    # CreateAPIView의 post와 CreateAPIView가 상속받은 CreateModelMixin의 create 재정의
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # 우리가 바꾼 부분
        # 작성자 받게 customizing
        # self.perform_create(serializer)
        if request.user.is_authenticated:
            instance = serializer.save(writer=request.user)
        else:
            serializer.save()

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

# 게시글 상세, 업데이트(수정), 삭제
# View끼리 상속받는 것들이 포함되어 있는 경우들이 있어서 어떤 기능끼리 묶을지 알아야 하나봐? 걍 다 하나로 묶으면 안되나
# 웹개발이랑 다르게 RESTFul하게 작성이 되어야 하는데, GET, PUT, PATCH, DELETE는 모두 url에 id값이 들어가있어야 해서 하나로 묶인대. 오호
# 목록, 게시글생성은 GET/POST이 또 하나로 묶이고
# API Guide에 있는 표처럼 기능별로 묶어야 하나봐
# PUT, PATCH 차이. PUT은 자원의 전체를 교체. PATCH는 부분적으로 교체. 차이점은 알고 있어야 한대
# UpdateView에 put, patch 따로 구분해서 함수 해놨음
class PostRetrieveUpdateView(generics.RetrieveAPIView, generics.RetrieveUpdateAPIView, generics.RetrieveDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostRetrieveModelSerializer


    

class PostModelViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostListModelSerializer

    # def get_serializer_class(self):
    #     if self.action == 'create':
    #         return PostBaseModelSerializer
    #     return super().get_serializer_class()

    def get_permissions(self):
        permission_classes = list()
        action = self.action
        if action == 'list':
            permission_classes = [AllowAny]
        elif action in ['create', 'retrieve']:
            permission_classes = [IsAuthenticated]
        elif action in ['update', 'partial_updage', 'destory']:
            permission_classes = [IsOwnerOnly]
        return [permission() for permission in permission_classes]

    @action(detail=True, methods=['get'])
    def get_comment_all(self, request, pk=None):    # Post의 pk값을 가져와서 comment 가져오는 함수
        post = self.get_object()    # 입력받는 값이 없어서 유효성검사 필요 없음. object가 없는 경우는 get_object가 걸러주니까
        comment_all = post.comment_set.all()  # comment에서 post의 related_name 안정한 경우 이렇게 부르면 된대
        serializer = CommentListModelSerializer(comment_all, many=True)
        return Response(serializer.data)



class CommentModelViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentHyperlinkedModelSerializer

@api_view()
def calculator(request):
    # 1. 데이터 확인
    num1 = request.GET.get('num1', 0)
    num2 = request.GET.get('num2', 0)
    operators = request.GET.get('operators')

    # 2. 계산
    if operators == '+':
        result = int(num1) + int(num2)
    elif operators == '-':
        result = int(num1) - int(num2)
    elif operators == '*':
        result = int(num1) * int(num2)
    elif operators == '/':
        result = int(num1) / int(num2)
    else:
        result = 0

    # 3. 응답
    data = {
        'type' : 'FBV', # 함수기반 view라고 명시해줄라고 FBV
        'result' : result,

    }
    return Response(data)    # DRF에서 제공해주는 API. Dictionary 형태로 넣어주면 됨


# APIView 상속받아서 class 기반 Calculator 기능 만들어보기
class CalculatorAPIView(APIView):
    def get(self, request): # 클래스 기반으로 만들때(CBV)는 get 요청을 어떻게 처리할지 이해가 있어야 함. get 함수 만들면 됨
        # get요청을 받으면 이렇게 알아서 get함수 타게 해놨나봐
        # class에 있는 함수는 무조건 self 가져야 된대
        # 1. 데이터 확인
        num1 = request.GET.get('num1', 0)
        num2 = request.GET.get('num2', 0)
        operators = request.GET.get('operators')

        # 2. 계산
        if operators == '+':
            result = int(num1) + int(num2)
        elif operators == '-':
            result = int(num1) - int(num2)
        elif operators == '*':
            result = int(num1) * int(num2)
        elif operators == '/':
            result = int(num1) / int(num2)
        else:
            print('error')
            result = 0

        # 3. 응답
        data = {
            'type' : 'CBV', # 클래스 기반 view라고 명시해줄라고 CBV
            'result' : result,

        }
        return Response(data)
    
    def post(self, request):
        data = {
            'type' : 'CBV',
            'method' : 'POST',
            'result' : 0,

        }
        return Response(data)

# frontapp 열려고 해봄. 그냥 html 파일 열고 들어가면 No 'Access-Control-Allow-Origin' header is present on the requested resource. error 생겨서
# 근데 이렇게 들어가도 결국 local 주소 타고 들어가서 data 불러오는 거라 안되네;; 어케하는거지
#  1. 설치 chrome plugin에서 Allow CORS: Access-Control-Allow-Origin'
#  2. 서버쪽 세팅
# res.setHeader('Access-Control-Allow-origin', '*');
# res.setHeader('Access-Control-Allow-Credentials', 'true'); // 쿠키 주고받기 허용
# res.setHeader('Access-Control-Allow-origin', 'https://inpa.tistory.com');
# 출처: https://inpa.tistory.com/entry/WEB-📚-CORS-💯-정리-해결-방법-👏 [👨‍💻 Dev Scroll]
def post_frontapp(request):
        return render(request, 'frontapp.html')