from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'), 
    path('login-redirect/', views.login_redirect, name='login_redirect'),   
]
