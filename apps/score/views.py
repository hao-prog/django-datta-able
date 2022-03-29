from django.core.exceptions import ValidationError
from django.shortcuts import redirect, render
from apps.common_functions import login_required
from apps.course.models import Course
from apps.score.models import Score
from apps.student.models import Student
from apps.subject.models import Subject


@login_required()
def score(request):
    keyword = request.GET.get("keyword")
    student_name = request.GET.get("student_name")
    course_name = request.GET.get("course_name")
    score_records = Score.get_scores_by(keyword, student_name, course_name)
    context = {"data": score_records}
    return render(request, "score/ui-scores.html", context)


@login_required()
def score_delete(request):
    id = request.POST.get("score_id")
    record_score = Score.get_by_id(id)
    record_score.delete()
    return redirect("/score")


@login_required()
def score_add_ui(request):
    student_records = Student.get_students_by()
    course_records = Course.get_courses_by()
    context = {
        "student_records": student_records,
        "course_records": course_records,
    }
    return render(request, "score/ui-score-add.html", context)


@login_required()
def score_add(request):
    student_id = request.POST.get("student_id")
    course_id = request.POST.get("course_id")
    score = request.POST.get("score")
    description = request.POST.get("description")
    try:
        Score.create(
            student_id=student_id,
            course_id=course_id,
            score=score,
            description=description,
        )
    except ValidationError as e:
        return render(request, "score/ui-score-add.html", dict(e))

    return redirect("/score")


@login_required()
def score_edit_ui(request):
    score_id = request.POST.get("score_id")
    student_records = Student.get_students_by()
    course_records = Course.get_courses_by()
    record_score = Score.get_by_id(score_id)
    context = {
        "record_score": record_score,
        "student_records": student_records,
        "course_records": course_records,
    }
    return render(request, "score/ui-score-edit.html", context)


@login_required()
def score_edit(request):
    score_id = request.POST.get("score_id")
    student_id = request.POST.get("student_id")
    course_id = request.POST.get("course_id")
    score = request.POST.get("score")
    description = request.POST.get("description")

    score_record = Score.get_by_id(score_id)

    try:
        score_record.update(
            student_id=student_id,
            course_id=course_id,
            score=score,
            description=description,
        )
    except ValidationError as e:
        return render(request, "score/ui-score-edit.html", dict(e))

    return redirect("/score")


@login_required()
def score_detail(request):
    id = request.GET.get("id")
    try:
        record_score = Score.get_by_id(id)
    except Exception as e:
        return render(request, "home/page-404.html")
    return render(request, "score/ui-score-detail.html", {"record_score": record_score})
