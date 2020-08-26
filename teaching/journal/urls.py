from django.urls import path

from . import views

app_name = "journal"
urlpatterns = [
    path("", views.index_page, name="index"),
    path("students/", views.students_page, name="students"),
    path("change_students/<str:field>", views.change_students, name="change_students"),
    path("lessons/", views.lessons_page, name="lessons"),
    path("change_lessons/<str:field>", views.change_lessons, name="change_lessons"),
    path("tasks/", views.tasks_page, name="tasks"),
    path("change_tasks/<str:field>", views.change_tasks, name="change_tasks"),
    path("attendance/", views.attendance_page, name="attendance"),
]
