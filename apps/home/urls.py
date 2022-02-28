# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from apps.home import views
from apps.home.student import student_views

urlpatterns = [
    # The home page
    path("", views.index, name="home"),
    path("table", views.table, name="table"),
    path("form", views.form, name="form"),
    path("button", views.button, name="button"),
    path("badge", views.badge, name="badge"),
    path("breadcrumb", views.breadcrumb, name="breadcrumb"),
    path("collapse", views.collapse, name="collapse"),
    path("tab", views.tab, name="tab"),
    path("typography", views.typography, name="typography"),
    path("icon", views.icon, name="icon"),

    path("student", student_views.student, name="student"),
    path("student_delete", student_views.student_delete, name="student_delete"),
    path("student_add_ui", student_views.student_add_ui, name="student_add_ui"),
    path("student_add", student_views.student_add, name="student_add"),
    path("student_edit_ui", student_views.student_edit_ui, name="student_edit_ui"),
    path("student_edit", student_views.student_edit, name="student_edit"),
    # Matches any html file
    re_path(r"^.*\.*", views.pages, name="pages"),
]
