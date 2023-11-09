from django.urls import path
from . import views  # views 모듈을 가져오기

urlpatterns = [
    path('search/', views.search, name='search'),
    #path('button_law/', views.button_law, name='button_law'),
    #path('button_prec/', views.button_prec, name='button_prec'),
    path('', views.home, name='home'),
    path('searchengine/', views.searchengine, name='searchengine'),
]
