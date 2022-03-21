import uuid
from django.db import models

from core.settings import DATE_INPUT_FORMATS


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

    def get_subjects():
        return Subject.objects.filter(deleted=False)

    def create(name, avatar, description):
        subject = Subject(
            name=name,
            avatar=avatar,
            description=description,
        )
        subject.clean_fields()
        subject.save()

    def update(self, name, avatar, description):
        self.name = name
        self.avatar = avatar
        self.description = description
        self.clean_fields()
        self.save()

    def delete(self):
        self.deleted = True
        self.save()
