from django.db import models

# Create your models here.

class Prefecture(models.Model):
    name = models.CharField(max_length=50, default="", unique=True)
    display_order = models.IntegerField(default=1)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Category(models.Model):
    name = models.CharField(max_length=50, default="", unique=True)
    display_order = models.IntegerField(default=1)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)


class WorkHour(models.Model):
    name = models.CharField(max_length=50, default="", unique=True)
    display_order = models.IntegerField(default=1)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

class WorkType(models.Model):
    name = models.CharField(max_length=50, default="", unique=True)
    display_order = models.IntegerField(default=1)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

class Skill(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, default="", unique=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)