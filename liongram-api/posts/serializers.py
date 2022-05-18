from dataclasses import fields
from rest_framework.serializers import ModelSerializer, HyperlinkedModelSerializer
from .models import Post, Comment

class PostBaseModelSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'

class PostListModelSerializer(PostBaseModelSerializer): # PostBaseModelSerializer를 상속받게 해서 특정 field만 지우기
    class Meta(PostBaseModelSerializer.Meta):   # Meta도 마찬가지로 상위 class의 Meta 상속 받아야 함
        fields = ['id', 'image', 'content', 'created_at', 'view_count', 'writer']
        depth = 1   # 원래는 writer(user)의 id값만 불러오는데, depth 설정하면, 해당 user의 모든 정보 다 불러옴. 이거 이용해서 댓글도 같이 보여줄 수 있음
        # exclude = ['content', ]        

class PostCreateModelSerializer(PostBaseModelSerializer):
    class Meta(PostBaseModelSerializer.Meta):   # Create에 필요한 fields만 집어넣기
        fields = ['image', 'content']

class PostDeleteModelSerializer(PostBaseModelSerializer):
    pass

class CommentHyperlinkedModelSerializer(HyperlinkedModelSerializer):   # HyperlinkedModelSerializer 이용해서 만들어보기. 근데 지금 user-detail이 없어서 안됨. 나중에 다시 한대
    class Meta:
        model = Comment
        fields = '__all__'


class PostRetrieveModelSerializer(PostBaseModelSerializer):
    class Meta(PostBaseModelSerializer.Meta):
        depth = 1

class CommentListModelSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'