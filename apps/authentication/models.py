# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

import uuid
from apps.student.models import Student
from apps.teacher.models import Teacher
from django.db import models

# Create your models here.
class Account(models.Model):
    class Meta:
        db_table = "account"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    student = models.OneToOneField(
        Student, on_delete=models.CASCADE, default=None, blank=True, null=True
    )
    teacher = models.OneToOneField(
        Teacher, on_delete=models.CASCADE, default=None, blank=True, null=True
    )
    is_admin = models.BooleanField(default=False)
    deleted = models.BooleanField(default=False)

    def get_by(username, password):
        try:
            account = Account.objects.get(username=username, password=password)
        except Exception:
            account = None
        return account