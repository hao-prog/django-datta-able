import os
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.shortcuts import redirect, render
from apps.teacher.models import Teacher
from django.core.files.storage import FileSystemStorage
from core.settings import DATE_INPUT_FORMATS


# @login_required(login_url="/login/")
def teacher(request):
    teachers = Teacher.get_teachers()
    context = {"data": teachers}
    return render(request, "teacher/ui-teachers.html", context)

def teacher_add_ui(request):
    return render(request, "teacher/ui-teacher-add.html")

def teacher_add(
    request,
    name_value,
    avatar_value,
    address_value,
    phone_value,
    birthday_value,
    specialized_value,
    description_value,
    uploaded_file,
    file_path_tmp,
    avatar_tmp_value,
    context,
    folder = 'teacher/',
):
    fs = FileSystemStorage()

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
        if uploaded_file:
            if fs.exists(file_path_tmp):
                fs.delete(file_path_tmp)
            fs.save("tmp/teacher/" + uploaded_file.name, uploaded_file)

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