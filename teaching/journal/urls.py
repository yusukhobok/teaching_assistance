from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<int:semester_id>/", views.semester, name="semester"),
    path("students/", views.StudentsView.as_view(), name="students")
]