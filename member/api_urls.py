from django.urls import path
from . import api_views

urlpatterns = [
    
    path('api/login/', api_views.api_login, name='api_login'),
    path('api/register/', api_views.api_register, name='api_register'),

    path('api/logout/', api_views.api_logout, name='api_logout'),
    path('api/admin/', api_views.api_admin, name='api_admin'),
    path('api/user-delete/', api_views.api_user_delete, name='api_user_delete'),
    path('api/mypage/', api_views.api_mypage, name='api_mypage'),
    path('api/resource/', api_views.your_resource_view, name='api_resource'),
]
