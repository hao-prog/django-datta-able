from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.shortcuts import redirect, render
from apps.home.student.models import Student


@login_required(login_url="/login/")
def student(request):
    students = Student.get_students()
    context = {"data": students}
    return render(request, "student/ui-students.html", context)

@login_required(login_url="/login/")
def student_delete(request):
    id = request.POST.get('student_id')
    std = Student.get_by_id(id)
    std.delete()
    return redirect('/student')

@login_required(login_url="/login/")
def student_add_ui(request):
    return render(request, "student/ui-student-add.html")

@login_required(login_url="/login/")
def student_add(request):
    fn = request.POST.get('fn')
    ln = request.POST.get('ln')
    usrn = request.POST.get('usrn')
    try:
        Student.create(fn, ln, usrn)
    except ValidationError as e:
        context = {'fn': fn, 'ln': ln, 'usrn': usrn}
        context = {**context, **dict(e)}
        return render(request, "student/ui-student-add.html", context)
    return redirect('/student')

@login_required(login_url="/login/")
def student_edit_ui(request):
    student_id = request.POST.get('student_id')
    std = Student.get_by_id(student_id)
    return render(request, "student/ui-student-edit.html", {'std': std})

@login_required(login_url="/login/")
def student_edit(request):
    student_id = request.POST.get('student_id')
    fn = request.POST.get('fn')
    ln = request.POST.get('ln')
    usrn = request.POST.get('usrn')
    
    std = Student.get_by_id(student_id)
    
    try:
        std.update(fn, ln, usrn)
        
    except ValidationError as e:
        context = {'std': std}
        context = {**context, **dict(e)}
        return render(request, "student/ui-student-edit.html", context)

    return redirect('/student')
