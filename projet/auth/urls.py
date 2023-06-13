from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home1'),
    path('login', views.loginn, name='login'),
    path('register', views.register, name='register'),
    path('logout', views.log_out, name='log_out'),
]