from django.urls import path
from . import views

urlpatterns = [
    path("roles/", views.selected_roles, name='selected_roles'),
    path('welcome/', views.welcome, name='welcome'),        
    path('roles/<int:role_id>/resources/', views.role_resources, name='role_resources'),
    path('resources/<int:resource_id>/items/', views.resource_items, name='resource_items'),
    path('learning-delete/<str:item_type>/<int:item_id>/', views.delete_item, name='delete_item'), 
]