import uuid
from django.db import models
from django.db.models import Q
from core.settings import DATE_INPUT_FORMATS


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

    def get_by_id(id):
        teacher = Teacher.objects.get(pk=id, deleted=False)
        teacher.birthday = teacher.birthday.strftime(DATE_INPUT_FORMATS)
        return teacher

    def get_teachers_by(keyword=None, specialized=None, birthday=None):
        condition = Q(deleted=False)
        if keyword:
            keyword_condition = Q(name__icontains=keyword) | Q(description__icontains=keyword)
            condition &= keyword_condition
        if specialized:
            condition &= Q(specialized=specialized)
        if birthday:
            condition &= Q(birthday=birthday)

        return Teacher.objects.filter(condition)

    def create(
        name, avatar, address, phone, birthday, specialized, degree, description
    ):
        teacher = Teacher(
            name=name,
            avatar=avatar,
            address=address,
            phone=phone,
            birthday=birthday,
            specialized=specialized,
            degree=degree,
            description=description,
        )
        teacher.clean_fields()
        teacher.save()

    def update(
        self, name, avatar, address, phone, birthday, specialized, degree, description
    ):
        self.name = name
        self.avatar = avatar
        self.address = address
        self.phone = phone
        self.birthday = birthday
        self.specialized = specialized
        self.degree = degree
        self.description = description
        self.clean_fields()
        self.save()

    def delete(self):
        self.deleted = True
        self.save()
