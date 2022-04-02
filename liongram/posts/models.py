from pyexpat import model
from statistics import mode
from tkinter import CASCADE
from django.db import models
from django.contrib.auth import get_user_model  # 장고(인증시스템)에서 사용하고 있는 유저모델

User = get_user_model()

# Create your models here.

# 게시글 클래스
class Post(models.Model):
    image = models.ImageField(verbose_name='이미지', null=True, blank=True) # verbose_name : 관리자나 폼 등 일반 사용자쪽 페이지에 노출될 필드에 대한 이름 지정
    content = models.TextField(verbose_name='내용')
    created_at = models.DateTimeField(verbose_name='작성일', auto_now_add=True) # 게시글 작성시 자동 날짜 입력
    view_count = models.IntegerField(verbose_name='조회수', default=0)
    writer = models.ForeignKey(to=User, on_delete=models.CASCADE, null=True, blank=True)

# 댓글 클래스. 클래스는 객체. 저 Model 클래스를 상속받은 Comment 클래스 생성하는 것
# django에서 만든 Model 클래스에는 db와 연결하는 많은 함수들이 있고, 이를 상속 받은 Comment 클래스에 모델링하면 db에 테이블로 만들어지는 것
class Comment(models.Model):
    content = models.TextField(verbose_name='내용')
    created_at = models.DateTimeField(verbose_name='작성일')
    post = models.ForeignKey(to='Post', on_delete=models.CASCADE)   # 게시글 foreignKey 연결. 게시글이 삭제되면 댓글도 삭제되게 on_delete에 CASCADE 설정
    writer = models.ForeignKey(to=User, on_delete=models.CASCADE) # 사용자 연결. 장고에서 만든 사용자 모델 연결