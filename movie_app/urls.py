from django.urls import path
from . import views

app_name = 'movies'

urlpatterns = [
    path('', views.index, name='index'),
    path('search/', views.search_movie, name='search_movie'),
    path('history/clear/', views.clear_history, name='clear_history'),
    path('search/history/<str:movie_name>/', views.search_by_history, name='search_by_history'),
    path('history/delete/<int:search_id>/', views.delete_search, name='delete_search'),
]