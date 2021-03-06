from django.core.exceptions import ValidationError
from django.shortcuts import redirect, render
from apps.common_functions import login_required, upload_file
from apps.student.models import Student
from core.settings import MEDIA_FOLDER_PATH_STUDENT


@login_required()
def student(request):
    keyword = request.GET.get("keyword")
    birthday = request.GET.get("birthday")
    code = request.GET.get("code")
    students = Student.get_students_by(keyword=keyword, birthday=birthday, code=code)
    context = {"data": students}
    return render(request, "student/ui-students.html", context)


@login_required()
def student_delete(request):
    id = request.POST.get("student_id")
    record_student = Student.get_by_id(id)
    record_student.delete()
    return redirect("/student")


@login_required()
def student_add_ui(request):
    return render(request, "student/ui-student-add.html")


@login_required()
def student_add(request):
    name = request.POST.get("name")
    code = request.POST.get("code")
    address = request.POST.get("address")
    phone = request.POST.get("phone")
    birthday = request.POST.get("birthday")
    specialized = request.POST.get("specialized")
    description = request.POST.get("description")
    avatar = ""

    if "avatar" in request.FILES:
        try:
            avatar = upload_file(request.FILES["avatar"], MEDIA_FOLDER_PATH_STUDENT)
        except ValidationError as e:
            return render(request, "student/ui-student-add.html", dict(e))

    try:
        Student.create(
            name=name,
            code=code,
            avatar=avatar,
            address=address,
            phone=phone,
            birthday=birthday,
            specialized=specialized,
            description=description,
        )
    except ValidationError as e:
        return render(request, "student/ui-student-add.html", dict(e))

    return redirect("/student")


@login_required()
def student_edit_ui(request):
    student_id = request.POST.get("student_id")
    record_student = Student.get_by_id(student_id)
    return render(
        request, "student/ui-student-edit.html", {"record_student": record_student}
    )


@login_required()
def student_edit(request):
    student_id = request.POST.get("student_id")
    name = request.POST.get("name")
    code = request.POST.get("code")
    address = request.POST.get("address")
    phone = request.POST.get("phone")
    birthday = request.POST.get("birthday")
    specialized = request.POST.get("specialized")
    description = request.POST.get("description")

    student = Student.get_by_id(student_id)
    avatar = student.avatar

    if "avatar" in request.FILES:
        try:
            avatar = upload_file(request.FILES["avatar"], MEDIA_FOLDER_PATH_STUDENT)
        except ValidationError as e:
            return render(request, "student/ui-student-edit.html", dict(e))

    try:
        student.update(
            name=name,
            code=code,
            avatar=avatar,
            address=address,
            phone=phone,
            birthday=birthday,
            specialized=specialized,
            description=description,
        )
    except ValidationError as e:
        return render(request, "student/ui-student-edit.html", dict(e))

    return redirect("/student")


@login_required()
def student_detail(request):
    id = request.GET.get("id")
    try:
        record_student = Student.get_by_id(id)
    except Exception as e:
        return render(request, "home/page-404.html")
    return render(
        request, "student/ui-student-detail.html", {"record_student": record_student}
    )
