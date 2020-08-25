from django.urls import path

from . import views

app_name = "journal"
urlpatterns = [
    path("", views.index, name="index"),
    path("students/", views.students_page, name="students"),
]