# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from apps.home import views

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
    # Matches any html file
    re_path(r"^.*\.*", views.pages, name="pages"),
]
