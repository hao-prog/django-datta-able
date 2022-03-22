from django.urls import path
from apps.course import views

urlpatterns = [
    path("course", views.course, name="course"),
    path("course_delete", views.course_delete, name="course_delete"),
    path("course_add_ui", views.course_add_ui, name="course_add_ui"),
    path("course_add", views.course_add, name="course_add"),
    path("course_edit_ui", views.course_edit_ui, name="course_edit_ui"),
    path("course_edit", views.course_edit, name="course_edit"),
    path("course_detail", views.course_detail, name="course_detail"),
    
]
