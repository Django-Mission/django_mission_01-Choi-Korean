from django.urls import URLPattern, path
from .views import post_create_form_view, post_list_view, post_create_view, post_detail_view, post_delete_view, post_update_view
from django.conf import settings        # conf를 하면 settings에서 지정해놓은 값들(변수?) 다 가져올 수 있음
from django.conf.urls.static import static

app_name = 'posts'

urlpatterns = [
    path('', post_list_view, name='post-list'),
    # path('create/', post_create_view, name='post-create'),    # post_create_form_view 보기 위해 임시 주석처리
    path('create/', post_create_form_view, name='post-create'),
    path('<int:id>/', post_detail_view, name='post-detail'),    # id값을 받았을때 상세정보 보여주기
    path('<int:id>/edit/', post_update_view, name='post-update'), # id edit으로 들어오면 update 페이지
    path('<int:id>/delete/', post_delete_view, name='post-delete'),  
]

# urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFIELS_DIRS)    # settings에 만들어놓은 static 변수 urlpattern에 추가
