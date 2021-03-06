# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.conf import settings
from django.contrib import admin
from django.urls import path, include  # add this
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),  # Django admin route
    path("", include("apps.authentication.urls")),  # Auth routes - login / register
    path("", include("apps.student.urls")),
    path("", include("apps.teacher.urls")),
    path("", include("apps.subject.urls")),
    path("", include("apps.course.urls")),
    path("", include("apps.score.urls")),

    path("", include("apps.home.urls")),  # UI Kits Html files
]

if True:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
