from django.shortcuts import render, get_object_or_404

from django.http import HttpResponse, Http404
from django.template import loader
from django.views import generic

from .models import Semester, Student


def index(request):
    # template = loader.get_template("journal/index.html")
    # return HttpResponse(template.render())
    context = {}
    return render(request, "journal/index.html", context)

def semester(request, semester_id):
    semester = get_object_or_404(Semester, pk=semester_id)
    return render(request, "journal/semester.html", {"semester": semester})


class StudentsView(generic.ListView):
    template_name = "journal/students.html"
    context_object_name = "students_list"

    def get_queryset(self):
        return Student.objects.all()