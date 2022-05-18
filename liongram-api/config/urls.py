from django.contrib import admin
from django.urls import path, include, re_path

from rest_framework import routers
from posts.views import PostModelViewSet, calculator, CalculatorAPIView, CommentModelViewSet, PostListCreateView, PostRetrieveUpdateView, post_frontapp
from accounts.views import LoginView, login_view

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Snippets API",
        default_version='v1',
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
        ),
    public=True,
    permission_classes=[permissions.AllowAny],
)


router = routers.DefaultRouter()
router.register('posts', PostModelViewSet)  # prefix 뭐시기에 자동 추가된다는건데 뭐라는거야
router.register('comments', CommentModelViewSet)


urlpatterns = [
    path('', include(router.urls)), # 이거 꼭 추가해야 한다는데, 뭔소리지
    path('admin/', admin.site.urls),
    path('login/', LoginView.as_view()),
    # path('login/', login_view),
    path('frontapp/', post_frontapp),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    # path('calculator-fbv/', calculator, name='calculator-fbv'),
    # path('calculator-cbv/', CalculatorAPIView.as_view(), name='calculator-cbv'),
    # path('posts-list/', PostListCreateView.as_view(), name='post-list-create'), # router 없이도 사용 가능
    # path('posts-list/<int:pk>/', PostRetrieveUpdateView.as_view(), name='post-detail'), # router 없이도 사용 가능

]
