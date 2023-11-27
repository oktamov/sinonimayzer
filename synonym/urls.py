from django.urls import path

from synonym import views

urlpatterns = [
    path('', views.index, name='index'),
    path('check/', views.check, name='check'),
    path('words/', views.view_words, name='view_words'),
]
