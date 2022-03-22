import uuid
from django.db import models
from django.db.models import Q
from django.core.exceptions import ValidationError


class Subject(models.Model):
    class Meta:
        db_table = "subject"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50)
    avatar = models.CharField(max_length=100)
    description = models.TextField(max_length=1000)
    deleted = models.BooleanField(default=False)

    def get_by_id(id):
        subject = Subject.objects.get(pk=id, deleted=False)
        return subject

    def get_subjects_by(keyword=None):
        condition = Q(deleted=False)
        if keyword:
            keyword_condition = Q(name__icontains=keyword) | Q(description__icontains=keyword)
            condition &= keyword_condition

        return Subject.objects.filter(condition)

    def create(name, avatar, description):
        if Subject.objects.filter(name=name).exists():
            raise ValidationError({'name': 'Name of subject is existed'})
        subject = Subject(
            name=name,
            avatar=avatar,
            description=description,
        )
        subject.clean_fields()
        subject.save()

    def update(self, name, avatar, description):
        if Subject.objects.filter(name=name).exclude(id=self.id).exists():
            raise ValidationError({'name': 'Name of subject is existed'})
        self.name = name
        self.avatar = avatar
        self.description = description
        self.clean_fields()
        self.save()

    def delete(self):
        self.deleted = True
        self.save()
