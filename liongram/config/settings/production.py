from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['54.180.104.141']  # 도메인, IP. 예로 네이버면 'naver.com'
# production 올려서 실제 ip주소 얻으면, 그거 써주면 됨

DJANGO_APPS += []

PROJECT_APPS += []

THIRD_PARTY_APPS += [
]

INSTALLED_APPS = DJANGO_APPS + PROJECT_APPS + THIRD_PARTY_APPS

# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {   # 현재는 mysql쓰지만, oracle 뭐 이렇게 바뀌면 바꿔줭 ㅑ한대
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# 배포할 때는 STATICFILES_DIRS이 아닌 ROOT로. 배열도 아니고 문자열 하나로
# 실제 static 파일 있는 곳 한군데 정확히 기재해야 한대 production에서는
STATIC_ROOT= BASE_DIR / 'static'