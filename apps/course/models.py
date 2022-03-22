import uuid
from django.db import models
from django.db.models import Q
from apps.subject.models import Subject
from django.core.exceptions import ValidationError


class Course(models.Model):
    class Meta:
        db_table = "course"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    description = models.TextField(max_length=1000)
    deleted = models.BooleanField(default=False)

    def get_by_id(id):
        course = Course.objects.get(pk=id, deleted=False)
        return course

    def get_courses_by(keyword=None):
        condition = Q(deleted=False)
        if keyword:
            keyword_condition = Q(name__icontains=keyword) | Q(
                description__icontains=keyword
            )
            condition &= keyword_condition

        return Course.objects.filter(condition)

    def create(name, subject, description):
        if Course.objects.filter(name=name).exists():
            raise ValidationError({"name": "Name of course is existed"})
        course = Course(
            name=name,
            subject=subject,
            description=description,
        )
        course.clean_fields()
        course.save()

    def update(self, name, subject, description):
        if Course.objects.filter(name=name).exclude(id=self.id).exists():
            raise ValidationError({"name": "Name of course is existed"})
        self.name = name
        self.subject = subject
        self.description = description
        self.clean_fields()
        self.save()

    def delete(self):
        self.deleted = True
        self.save()
