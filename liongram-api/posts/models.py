from django.db import models
from django.contrib.auth import get_user_model  # 장고(인증시스템)에서 사용하고 있는 유저모델

User = get_user_model()

# Create your models here.

# liongram posts model 그대로 가져옴
# 근데 얘는 serializers에 추가해줘야 된대. serializers.py에 추가헀음
class Post(models.Model):
    image = models.ImageField(verbose_name='이미지', null=True, blank=True)
    content = models.TextField(verbose_name='내용')
    created_at = models.DateTimeField(verbose_name='작성일', auto_now_add=True)
    view_count = models.IntegerField(verbose_name='조회수', default=0)
    writer = models.ForeignKey(to=User, on_delete=models.CASCADE, null=True, blank=True)

class Comment(models.Model):
    content = models.TextField(verbose_name='내용')
    created_at = models.DateTimeField(verbose_name='작성일', auto_now_add=True)
    post = models.ForeignKey(to='Post', on_delete=models.CASCADE)
    writer = models.ForeignKey(to=User, on_delete=models.CASCADE)
