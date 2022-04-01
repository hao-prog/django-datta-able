from django.core.exceptions import ValidationError
from django.shortcuts import redirect, render
from apps.common_functions import login_required
from apps.course.models import Course, CourseStudent, CourseTeacher
from apps.subject.models import Subject
from apps.teacher.models import Teacher
from apps.student.models import Student


@login_required()
def course(request):
    keyword = request.GET.get("keyword")
    courses = Course.get_courses_by(keyword)
    context = {"data": courses}
    return render(request, "course/ui-courses.html", context)


@login_required()
def course_delete(request):
    id = request.POST.get("course_id")
    record_course = Course.get_by_id(id)
    record_course.delete()
    return redirect("/course")


@login_required()
def course_add_ui(request):
    student_name = request.GET.get("student_name")
    student_code = request.GET.get("student_code")
    teacher_name = request.GET.get("teacher_name")
    teacher_code = request.GET.get("teacher_code")
    subject_records = Subject.get_subjects_by()
    teacher_records = Teacher.get_teachers_by()
    student_records = Student.get_students_by(keyword=student_name, code=student_code)
    context = {
        "subject_records": subject_records,
        "teacher_records": teacher_records,
        "student_records": student_records,
    }
    return render(request, "course/ui-course-add.html", context)


@login_required()
def course_add(request):
    name = request.POST.get("name")
    subject_id = request.POST.get("subject_id")
    description = request.POST.get("description")
    teachers = request.POST.getlist("teachers")
    students = request.POST.getlist("students")
    try:
        course_record = Course.create(
            name=name,
            subject_id=subject_id,
            description=description,
        )
        for teacher_id in teachers:
            CourseTeacher.create(course_record.id, teacher_id)
        for student_id in students:
            CourseStudent.create(course_record.id, student_id)
    except ValidationError as e:
        return render(request, "course/ui-course-add.html", dict(e))

    return redirect("/course")


@login_required()
def course_edit_ui(request):
    course_id = request.POST.get("course_id")
    record_course = Course.get_by_id(course_id)
    subject_records = Subject.get_subjects_by()
    teacher_records = record_course.get_teacher_list()
    student_records = record_course.get_student_list()
    context = {
        "record_course": record_course,
        "subject_records": subject_records,
        "teacher_records": teacher_records,
        "student_records": student_records,
    }
    return render(request, "course/ui-course-edit.html", context)


@login_required()
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


@login_required()
def course_detail(request):
    id = request.GET.get("id")
    try:
        record_course = Course.get_by_id(id)
        teacher_records = record_course.get_teacher_list()
        student_records = record_course.get_student_list()
    except Exception as e:
        return render(request, "home/page-404.html")
    return render(
        request,
        "course/ui-course-detail.html",
        {
            "record_course": record_course,
            "teacher_records": teacher_records,
            "student_records": student_records,
        },
    )


@login_required()
def course_teacher_add_ui(request):
    course_id = request.POST.get("course_id")
    course_record = Course.get_by_id(course_id)
    teacher_records = course_record.get_teachers_exclude()
    context = {"teacher_records": teacher_records, "course_id": course_id}
    return render(request, "course/ui-course-teacher-add.html", context)


@login_required()
def course_student_add_ui(request):
    course_id = request.POST.get("course_id")
    course_record = Course.get_by_id(course_id)
    student_records = course_record.get_students_exclude()
    context = {"student_records": student_records, "course_id": course_id}
    return render(request, "course/ui-course-student-add.html", context)


@login_required()
def course_teacher_add(request):
    course_id = request.POST.get("course_id")
    teacher_id = request.POST.get("teacher_id")
    try:
        CourseTeacher.create(course_id, teacher_id)
    except ValidationError as e:
        return render(request, "course/ui-course-teacher-add.html", dict(e))
    return redirect("/course")


@login_required()
def course_student_add(request):
    course_id = request.POST.get("course_id")
    student_id = request.POST.get("student_id")
    try:
        CourseStudent.create(course_id, student_id)
    except ValidationError as e:
        return render(request, "course/ui-course-student-add.html", dict(e))
    return redirect("/course")


@login_required()
def course_teacher_delete(request):
    course_id = request.POST.get("course_id")
    teacher_id = request.POST.get("teacher_id")
    course_teacher = CourseTeacher.get_by(course_id=course_id, teacher_id=teacher_id)
    course_teacher.delete()
    return redirect("/course")


@login_required()
def course_student_delete(request):
    course_id = request.POST.get("course_id")
    student_id = request.POST.get("student_id")
    course_student = CourseStudent.get_by(course_id=course_id, student_id=student_id)
    course_student.delete()
    return redirect("/course")
