from django.contrib import admin
from django.urls import path, include

from . import views as v

app_name = 'blog'

urlpatterns = [
    path('', v.IndexView.as_view(), name='index'),
    path('article/<str:slug>/', v.ArticleView.as_view(), name='detail'),
    path('category/<int:pk>/', v.CategoryView.as_view(), name='category'),
    path('tag/<int:pk>/', v.TagView.as_view(), name='tag'),
]
