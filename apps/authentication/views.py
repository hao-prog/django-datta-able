# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

# Create your views here.
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate

from apps.authentication.models import Account
from apps.common_functions import login
from apps.student.models import Student
from apps.teacher.models import Teacher
from .forms import LoginForm, SignUpForm


def login_view(request):
    from django.contrib.auth.models import User

    form = LoginForm(request.POST or None)

    msg = None

    if request.method == "POST":

        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            # user = authenticate(username=username, password=password)
            user = Account.get_by(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("/student")
            else:
                msg = "Wrong user or password"
        else:
            msg = "Error validating the form"

    return render(request, "accounts/login.html", {"form": form, "msg": msg})


def register_user(request):
    msg = None

    if request.method == "POST":
        username = request.POST.get("username")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        try:
            Account.create(username=username, password1=password1, password2=password2)
        except ValidationError as e:
            return render(request, "accounts/register.html", dict(e))

        msg = 'User created - please <a href="/login/">login</a>.'

    return render(
        request,
        "accounts/register.html",
        {"msg": msg},
    )
