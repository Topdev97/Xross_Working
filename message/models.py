from django.db import models

# Create your models here.

from customAdmin.models import *
from accounts.models import *
from job.models import *
from proposal.models import *

class JobMessage(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sender")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="receiver")
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    message = models.CharField(max_length=99999, default="")
    
    receiver_readed = models.BooleanField(default=False)
    sender_readed = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class AttachmentFile(models.Model):
    message = models.OneToOneField(JobMessage, on_delete=models.CASCADE)
    name = models.CharField(max_length=99999, default="")
    storage_id = models.CharField(max_length=100)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)