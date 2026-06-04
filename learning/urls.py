from django.urls import path
from . import views

urlpatterns = [
    path("roles/", views.selected_roles, name='selected_roles'),
    path('welcome/', views.welcome, name='welcome'),
    path('roles/delete/<int:role_id>/', views.delete_job_role, name='delete_job_role'),
]