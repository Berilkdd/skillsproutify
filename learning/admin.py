from django.contrib import admin
from .models import JobRole

@admin.register(JobRole)
class JobRoleAdmin(admin.ModelAdmin):
    list_display = ('user', 'title')
    search_fields = ('user__username', 'title')