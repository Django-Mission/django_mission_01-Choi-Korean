"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from unicodedata import name
from django.contrib import admin
from django.conf import settings        # conf를 하면 settings에서 지정해놓은 값들(변수?) 다 가져올 수 있음
from django.conf.urls.static import static
from django.urls import path, include
from posts.views import class_view, function_list_view, function_view, url_view, url_parameter_view, index

urlpatterns = [
    path('admin/', admin.site.urls),
    path('url/', url_view),
    path('url/<str:username>/', url_parameter_view), # username처럼 변수명을 넣어서, 해당 변수 받아서 view에 전달 가능
    path('fbv/', function_view),
    path('cbv_view', class_view.as_view()),  # 함수가 아닌, 클래스이기에 as_view()로 호출해야 함
    path('fbv/list/', function_list_view),
    path('', index, name='index'),
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('posts/', include('posts.urls', namespace='posts')),
    # path('__debug__/', include('debug_toolbar.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)    # settings에 만들어놓은 media 변수 urlpattern에 추가