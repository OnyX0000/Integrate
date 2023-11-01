from django.urls import include
from django.urls import path
from django.contrib import admin
from allauth.socialaccount.providers.oauth2.urls import default_urlpatterns
from allauth.socialaccount import views as socialaccount_views
from member import views
from member.views import mypage
from member.views import CustomAuthToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
# from member.views import ChatbotView
# from member.views import LegalQAFinalViewSet

urlpatterns = [
    # 빈 경로에 대한 URL 패턴 추가
    path('', views.home, name='home'),

    # 회원가입 기능
    path('register/', views.register, name='register'),

    # 회원 관리자 페이지
    path('user_admin/', views.user_admin, name='user_admin'),

    # 로그인 기능
    path('login/', views.user_login, name='login'),
    path('login/', CustomAuthToken.as_view(), name='custom_auth_token'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # 로그아웃 기능
    path('logout/', views.user_logout, name='logout'),

    # 관리자 페이지
    path('admin/', admin.site.urls),

    # fix need
    path('messages/', views.messsages, name='messages'),

    path('button_law/', views.button_law, name='button_law'),

    path('button_prec/', views.button_prec, name='button_prec'),
    
    #챗봇
    path('chatbot/', views.chatbot, name='chatbot'),

    # 마이페이지
    path('mypage/', mypage, name='mypage'),

    # 회원탈퇴
    path('user-delete/', views.user_delete, name='user_delete'),

    # #구글로그인
    # path('welcome/', views.welcome, name='welcome'),
    # 소셜 로그인 기능
    # path('accounts/kakao/login/callback/', views.social_login, name='social_login'),
    # path('accounts/', include('allauth.urls')),

]

# 로그인 성공 시 홈 화면으로 리다이렉트하는 URL 패턴 추가
urlpatterns += [
    path('home/', views.home, name='home_redirect'),
]
