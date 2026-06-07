from django.urls import path
from . import views

urlpatterns = [
    path("roles/", views.selected_roles, name='selected_roles'),
    path('welcome/', views.welcome, name='welcome'),   
    path('learning-delete/<str:item_type>/<int:item_id>/', views.delete_item, name='delete_item'),    
    path('roles/<int:role_id>/resources/', views.role_resources, name='role_resources'),
]