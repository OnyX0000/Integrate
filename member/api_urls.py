from django.urls import path
from . import api_views

urlpatterns = [
    # 토큰 발급
    path('api/login/', api_views.custom_auth_token, name='api_login'),

    # 토큰 유효성 검증
    path('api/validate-token/', api_views.validate_token, name='api_validate_token'),

    # 기본 API 엔드포인트들
    path('api/logout/', api_views.api_logout, name='api_logout'),
    path('api/register/', api_views.api_register, name='api_register'),
    path('api/admin/', api_views.api_admin, name='api_admin'),
    path('api/user-delete/', api_views.api_user_delete, name='api_user_delete'),
    path('api/mypage/', api_views.api_mypage, name='api_mypage'),
    path('api/resource/', api_views.your_resource_view, name='api_resource'),
]
