from django.contrib import admin
from .models import JobRole, Resource, ResourceItem

@admin.register(JobRole)
class JobRoleAdmin(admin.ModelAdmin):
    list_display = ('user', 'title')
    search_fields = ('user__username', 'title')

@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ('job_role', 'name')
    search_fields = ('job_role__title', 'name')

@admin.register(ResourceItem)
class ResourceItemAdmin(admin.ModelAdmin):
    list_display = ('resource', 'name', 'status')
    search_fields = ('resource__name', 'name')