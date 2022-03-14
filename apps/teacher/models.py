import uuid
from django.db import models


class Teacher(models.Model):
    class Meta:
        db_table = "teacher"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50)
    avatar = models.CharField(max_length=100)
    address = models.CharField(max_length=50)
    phone = models.CharField(max_length=11)
    birthday = models.DateField()
    description = models.TextField(max_length=1000)
    specialized = models.CharField(max_length=10)
    degree = models.CharField(max_length=10)
    deleted = models.BooleanField(default=False)