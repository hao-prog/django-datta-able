from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.shortcuts import redirect, render
from apps.common_functions import upload_file
from apps.course.models import Course
from apps.subject.models import Subject


def course(request):
    keyword = request.GET.get("keyword")
    courses = Course.get_courses_by(keyword)
    context = {"data": courses}
    return render(request, "course/ui-courses.html", context)


def course_delete(request):
    id = request.POST.get("course_id")
    record_course = Course.get_by_id(id)
    record_course.delete()
    return redirect("/course")


def course_add_ui(request):
    subject_records = Subject.get_subjects_by()
    context = {"subject_records": subject_records}
    return render(request, "course/ui-course-add.html", context)


def course_add(request):
    name = request.POST.get("name")
    subject_id = request.POST.get("subject_id")
    description = request.POST.get("description")
    subject = Subject.get_by_id(subject_id)
    try:
        Course.create(
            name=name,
            subject=subject,
            description=description,
        )
    except ValidationError as e:
        return render(request, "course/ui-course-add.html", dict(e))

    return redirect("/course")


def course_edit_ui(request):
    course_id = request.POST.get("course_id")
    record_course = Course.get_by_id(course_id)
    subject_records = Subject.get_subjects_by()
    context = {"record_course": record_course, "subject_records": subject_records}
    return render(request, "course/ui-course-edit.html", context)


def course_edit(request):
    course_id = request.POST.get("course_id")
    name = request.POST.get("name")
    subject_id = request.POST.get("subject_id")
    description = request.POST.get("description")

    course = Course.get_by_id(course_id)
    subject = Subject.get_by_id(subject_id)

    try:
        course.update(
            name=name,
            subject=subject,
            description=description,
        )
    except ValidationError as e:
        return render(request, "course/ui-course-edit.html", dict(e))

    return redirect("/course")


def course_detail(request):
    id = request.GET.get("id")
    try:
        record_course = Course.get_by_id(id)
    except Exception as e:
        return render(request, "home/page-404.html")
    return render(
        request, "course/ui-course-detail.html", {"record_course": record_course}
    )
