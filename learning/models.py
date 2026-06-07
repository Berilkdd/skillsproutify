from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class JobRole(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title
    
    def clean(self):
        #Check the quantity before save
        if self.user.jobrole_set.count() >= 5 and not self.pk:
            raise ValidationError("You can only have up to 5 roles.")
        
class Resource(models.Model):
    job_role = models.ForeignKey(JobRole, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    def clean(self):
        #Check the quantity before save
        if self.job_role.resource_set.count() >= 5 and not self.pk:
            raise ValidationError("You can only have up to 5 resources.")

class ResourceItem(models.Model):
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    status = models.CharField(max_length=15, default='planted')

    def __str__(self):
        return self.name

    def clean(self):
        if self.resource.resourceitem_set.count() >= 10 and not self.pk:
            raise ValidationError("You can only add up to 10 items.")