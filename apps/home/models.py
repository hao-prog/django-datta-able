# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


# Create your models here.
class Student(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    user_name = models.CharField(max_length=20)
    deleted = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.first_name

    def get_by_id(id):
        return Student.objects.get(pk=id)
    
    def get_students():
        return Student.objects.filter(deleted=False)

    def create(first_name, last_name, user_name):
        std = Student(first_name=first_name, last_name=last_name, user_name=user_name)
        std.clean_fields()
        std.save()

    def update(self, first_name, last_name, user_name):
        self.first_name = first_name
        self.last_name = last_name
        self.user_name = user_name
        self.clean_fields()
        self.save()

    def delete(self):
        self.deleted = True
        self.save()

