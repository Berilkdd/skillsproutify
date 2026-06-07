from django import forms
from .models import JobRole, Resource, ResourceItem

class JobRoleForm(forms.ModelForm):
    class Meta:
        model = JobRole
        fields = ('title',)
        
class ResourceForm(forms.ModelForm):
    class Meta:
        model = Resource
        fields = ('name',)

class ResourceItemForm(forms.ModelForm):
    class Meta:
        model = ResourceItem
        fields = ('name',)