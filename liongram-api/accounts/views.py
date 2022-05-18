from django.shortcuts import render
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView

from accounts.serializers import LoginSerializers, Tokenserializers

# Create your views here.

@api_view(['POST'])
# @authentication_classes([SessionAuthentication, BasicAuthentication]) # 이렇게 인증방식 바꿀 수 있음
@permission_classes([AllowAny])    # 권한방식도 바꿀 수 있음. login은 누구나 들어와야 하기에 AllowAny로. header에만 token 담아주면 login 할 수 있음
@swagger_auto_schema(request_body=LoginSerializers, responses={200: Tokenserializers}) # 상태값일때(200) : Serializer 쓸거다 알려주는 것
def login_view(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user:
        token, _ = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})
    else:
        return Response(status=401)

class LoginView(APIView):   # 위 함수형이 안되어서 우선 class 기반으로 다시 작성해봄. 이건 정상 작동

    permission_classes = AllowAny
    @swagger_auto_schema(request_body=LoginSerializers, responses={200: Tokenserializers})
    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key})
        else:
            return Response(status=401)