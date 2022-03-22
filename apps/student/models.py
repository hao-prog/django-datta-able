import uuid
from django.db import models
from django.db.models import Q
from core.settings import DATE_INPUT_FORMATS


class Student(models.Model):
    class Meta:
        db_table = "student"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50)
    avatar = models.CharField(max_length=100)
    address = models.CharField(max_length=50)
    phone = models.CharField(max_length=11)
    birthday = models.DateField()
    description = models.TextField(max_length=1000)
    specialized = models.CharField(max_length=10)
    deleted = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.name

    def get_by_id(id):
        student = Student.objects.get(pk=id, deleted=False)
        student.birthday = student.birthday.strftime(DATE_INPUT_FORMATS)
        return student
    
    def get_students_by(keyword=None, birthday=None):
        condition = Q(deleted=False)
        if keyword:
            keyword_condition = Q(name__icontains=keyword) | Q(description__icontains=keyword)
            condition &= keyword_condition
        if birthday:
            condition &= Q(birthday=birthday)

        return Student.objects.filter(condition)

    def create(name, avatar, address, phone, birthday, specialized, description):
        student = Student(
            name=name,
            avatar=avatar,
            address=address,
            phone=phone,
            birthday=birthday,
            specialized=specialized,
            description=description,
        )
        student.clean_fields()
        student.save()

    def update(self, name, avatar, address, phone, birthday, specialized, description):
        self.name = name
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
