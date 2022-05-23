from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []  # 도메인, IP. 예로 네이버면 'naver.com'
# production 올려서 실제 ip주소 얻으면, 그거 써주면 됨

DJANGO_APPS += []

PROJECT_APPS += []

THIRD_PARTY_APPS += [
    'debug_toolbar',
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


# DEBUG가 True면, static_ROOT가 아닌 STATICFIELS_DIRS로 해야 한대
STATICFILES_DIRS = [    
    BASE_DIR / 'static'
]

# STATIC_ROOT= BASE_DIR / 'static'