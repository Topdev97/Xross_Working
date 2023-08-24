from django.db import models

# Create your models here.

from customAdmin.models import *
from accounts.models import *

STATUS_CHOICES = (
  (0, 'applicating'),
  (1, 'completed'),
  (2, 'canceled'),
)

class Job(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, default="")
    comment = models.CharField(max_length=99999, default="")
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    
    price_min = models.IntegerField(default=10)
    price_max = models.IntegerField(default=10)
    
    work_at = models.ForeignKey(Prefecture, on_delete=models.CASCADE)
    work_hour = models.ForeignKey(WorkHour, on_delete=models.CASCADE)
    work_type = models.ForeignKey(WorkType, on_delete=models.CASCADE)
    
    applicating_until = models.DateField()
    pj_start_date = models.DateField()
    pj_end_date = models.DateField()
    
    status = models.IntegerField(choices=STATUS_CHOICES, default=0)

    is_active = models.BooleanField(default=False)
    last_message_at = models.DateTimeField(auto_now=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



class JobSkill(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)

    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)


class JobEmployeeMessageHistory(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)


class JobFavourite(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)


class JobLike(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
