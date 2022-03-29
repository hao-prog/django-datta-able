from django.core.exceptions import ValidationError
from django.shortcuts import redirect, render
from apps.common_functions import login_required, upload_file
from apps.subject.models import Subject
from core.settings import MEDIA_FOLDER_PATH_SUBJECT


@login_required()
def subject(request):
    keyword = request.GET.get("keyword")
    subjects = Subject.get_subjects_by(keyword)
    context = {"data": subjects}
    return render(request, "subject/ui-subjects.html", context)


@login_required()
def subject_delete(request):
    id = request.POST.get("subject_id")
    record_subject = Subject.get_by_id(id)
    record_subject.delete()
    return redirect("/subject")


@login_required()
def subject_add_ui(request):
    return render(request, "subject/ui-subject-add.html")


@login_required()
def subject_add(request):
    name = request.POST.get("name")
    description = request.POST.get("description")
    avatar = ""

    if "avatar" in request.FILES:
        try:
            avatar = upload_file(request.FILES["avatar"], MEDIA_FOLDER_PATH_SUBJECT)
        except ValidationError as e:
            return render(request, "subject/ui-subject-add.html", dict(e))

    try:
        Subject.create(
            name=name,
            avatar=avatar,
            description=description,
        )
    except ValidationError as e:
        return render(request, "subject/ui-subject-add.html", dict(e))

    return redirect("/subject")


@login_required()
def subject_edit_ui(request):
    subject_id = request.POST.get("subject_id")
    record_subject = Subject.get_by_id(subject_id)
    return render(
        request, "subject/ui-subject-edit.html", {"record_subject": record_subject}
    )


@login_required()
def subject_edit(request):
    subject_id = request.POST.get("subject_id")
    name = request.POST.get("name")
    description = request.POST.get("description")

    subject = Subject.get_by_id(subject_id)
    avatar = subject.avatar

    if "avatar" in request.FILES:
        try:
            avatar = upload_file(request.FILES["avatar"], MEDIA_FOLDER_PATH_SUBJECT)
        except ValidationError as e:
            return render(request, "subject/ui-subject-edit.html", dict(e))

    try:
        subject.update(
            name=name,
            avatar=avatar,
            description=description,
        )
    except ValidationError as e:
        return render(request, "subject/ui-subject-edit.html", dict(e))

    return redirect("/subject")


@login_required()
def subject_detail(request):
    id = request.GET.get("id")
    try:
        record_subject = Subject.get_by_id(id)
    except Exception as e:
        return render(request, "home/page-404.html")
    return render(
        request, "subject/ui-subject-detail.html", {"record_subject": record_subject}
    )
