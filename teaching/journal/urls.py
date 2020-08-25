from django.urls import path

from . import views

app_name = "journal"
urlpatterns = [
    path("", views.students_page, name="students"),
    path("students/", views.students_page, name="students"),
    path("change_students/<str:field>", views.change_students, name="change_students"),
    path("lessons/", views.lessons_page, name="lessons"),
]
