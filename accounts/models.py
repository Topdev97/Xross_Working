from django.contrib.auth.models import AbstractUser as BaseUser
from django.db import models

from customAdmin.models import *

STATUS_CHOICES = (
    (1, 'Register'),
    (2, 'Normal'),
    (3, 'Block Bid'),
    (4, 'Block Account'),
)

USER_TYPE_CHOICES = (
    ("employee", 'employee'),
    ("employer", 'employer'),
)

class User(BaseUser):
    avatar = models.CharField(max_length=50, default="default.png")
    first_name_hiragana = models.CharField(max_length=50, default="")
    last_name_hiragana = models.CharField(max_length=50, default="")
    prefecture = models.ForeignKey(Prefecture, on_delete=models.CASCADE, null=True)
    address = models.CharField(max_length=50, default="")
    phone = models.CharField(max_length=50, default="")
    birthday = models.DateField(auto_now=True)
    status = models.PositiveSmallIntegerField(choices=STATUS_CHOICES, default=1)    
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default="employer")
    points = models.IntegerField(default=10)
    paypoints = models.IntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    


class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    feature_image = models.CharField(max_length=100, default="default.png")
    role = models.CharField(max_length=50, default="フリーランサー")
    intro = models.CharField(max_length=500, default="")

    personal_url = models.URLField(default="")
    facebook_url = models.URLField(default="")
    twitter_url = models.URLField(default="")
    github_url = models.URLField(default="")
    
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    

class Employer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    feature_image = models.CharField(max_length=100, default="default.png")
    company_name = models.CharField(max_length=50, default="株式会社")
    publish_at = models.DateField(auto_now=True)
    seo_name = models.CharField(max_length=100, default="")
    intro = models.CharField(max_length=500, default="")
    address = models.CharField(max_length=500, default="")

    google_map_url = models.URLField(max_length=3000, default="")
    company_url = models.URLField(default="")
    facebook_url = models.URLField(default="")
    twitter_url = models.URLField(default="")
    github_url = models.URLField(default="")

    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

class Email(models.Model):

    when = models.DateTimeField(null=False, auto_now_add=True)
    to = models.EmailField(null=False, blank=False,)
    subject = models.CharField(null=False, max_length=128,)
    body = models.TextField(null=False, max_length=1024,)
    ok = models.BooleanField(null=False, default=True,)
    
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)