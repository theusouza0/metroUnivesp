from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('fetch-html/', views.fetch_html, name='fetch_html'),
]