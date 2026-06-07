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