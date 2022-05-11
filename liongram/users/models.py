from tkinter import CASCADE
from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager as DjangoUserManager


# Create your models here.

# manager : django 모델이 db로 쿼리를 날릴떄 제공해주는 interface
# 일반유저와 super 유저를 작성하는데 차이가 있어서 이걸 좀 다르게 구성해야 한대. 둘다 _create_user 함수로 create하긴 함
# is_superuser, is_staff fields가 super user는 모두 True여야 해서
class UserManager(DjangoUserManager):
    def _create_user(self, username, email, password, **extra_fields):  # 앞에 _ 쓰는거는 외부에 유출하지 않고 내부에서만 쓰는(숨기기 위한) 용도로 명시
        if not email:   # email 꼭 받아야 하면 이렇게
            raise ValueError("이메일은 필수 값입니다.")
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password) # set_password로 받는 이유 : hashing처리해서 문자열을 암호화하기 위해. db에 사용자 pw 그대로 넣으면 안되어서
        user.save(using=self.db)
        return user

    def create_user(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, email, password, **extra_fields)   # 들어온거 그대로 넣고, extra_fields만 설정해서 _create_user 함수로 return

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(username, email, password, **extra_fields)


# 다양한 user모델이 있는데, 보통 AbstractUser 많이 상속 받아서 customizing 한대
#AbstractUser에는 이미 많은 field가 있기에 추가되어 있음. 거기에 phone이 없었어서 phone만 추가한거
class User(AbstractUser):
    phone = models.CharField(verbose_name="전화번호", max_length=11)
    objects = UserManager() # 장고 user에 연결시켜줘야 제대로 작동. 연결안하면 그냥 개별 모델이 되는 거래.
    # 이제 이걸 나중에 User.Objects.UserManager() 이렇게 사용할거래 ㅇㅎ


# 기본 User 정보에서 추가로 확장해야할 정보가 있을때, 이런식으로 해주면 됨
# 그래서 기본적 데이터는 User에 넣고, 자주는 쓰지만 항상 들어가는건 아니면 이렇게 확장으로 뺄 수도 있대.
# 데이터의 성질 특징에 따라서 별도로 관리할때가 있대.
# class UserInfo(models.Model):
#     phone_sub = models.CharField(verbose_name='보조 전화번호', max_length=11)
#     user = models.ForeignKey(to='User', on_delete=models.CASCADE)

