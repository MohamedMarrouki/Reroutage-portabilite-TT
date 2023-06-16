from django.urls import path
from . import views

urlpatterns = [
    path('home', views.home, name='home'),
    path('upload',views.send_files,name='upload'),
    path('chart',views.chart,name='chart')
]
