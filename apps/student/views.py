from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.shortcuts import redirect, render
from apps.common_functions import move_tmp_file, upload_file, validate_file
from apps.student.models import Student
from django.core.files.storage import FileSystemStorage
from core.settings import DATE_INPUT_FORMATS, MEDIA_FOLDER_PATH


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


# @login_required(login_url="/login/")
def student_add(request):
    fs = FileSystemStorage()
    folder_path = MEDIA_FOLDER_PATH + "student/"
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
    file_path_tmp = "tmp/student/" + avatar_tmp

    if "avatar" in request.FILES:
        context["avatar"], avatar_value, file_path_tmp, avatar_tmp_value = upload_file(
            request.FILES["avatar"],
            "tmp/student/",
            file_path_tmp,
            avatar_tmp,
        )

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
        if context.get("avatar"):
            raise ValidationError({})
    except ValidationError as e:
        if student.birthday:
            student.birthday = student.birthday.strftime(DATE_INPUT_FORMATS)

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

    move_tmp_file(folder_path, file_path_tmp, avatar_tmp_value)

    return redirect("/student")


# @login_required(login_url="/login/")
def student_edit_ui(request):
    student_id = request.POST.get("student_id")
    std = Student.get_by_id(student_id)
    return render(request, "student/ui-student-edit.html", {"std": std})


# @login_required(login_url="/login/")
def student_edit(request):
    fs = FileSystemStorage()
    folder_path = MEDIA_FOLDER_PATH + "student/"
    context = {}

    student_id = request.POST.get("student_id")
    name_value = request.POST.get("name")
    address_value = request.POST.get("address")
    phone_value = request.POST.get("phone")
    birthday_value = request.POST.get("birthday")
    specialized_value = request.POST.get("specialized")
    description_value = request.POST.get("description")
    avatar_tmp = request.POST.get("avatar_tmp")  # upload file in tmp folder

    avatar_tmp_value = avatar_tmp  # new avatar_tmp
    avatar_value = avatar_tmp or ""
    file_path_tmp = "tmp/student/" + avatar_tmp

    if "avatar" in request.FILES:
        context["avatar"], avatar_value, file_path_tmp, avatar_tmp_value = upload_file(
            request.FILES["avatar"],
            "tmp/student/",
            file_path_tmp,
            avatar_tmp,
        )

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
        if context.get("avatar"):
            raise ValidationError({})
    except ValidationError as e:
        student.birthday = student.birthday.strftime(DATE_INPUT_FORMATS)

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

    move_tmp_file(folder_path, file_path_tmp, avatar_tmp_value)

    return redirect("/student")


# @login_required(login_url="/login/")
def student_detail(request):
    id = request.GET.get("id")
    try:
        std = Student.get_by_id(id)
    except Exception as e:
        return render(request, "home/page-404.html")
    return render(request, "student/ui-student-detail.html", {"std": std})
