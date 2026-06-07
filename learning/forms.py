from django import forms
from .models import JobRole, Resource

class JobRoleForm(forms.ModelForm):
    class Meta:
        model = JobRole
        fields = ('title',)
        
class ResourceForm(forms.ModelForm):
    class Meta:
        model = Resource
        fields = ('name',)