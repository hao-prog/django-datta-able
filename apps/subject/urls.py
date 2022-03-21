from django.urls import path
from apps.subject import views

urlpatterns = [
    path("subject", views.subject, name="subject"),
    path("subject_delete", views.subject_delete, name="subject_delete"),
    path("subject_add_ui", views.subject_add_ui, name="subject_add_ui"),
    path("subject_add", views.subject_add, name="subject_add"),
    path("subject_edit_ui", views.subject_edit_ui, name="subject_edit_ui"),
    path("subject_edit", views.subject_edit, name="subject_edit"),
    path("subject_detail", views.subject_detail, name="subject_detail"),
    
]
