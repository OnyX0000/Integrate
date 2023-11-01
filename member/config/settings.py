from pathlib import Path
import os

DEFAULT_CHARSET = 'utf-8'
FILE_CHARSET = 'utf-8'

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-u#(fgp7hh6tk+7b*zfe63ceiz_pd58scss($1=8_@2ld25u!+&'

DEBUG = True

ALLOWED_HOSTS = ['*']

# static directory 등록
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.sites',
    'django.contrib.staticfiles',
    'member',
    'rest_framework',
    'rest_framework.authtoken',
    'rest_framework_simplejwt',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.kakao',
    # 'config',
]

SITE_ID = 1

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# 추가된 설정: 데이터베이스 설정
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# 추가된 설정: 인증 백엔드 지정
AUTHENTICATION_BACKENDS = [
    'member.backends.EmailBackend',  # 이메일을 사용한 인증을 위한 사용자 정의 인증 백엔드 추가
    'django.contrib.auth.backends.ModelBackend',  # Django 기본 인증 백엔드 유지
    # 'allauth.account.auth_backends.AuthenticationBackend',
    # 'allauth.socialaccount.auth_backends.AuthenticationBackend',
    # 'social_core.backends.kakao.KakaoOAuth2',
]

# 추가된 설정: 비밇번호 유효성 검사
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

#추가된 설정: 소셜로그인
SOCIALACCOUNT_PROVIDERS = {
    'kakao': {
        'APP': {
            'client_id': 'b77994182d3e8dd5d7136f164e0ca7bb',
            'secret': 'QNG2tJLO9ZEEJ4jJXOUAa9HVmxqfa3PJ',
            'redirect_uri': 'http://127.0.0.1:8000/accounts/kakao/login/callback/',
        },
        'SCOPE': ['profile', 'account_email'], 
    }
}

# # 추가된 설정: 토큰 발급 restframework
# REST_FRAMEWORK = {
#     'DEFAULT_AUTHENTICATION_CLASSES': [
#         'rest_framework.authentication.TokenAuthentication',
#     ],
#     'DEFAULT_PERMISSION_CLASSES': (
#         'rest_framework.permissions.IsAuthenticated',
#     )
# }

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (

        'rest_framework_simplejwt.authentication.JWTAuthentication',
    )
}


#추가된 설정: 포스트맨 쿠키
CSRF_COOKIE_NAME = "csrftoken"
CSRF_COOKIE_HTTPONLY = False

LOGIN_URL = 'login'

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

SOCIALACCOUNT_LOGIN_ON_GET = True
LOGIN_REDIRECT_URL = 'home'
ACCOUNT_LOGOUT_REDIRECT_URL = 'home'
ACCOUNT_LOGOUT_ON_GET = True

STATIC_URL = '/static/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CORS_ALLOW_ALL_ORIGINS = True # 다른 도메인에서 API 접근 허용

CSRF_COOKIE_SECURE = True
CSRF_COOKIE_SAMESITE = 'Lax'  # 또는 'Strict'

CSRF_TRUSTED_ORIGINS = ["http://127.0.0.1:8000"]


APPEND_SLASH = False

# CSRF_COOKIE_SECURE = False
# CSRF_USE_SESSIONS = False