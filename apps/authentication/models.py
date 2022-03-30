# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

import uuid

from django.core.exceptions import ValidationError
from apps.student.models import Student
from apps.teacher.models import Teacher
from django.db import models
from django.contrib.auth.hashers import make_password

# Create your models here.
class Account(models.Model):
    class Meta:
        db_table = "account"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=128)
    is_admin = models.BooleanField(default=False)
    deleted = models.BooleanField(default=False)

    def get_by(username, password):
        try:
            encoded_password = make_password(
                password=password, salt="salt", hasher="pbkdf2_sha256"
            )
            account = Account.objects.get(username=username, password=encoded_password)
        except Exception:
            account = None
        return account

    def create(username, password1, password2, is_admin=True):
        if Account.objects.filter(username=username).exists():
            raise ValidationError({"username": "Username is existed"})
        if password1 is None or password1 == "":
            raise ValidationError({"password1": "Password cannot be blank"})
        if password1 != password2:
            raise ValidationError({"password2": "Password does not match"})
        account = Account(
            username=username,
            password=make_password(
                password=password1, salt="salt", hasher="pbkdf2_sha256"
            ),
            is_admin=is_admin,
        )
        account.clean_fields()
        account.save()
