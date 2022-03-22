from django.urls import path
from apps.score import views

urlpatterns = [
    path("score", views.score, name="score"),
    path("score_delete", views.score_delete, name="score_delete"),
    path("score_add_ui", views.score_add_ui, name="score_add_ui"),
    path("score_add", views.score_add, name="score_add"),
    path("score_edit_ui", views.score_edit_ui, name="score_edit_ui"),
    path("score_edit", views.score_edit, name="score_edit"),
    path("score_detail", views.score_detail, name="score_detail"),
    
]
