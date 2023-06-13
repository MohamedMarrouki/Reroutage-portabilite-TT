from django.urls import path
from . import views

urlpatterns = [
    path('aaa', views.home, name='home')
]
