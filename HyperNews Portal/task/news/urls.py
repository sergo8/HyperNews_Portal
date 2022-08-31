from django.urls import path, re_path
from . import views


urlpatterns = [
    path('', views.MainPaigeView.as_view(), name='home'),
    path('news/<int:link>/', views.NewsView.as_view()),
    path('news/', views.AllNewsView.as_view(), name='all_news'),
    path('news/create/', views.CreateNewsView.as_view(), name='create')
]