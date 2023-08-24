from django.db import models

from accounts.models import *

# Create your models here.


class JobHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    company = models.CharField(max_length=100, default="")
    role = models.CharField(max_length=100, default="")
    comment = models.CharField(max_length=500, default="")
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField(auto_now_add=True)
    
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    
class UserSkill(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    year = models.IntegerField(default=0)
    
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    