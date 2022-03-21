from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.shortcuts import redirect, render
from apps.teacher.models import Teacher
from apps.common_functions import upload_file
from core.settings import MEDIA_FOLDER_PATH_TEACHER


def teacher(request):
    teachers = Teacher.get_teachers()
    context = {"data": teachers}
    return render(request, "teacher/ui-teachers.html", context)


def teacher_add_ui(request):
    return render(request, "teacher/ui-teacher-add.html")


def teacher_add(request):
    name = request.POST.get("name")
    address = request.POST.get("address")
    phone = request.POST.get("phone")
    birthday = request.POST.get("birthday")
    specialized = request.POST.get("specialized")
    degree = request.POST.get("degree")
    description = request.POST.get("description")
    avatar = ""

    if "avatar" in request.FILES:
        try:
            avatar = upload_file(request.FILES["avatar"], MEDIA_FOLDER_PATH_TEACHER)
        except ValidationError as e:
            return render(request, "teacher/ui-teacher-add.html", dict(e))

    try:
        Teacher.create(
            name=name,
            avatar=avatar,
            address=address,
            phone=phone,
            birthday=birthday,
            specialized=specialized,
            degree=degree,
            description=description,
        )
    except ValidationError as e:
        return render(request, "teacher/ui-teacher-add.html", dict(e))

    return redirect("/teacher")


def teacher_edit_ui(request):
    teacher_id = request.POST.get("teacher_id")
    record_teacher = Teacher.get_by_id(teacher_id)
    return render(
        request, "teacher/ui-teacher-edit.html", {"record_teacher": record_teacher}
    )


def teacher_edit(request):
    teacher_id = request.POST.get("teacher_id")
    name = request.POST.get("name")
    address = request.POST.get("address")
    phone = request.POST.get("phone")
    birthday = request.POST.get("birthday")
    specialized = request.POST.get("specialized")
    degree = request.POST.get("degree")
    description = request.POST.get("description")

    teacher = Teacher.get_by_id(teacher_id)
    avatar = teacher.avatar

    if "avatar" in request.FILES:
        try:
            avatar = upload_file(request.FILES["avatar"], MEDIA_FOLDER_PATH_TEACHER)
        except ValidationError as e:
            return render(request, "teacher/ui-teacher-edit.html", dict(e))

    try:
        teacher.update(
            name=name,
            avatar=avatar,
            address=address,
            phone=phone,
            birthday=birthday,
            specialized=specialized,
            degree=degree,
            description=description,
        )
    except ValidationError as e:
        return render(request, "teacher/ui-teacher-edit.html", dict(e))

    return redirect("/teacher")


def teacher_detail(request):
    id = request.GET.get("id")
    try:
        record_teacher = Teacher.get_by_id(id)
    except Exception as e:
        return render(request, "home/page-404.html")
    return render(
        request, "teacher/ui-teacher-detail.html", {"record_teacher": record_teacher}
    )


def teacher_delete(request):
    id = request.POST.get("teacher_id")
    record_teacher = Teacher.get_by_id(id)
    record_teacher.delete()
    return redirect("/teacher")
