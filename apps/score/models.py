# import uuid
# from django.db import models

# from core.settings import DATE_INPUT_FORMATS


# class Score(models.Model):
#     class Meta:
#         db_table = "student"

#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     name = models.CharField(max_length=50)
#     avatar = models.CharField(max_length=100)
#     address = models.CharField(max_length=50)
#     phone = models.CharField(max_length=11)
#     birthday = models.DateField()
#     description = models.TextField(max_length=1000)
#     specialized = models.CharField(max_length=10)
#     deleted = models.BooleanField(default=False)

#     # def __init__(self, *args, **kwargs) -> None:
#     #     super().__init__(*args, **kwargs)
#     #     self.specialized = SPECIALIZED_ARR[self.specialized]

#     def __str__(self) -> str:
#         return self.name

#     def get_by_id(id):
#         student = Score.objects.get(pk=id, deleted=False)
#         student.birthday = student.birthday.strftime(DATE_INPUT_FORMATS)
#         return student

#     def get_students():
#         return Score.objects.filter(deleted=False)

#     def create(name, avatar, address, phone, birthday, specialized, description):
#         student = Score(
#             name=name,
#             avatar=avatar,
#             address=address,
#             phone=phone,
#             birthday=birthday,
#             specialized=specialized,
#             description=description,
#         )
#         student.clean_fields()
#         student.save()

#     def update(self, name, avatar, address, phone, birthday, specialized, description):
#         self.name = name
#         self.avatar = avatar
#         self.address = address
#         self.phone = phone
#         self.birthday = birthday
#         self.specialized = specialized
#         self.description = description
#         self.clean_fields()
#         self.save()

#     def delete(self):
#         self.deleted = True
#         self.save()
