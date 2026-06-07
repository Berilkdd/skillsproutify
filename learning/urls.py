from django.urls import path
from . import views

urlpatterns = [
    path('welcome/', views.welcome, name='welcome'),   
    path("roles/", views.selected_roles, name='selected_roles'),
    path('<int:role_id>/', views.role_resources, name='role_resources'),
    path('items/<int:resource_id>/', views.resource_items, name='resource_items'),
    path('learning-delete/<str:item_type>/<int:item_id>/', views.delete_item, name='delete_item'), 
]