from datetime import datetime
import os
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.shortcuts import redirect, render
from apps.student.models import Student
from django.core.files.storage import FileSystemStorage
from core.settings import BASE_DIR, DATE_INPUT_FORMATS


# @login_required(login_url="/login/")
def student(request):
    students = Student.get_students()
    context = {"data": students}
    return render(request, "student/ui-students.html", context)


# @login_required(login_url="/login/")
def student_delete(request):
    id = request.POST.get("student_id")
    std = Student.get_by_id(id)
    std.delete()
    return redirect("/student")


# @login_required(login_url="/login/")
def student_add_ui(request):
    return render(request, "student/ui-student-add.html")


def file_handle():
    def inner(func):
        def wrapper(*args, **kwargs):
            request = args[0]
            allowed_mime_types = ["png", "jpg", "jpeg", "jfif", "pjpeg", "pjp"]
            context = {}
            fs = FileSystemStorage()

            name_value = request.POST.get("name")
            address_value = request.POST.get("address")
            phone_value = request.POST.get("phone")
            birthday_value = request.POST.get("birthday")
            specialized_value = request.POST.get("specialized")
            description_value = request.POST.get("description")

            avatar_tmp = request.POST.get("avatar_tmp")
            avatar_tmp_value = ""
            avatar_value = avatar_tmp or ""
            file_path_tmp = "tmp/student/" + avatar_tmp
            uploaded_file = None

            if "avatar" in request.FILES:
                uploaded_file = request.FILES["avatar"]
                avatar_value = uploaded_file.name
                file_mime = uploaded_file.content_type.split("/")[1]
                if len(allowed_mime_types) > 0:
                    if file_mime not in allowed_mime_types:
                        context["avatar"] = ["File must be an image!"]
                        uploaded_file = None
                    else:
                        file_path_tmp = "tmp/student/" + avatar_value
                        avatar_tmp_value = avatar_value
                        file_path_pre_tmp = "tmp/student/" + avatar_tmp
                        if fs.exists(file_path_pre_tmp):
                            fs.delete(file_path_pre_tmp)

            kwargs.update(
                {
                    "data": {
                        "name_value": name_value,
                        "avatar_value": avatar_value,
                        "address_value": address_value,
                        "phone_value": phone_value,
                        "birthday_value": birthday_value,
                        "specialized_value": specialized_value,
                        "description_value": description_value,
                        "uploaded_file": uploaded_file,
                        "file_path_tmp": file_path_tmp,
                        "avatar_tmp_value": avatar_tmp_value,
                        "context": context,
                    }
                }
            )
            result = func(*args, **kwargs)
            if result:
                return result
            else:
                folder_path = "apps/static/assets/images/student/"
                if not os.path.exists(folder_path):
                    os.makedirs(os.path.dirname(folder_path))

                if uploaded_file:
                    file_path = "student/" + avatar_value
                    if fs.exists(file_path):
                        fs.delete(file_path)
                    if fs.exists(file_path_tmp):
                        fs.delete(file_path_tmp)
                    fs.save("student/" + avatar_value, uploaded_file)
                elif avatar_tmp:
                    file_path_tmp_os = "apps/static/assets/images/" + file_path_tmp
                    file_path_os = folder_path + avatar_tmp
                    os.rename(file_path_tmp_os, file_path_os)
                    avatar_value = avatar_tmp

                return redirect("/student")

        return wrapper

    return inner


# @login_required(login_url="/login/")
@file_handle()
def student_add(request, data):
    fs = FileSystemStorage()
    name_value = data["name_value"]
    avatar_value = data["avatar_value"]
    address_value = data["address_value"]
    phone_value = data["phone_value"]
    birthday_value = data["birthday_value"]
    specialized_value = data["specialized_value"]
    description_value = data["description_value"]
    uploaded_file = data["uploaded_file"]
    file_path_tmp = data["file_path_tmp"]
    avatar_tmp_value = data["avatar_tmp_value"]
    context = data["context"]

    try:
        student = Student(
            name=name_value,
            avatar=avatar_value,
            address=address_value,
            phone=phone_value,
            birthday=birthday_value,
            specialized=specialized_value,
            description=description_value,
        )
        student.clean_fields()
        if "avatar" in context:
            raise ValidationError({})
    except ValidationError as e:
        if student.birthday:
            student.birthday = student.birthday.strftime(DATE_INPUT_FORMATS) 
        if uploaded_file:
            if fs.exists(file_path_tmp):
                fs.delete(file_path_tmp)
            fs.save("tmp/student/" + uploaded_file.name, uploaded_file)

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
        return render(request, "student/ui-student-add.html", context)

    Student.create(
        name=name_value,
        avatar=avatar_value,
        address=address_value,
        phone=phone_value,
        birthday=birthday_value,
        specialized=specialized_value,
        description=description_value,
    )


# @login_required(login_url="/login/")
def student_edit_ui(request):
    student_id = request.POST.get("student_id")
    std = Student.get_by_id(student_id)
    return render(request, "student/ui-student-edit.html", {"std": std})


# @login_required(login_url="/login/")
@file_handle()
def student_edit(request, data):
    fs = FileSystemStorage()
    name_value = data["name_value"]
    avatar_value = data["avatar_value"]
    address_value = data["address_value"]
    phone_value = data["phone_value"]
    birthday_value = data["birthday_value"]
    specialized_value = data["specialized_value"]
    description_value = data["description_value"]
    uploaded_file = data["uploaded_file"]
    file_path_tmp = data["file_path_tmp"]
    avatar_tmp_value = data["avatar_tmp_value"]
    context = data["context"]

    student_id = request.POST.get("student_id")
    student = Student.get_by_id(student_id)
    if not avatar_value:
        avatar_value = student.avatar
    try:
        student.name = name_value
        student.avatar = avatar_value
        student.address = address_value
        student.phone = phone_value
        student.birthday = birthday_value
        student.specialized = specialized_value
        student.description = description_value
        student.clean_fields()
        if "avatar" in context:
            raise ValidationError({})
    except ValidationError as e:
        student.birthday = student.birthday.strftime(DATE_INPUT_FORMATS)
        if uploaded_file:
            if fs.exists(file_path_tmp):
                fs.delete(file_path_tmp)
            fs.save("tmp/student/" + uploaded_file.name, uploaded_file)

        context.update(
            {
                "std": student,
                "avatar_tmp": avatar_tmp_value,
            }
        )
        context = {**context, **dict(e)}
        return render(request, "student/ui-student-edit.html", context)

    student.update(
        name=name_value,
        avatar=avatar_value,
        address=address_value,
        phone=phone_value,
        birthday=birthday_value,
        specialized=specialized_value,
        description=description_value,
    )

# @login_required(login_url="/login/")
def student_detail(request):
    id = request.GET.get("id")
    try:
        std = Student.get_by_id(id)
    except Exception as e:
        return render(request, "home/page-404.html")
    return render(request, "student/ui-student-detail.html", {"std": std})
