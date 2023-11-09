from django.urls import path
from . import views  # views 모듈을 가져오기

urlpatterns = [
    path('search/', views.search, name='search'),
    path('', views.home, name='home'),
    path('searchengine/', views.searchengine, name='searchengine'),
]
