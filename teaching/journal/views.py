from django.shortcuts import render, get_object_or_404

from django.http import HttpResponse, Http404
from django.template import loader
from django.views import generic
from django.core import serializers

from .models import Semester, Student, Group, StudyingStudent, Discipline, Task, TaskInGroup, Lesson, LessonInGroup, \
    Attendance, Progress, ControlPoint, Rating
from .commondata import CommonData


def index(request):
    CommonData.prepare_data(request.POST)
    context = {"common_data": CommonData.data}
    return render(request, "journal/base.html", context=context)


def students_page(request):
    CommonData.prepare_data(request.POST)
    studying_students = StudyingStudent.objects.filter(group=CommonData.data["current_group"],
                                              discipline=CommonData.data["current_discipline"])

    context = {"common_data": CommonData.data, "studying_students": studying_students}
    return render(request, "journal/students.html", context=context)