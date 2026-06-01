from django.urls import path
from . import views

urlpatterns = [
    path("first-role/", views.first_role, name='first_role'),
    path("roles/", views.selected_roles, name='selected_roles'),
    path('welcome/', views.welcome, name='welcome'),
]