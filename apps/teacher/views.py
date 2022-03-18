import os
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.shortcuts import redirect, render
from apps.teacher.models import Teacher
from django.core.files.storage import FileSystemStorage
from core.settings import DATE_INPUT_FORMATS, MEDIA_FOLDER_PATH_STUDENT


def teacher(request):
    teachers = Teacher.get_teachers()
    context = {"data": teachers}
    return render(request, "teacher/ui-teachers.html", context)


def teacher_add_ui(request):
    return render(request, "teacher/ui-teacher-add.html")


def teacher_add(request):
    fs = FileSystemStorage()
    folder_path = MEDIA_FOLDER_PATH_STUDENT + "teacher/"
    context = {}

    name_value = request.POST.get("name")
    address_value = request.POST.get("address")
    phone_value = request.POST.get("phone")
    birthday_value = request.POST.get("birthday")
    specialized_value = request.POST.get("specialized")
    description_value = request.POST.get("description")
    avatar_tmp = request.POST.get("avatar_tmp")  # old avatar_tmp

    avatar_tmp_value = avatar_tmp  # new avatar_tmp
    avatar_value = avatar_tmp or ""
    file_path_tmp = "tmp/teacher/" + avatar_tmp

    try:
        teacher = Teacher(
            name=name_value,
            avatar=avatar_value,
            address=address_value,
            phone=phone_value,
            birthday=birthday_value,
            specialized=specialized_value,
            description=description_value,
        )
        teacher.clean_fields()
        if "avatar" in context:
            raise ValidationError({})
    except ValidationError as e:
        if teacher.birthday:
            teacher.birthday = teacher.birthday.strftime(DATE_INPUT_FORMATS)

        context.update(
            {
                "name_value": name_value,
                "avatar_value": avatar_value,
                "address_value": address_value,
                "phone_value": phone_value,
                "birthday_value": birthday_value,
                "specialized_value": specialized_value,
                "description_value": description_value,
                "avatar_tmp": avatar_tmp_value,
            }
        )
        context = {**context, **dict(e)}
        return render(request, "teacher/ui-teacher-add.html", context)

    Teacher.create(
        name=name_value,
        avatar=avatar_value,
        address=address_value,
        phone=phone_value,
        birthday=birthday_value,
        specialized=specialized_value,
        description=description_value,
    )
