from django.shortcuts import render, get_object_or_404

from django.http import HttpResponse, Http404
from django.template import loader
from django.views import generic
from django.core import serializers
from django.shortcuts import redirect

from .models import Semester, Student, Group, StudyingStudent, Discipline, Task, TaskInGroup, Lesson, LessonInGroup, \
    Attendance, Progress, ControlPoint, Rating
from .commondata import Data


def index_page(request):
    return render(request, "journal/base.html")

def students_page(request):
    Data.prepare_data(request.POST)
    Data.init_studying_students()
    context = {"common_data": Data.common_data, "studying_students": Data.studying_students}
    return render(request, "journal/students.html", context=context)

def extract_value_and_position(request):
    newValue = request.POST.get("newValue", None)
    position = request.POST.get("position", None)
    if newValue is not None and position is not None:
        position = int(position)
    return newValue, position



def change_students(request, field):
    newValue, position = extract_value_and_position(request)
    if newValue is not None and position is not None:
        id = Data.studying_students[position].student.id
        student = Student.objects.filter(id=id)[0]
        if field == "expelled":
            newValue = newValue == "true"
        setattr(student, field, newValue)
        student.save()
        return HttpResponse("CHANGE")
    else:
        return redirect("journal:students")


def lessons_page(request):
    Data.prepare_data(request.POST)
    Data.init_lessons_in_group()
    context = {"common_data": Data.common_data, "lessons": Data.lessons}
    return render(request, "journal/lessons.html", context=context)


def change_lessons(request, field):
    newValue, position = extract_value_and_position(request)
    if newValue is not None and position is not None:
        id = Data.lessons[position].id
        lesson = Lesson.objects.filter(id=id)[0]
        # if field == "expelled":
        #     newValue = newValue == "true"
        setattr(lesson, field, newValue)
        lesson.save()
        return HttpResponse("CHANGE")
    else:
        return redirect("journal:lessons")
