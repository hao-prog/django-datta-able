# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from multiprocessing import context
from django import template
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.template import loader
from django.urls import reverse
from apps.home.models import Student


@login_required(login_url="/login/")
def index(request):
    context = {"segment": "index"}

    html_template = loader.get_template("home/index.html")
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split("/")[-1]

        if load_template == "admin":
            return HttpResponseRedirect(reverse("admin:index"))
        context["segment"] = load_template

        html_template = loader.get_template("home/" + load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template("home/page-404.html")
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template("home/page-500.html")
        return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def table(request):
    context = {
        "data": [
            {"fn": "Blah Blah", "ln": "Baroibeo", "usrn": "PhanTanTrung"},
            {"fn": "Adidas Phat", "ln": "LOLOLOLOLOL", "usrn": "FrontLever"},
            {"fn": "Calisthenics", "ln": "DeadmanPress", "usrn": "HumanFlag"},
            {"fn": "Handstand", "ln": "MuscleUp", "usrn": "Planche"},
        ],
    }

    html_template = loader.get_template("home/ui-tables.html")
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def form(request):
    context = {"email": "abc@abc.com"}

    html_template = loader.get_template("home/ui-forms.html")
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def button(request):
    context = {}

    html_template = loader.get_template("home/ui-button.html")
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def badge(request):
    context = {}

    html_template = loader.get_template("home/ui-badges.html")
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def breadcrumb(request):
    context = {}

    html_template = loader.get_template("home/ui-breadcrumb-pagination.html")
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def collapse(request):
    context = {}

    html_template = loader.get_template("home/ui-collapse.html")
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def tab(request):
    context = {}

    html_template = loader.get_template("home/ui-tabs.html")
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def typography(request):
    context = {}

    html_template = loader.get_template("home/ui-typography.html")
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def icon(request):
    context = {}

    html_template = loader.get_template("home/ui-icons.html")
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def student(request):
    students = Student.objects.filter(deleted=False)
    context = {"data": students}
    return render(request, "home/ui-students.html", context)

@login_required(login_url="/login/")
def student_delete(request):
    id = request.POST.get('student_id')
    std = Student.objects.get(pk=id)
    std.deleted = True
    std.save()
    return redirect('/student')

@login_required(login_url="/login/")
def student_add_ui(request):
    return render(request, "home/ui-student-add.html")

@login_required(login_url="/login/")
def student_add(request):
    fn = request.POST.get('fn')
    ln = request.POST.get('ln')
    usrn = request.POST.get('usrn')
    std = Student(first_name=fn, last_name=ln, user_name=usrn)
    try:
        std.clean_fields()
    except ValidationError as e:
        context = {'std': std}
        context = {**context, **dict(e)}
        return render(request, "home/ui-student-add.html", context)
    std.save()
    return redirect('/student')

@login_required(login_url="/login/")
def student_edit_ui(request):
    student_id = request.POST.get('student_id')
    std = Student.objects.get(pk=student_id)
    return render(request, "home/ui-student-edit.html", {'std': std})

@login_required(login_url="/login/")
def student_edit(request):
    student_id = request.POST.get('student_id')
    fn = request.POST.get('fn')
    ln = request.POST.get('ln')
    usrn = request.POST.get('usrn')
    
    std = Student.objects.get(pk=student_id)
    std.first_name = fn
    std.last_name = ln
    std.user_name = usrn
    
    try:
        std.clean_fields()
    except ValidationError as e:
        context = {'std': std}
        context = {**context, **dict(e)}
        return render(request, "home/ui-student-edit.html", context)
    std.save()
    return redirect('/student')
