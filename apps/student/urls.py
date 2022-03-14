from django.urls import path
from apps.student import views

urlpatterns = [
    path("student", views.student, name="student"),
    path("student_delete", views.student_delete, name="student_delete"),
    path("student_add_ui", views.student_add_ui, name="student_add_ui"),
    path("student_add", views.student_add, name="student_add"),
    path("student_edit_ui", views.student_edit_ui, name="student_edit_ui"),
    path("student_edit", views.student_edit, name="student_edit"),
    path("student_detail", views.student_detail, name="student_detail"),
    
]
