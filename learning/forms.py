from django import forms
from .models import JobRole

class JobRoleForm(forms.ModelForm):
    class Meta:
        model = JobRole
        fields = ('title',)
        