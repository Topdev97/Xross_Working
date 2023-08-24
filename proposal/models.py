from django.db import models

# Create your models here.

from customAdmin.models import *
from accounts.models import *
from job.models import *

STATUS_CHOICES = (
  (0, 'applicating'),
  (1, 'accepted'),
  (2, 'ejected'),
  (3, 'contracted')
)

class Proposal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    comment = models.CharField(max_length=99999, default="")
    
    price = models.IntegerField(default=10)
    
    status = models.IntegerField(choices=STATUS_CHOICES, default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
