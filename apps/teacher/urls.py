from django.urls import path
from apps.teacher import views

urlpatterns = [
    path("teacher", views.teacher, name="teacher"),
    path("teacher_delete", views.teacher_delete, name="teacher_delete"),
    path("teacher_add_ui", views.teacher_add_ui, name="teacher_add_ui"),
    path("teacher_add", views.teacher_add, name="teacher_add"),
    path("teacher_edit_ui", views.teacher_edit_ui, name="teacher_edit_ui"),
    path("teacher_edit", views.teacher_edit, name="teacher_edit"),
    path("teacher_detail", views.teacher_detail, name="teacher_detail"),
    
]
