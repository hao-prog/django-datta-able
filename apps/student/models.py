import uuid
from django.db import models
from django.db.models import Q
from core.settings import DATE_INPUT_FORMATS
from django.core.exceptions import ValidationError


class Student(models.Model):
    class Meta:
        db_table = "student"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=10, default="1800")
    avatar = models.CharField(max_length=100, blank=True, null=True)
    address = models.CharField(max_length=50)
    phone = models.CharField(max_length=11)
    birthday = models.DateField()
    description = models.TextField(max_length=1000, blank=True, null=True)
    specialized = models.CharField(max_length=10)
    deleted = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.name

    def get_by_id(id):
        student = Student.objects.get(pk=id, deleted=False)
        student.birthday = student.birthday.strftime(DATE_INPUT_FORMATS)
        return student

    def get_students_by(keyword=None, birthday=None, code=None):
        condition = Q(deleted=False)
        if keyword:
            keyword_condition = Q(name__icontains=keyword) | Q(
                description__icontains=keyword
            )
            condition &= keyword_condition
        if birthday:
            condition &= Q(birthday=birthday)
        if code:
            condition &= Q(code__icontains=code)
        return Student.objects.filter(condition)

    def create(name, code, avatar, address, phone, birthday, specialized, description):
        if Student.objects.filter(code=code, deleted=False).exists():
            raise ValidationError({"code": "Student code is existed"})
        student = Student(
            name=name,
            code=code,
            avatar=avatar,
            address=address,
            phone=phone,
            birthday=birthday,
            specialized=specialized,
            description=description,
        )
        student.clean_fields()
        student.save()

    def update(
        self, name, code, avatar, address, phone, birthday, specialized, description
    ):
        if Student.objects.filter(code=code).exclude(id=self.id).exists():
            raise ValidationError({"code": "Student code is existed"})
        self.name = name
        self.code = code
        self.avatar = avatar
        self.address = address
        self.phone = phone
        self.birthday = birthday
        self.specialized = specialized
        self.description = description
        self.clean_fields()
        self.save()

    def delete(self):
        self.deleted = True
        self.save()
