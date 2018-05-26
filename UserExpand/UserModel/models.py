# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin
from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    desc = models.TextField()
    manager = models.CharField(max_length=255,blank=True, null=True, default="",)
    phone = models.CharField(max_length=13,blank=True, null=True, default="",)
    def __str__(self):
        return self.username,self.email,self.phone,self.manager,self.is_active,self.is_staff,self.is_superuser

class UserAdmin(admin.ModelAdmin):
    list_display = ('username','email','phone','manager','is_active','is_staff','is_superuser')
    