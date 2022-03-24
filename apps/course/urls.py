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
    path(
        "course_teacher_add_ui",
        views.course_teacher_add_ui,
        name="course_teacher_add_ui",
    ),
    path(
        "course_student_add_ui",
        views.course_student_add_ui,
        name="course_student_add_ui",
    ),
    path(
        "course_teacher_add",
        views.course_teacher_add,
        name="course_teacher_add",
    ),
    path(
        "course_student_add",
        views.course_student_add,
        name="course_student_add",
    ),
    path(
        "course_teacher_delete",
        views.course_teacher_delete,
        name="course_teacher_delete",
    ),
    path(
        "course_student_delete",
        views.course_student_delete,
        name="course_student_delete",
    ),
]
