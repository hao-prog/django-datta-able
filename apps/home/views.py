# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django import template

# from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.template import loader
from django.urls import reverse

from apps.common_functions import login_required


@login_required()
def index(request):
    context = {"segment": "index"}
    
    html_template = loader.get_template("home/index.html")
    return HttpResponse(html_template.render(context, request))


@login_required()
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


@login_required()
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


@login_required()
def form(request):
    context = {"email": "abc@abc.com"}

    html_template = loader.get_template("home/ui-forms.html")
    return HttpResponse(html_template.render(context, request))


@login_required()
def button(request):
    context = {}

    html_template = loader.get_template("home/ui-button.html")
    return HttpResponse(html_template.render(context, request))


@login_required()
def badge(request):
    context = {}

    html_template = loader.get_template("home/ui-badges.html")
    return HttpResponse(html_template.render(context, request))


@login_required()
def breadcrumb(request):
    context = {}

    html_template = loader.get_template("home/ui-breadcrumb-pagination.html")
    return HttpResponse(html_template.render(context, request))


@login_required()
def collapse(request):
    context = {}

    html_template = loader.get_template("home/ui-collapse.html")
    return HttpResponse(html_template.render(context, request))


@login_required()
def tab(request):
    context = {}

    html_template = loader.get_template("home/ui-tabs.html")
    return HttpResponse(html_template.render(context, request))


@login_required()
def typography(request):
    context = {}

    html_template = loader.get_template("home/ui-typography.html")
    return HttpResponse(html_template.render(context, request))


@login_required()
def icon(request):
    context = {}

    html_template = loader.get_template("home/ui-icons.html")
    return HttpResponse(html_template.render(context, request))
