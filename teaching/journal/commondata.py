# -*- coding: utf-8 -*-

import datetime
from .models import Semester, Student, Group, StudyingStudent, Discipline, Task, TaskInGroup, Lesson, LessonInGroup, \
    Attendance, Progress, ControlPoint, Rating


class Data():
    common_data = {
        "current_semester": None,
        "current_discipline": None,
        "current_group": None,
        "current_date": None,
        "semesters": None,
        "disciplines": None,
        "groups": None,
        "is_initialize": False}
    studying_students = None
    lessons_in_group = None
    lessons = None
    tasks_in_group = None
    tasks = None
    attendance = None

    @classmethod
    def set_today(cls):
        cls.common_data["current_date"] = datetime.datetime.now()

    @classmethod
    def set_current_date(cls, date: str):
        date = datetime.datetime.strptime(date, "%Y-%m-%d")
        cls.common_data["current_date"] = date

    @classmethod
    def set_current_semester(cls, id):
        if cls.common_data["semesters"] is None:
            return
        try:
            if cls.common_data["current_semester"].id == id:
                return
            for semester in cls.common_data["semesters"]:
                semester.is_current = False
                semester.save()
            cls.common_data["current_semester"] = Semester.objects.filter(id=id)[0]
            cls.common_data["current_semester"].is_current = True
            cls.common_data["current_semester"].save()
        except IndexError:
            pass

    @classmethod
    def set_current_discipline(cls, id):
        if cls.common_data["disciplines"] is None:
            return
        try:
            if cls.common_data["current_discipline"].id == id:
                return
            for discipline in cls.common_data["disciplines"]:
                discipline.is_current = False
                discipline.save()
            cls.common_data["current_discipline"] = Discipline.objects.filter(id=id)[0]
            cls.common_data["current_discipline"].is_current = True
            cls.common_data["current_discipline"].save()
        except IndexError:
            pass

    @classmethod
    def set_current_group(cls, id):
        if cls.common_data["groups"] is None:
            return
        try:
            if cls.common_data["current_group"].id == id:
                return
            for group in cls.common_data["groups"]:
                group.is_current = False
                group.save()
            cls.common_data["current_group"] = Group.objects.filter(id=id)[0]
            cls.common_data["current_group"].is_current = True
            cls.common_data["current_group"].save()
        except IndexError:
            pass

    @classmethod
    def load_current_semester(cls):
        semester = Semester.objects.filter(is_current=True)
        try:
            cls.common_data["current_semester"] = semester[0]
        except IndexError:
            cls.common_data["current_semester"] = None

    @classmethod
    def load_current_discipline(cls):
        discipline = Discipline.objects.filter(is_current=True)
        try:
            cls.common_data["current_discipline"] = discipline[0]
        except IndexError:
            cls.common_data["current_discipline"] = None

    @classmethod
    def load_current_group(cls):
        group = Group.objects.filter(is_current=True)
        try:
            cls.common_data["current_group"] = group[0]
        except IndexError:
            cls.common_data["current_group"] = None

    @classmethod
    def load_semesters(cls):
        cls.common_data["semesters"] = Semester.objects.all()

    @classmethod
    def load_disciplines(cls):
        if cls.common_data["current_semester"] is None:
            cls.common_data["disciplines"] = None
        else:
            cls.common_data["disciplines"] = Discipline.objects.filter(semester=cls.common_data["current_semester"])

    @classmethod
    def load_groups(cls):
        if cls.common_data["current_semester"] is None or cls.common_data["current_discipline"] is None:
            cls.common_data["groups"] = None
        else:
            cls.common_data["groups"] = Group.objects.filter(semester=cls.common_data["current_semester"])

    @classmethod
    def initialize(cls):
        if not cls.common_data["is_initialize"]:
            cls.load_semesters()
            cls.load_current_semester()
            cls.load_disciplines()
            cls.load_current_discipline()
            cls.load_groups()
            cls.load_current_group()
            cls.set_today()
            cls.common_data["is_initialize"] = True

    @classmethod
    def refresh_current_values(cls, POST):
        cls.set_current_semester(POST["semester"])
        cls.set_current_discipline(POST["discipline"])
        cls.set_current_group(POST["group"])
        cls.set_current_date(POST["date"])

    @classmethod
    def prepare_data(cls, POST):
        if len(POST) == 0:
            cls.initialize()
        else:
            cls.refresh_current_values(POST)

    @classmethod
    def init_studying_students(cls):
        cls.studying_students = StudyingStudent.objects.filter(group=cls.common_data["current_group"],
                                                               discipline=cls.common_data["current_discipline"])

    @classmethod
    def init_lessons_in_group(cls):
        cls.lessons_in_group = LessonInGroup.objects.filter(group=cls.common_data["current_group"],
                                                            lesson__discipline=cls.common_data["current_discipline"])

        #TODO:можно ли это решить внутренними средствами Django? SQL?
        cls.lessons = []
        for lg in cls.lessons_in_group:
            if lg.lesson not in cls.lessons:
                cls.lessons.append(lg.lesson)

    @classmethod
    def init_tasks_in_group(cls):
        cls.tasks_in_group = TaskInGroup.objects.filter(group=cls.common_data["current_group"],
                                                        task__discipline=cls.common_data["current_discipline"])

        #TODO:можно ли это решить внутренними средствами Django? SQL?
        cls.tasks = []
        for tg in cls.tasks_in_group:
            if tg.task not in cls.tasks:
                cls.tasks.append(tg.task)

    @classmethod
    def init_attendance(cls):
        cls.init_lessons_in_group()
        cls.init_studying_students()

        cls.attendance = list()
        for ss in cls.studying_students:
            students_data = dict()
            for lg in cls.lessons_in_group:
                if ss.subgroup_number == lg.subgroup_number:
                    att = Attendance.objects.filter(studying_student=ss, lesson_in_group=lg)[0]
                    students_data[f"{lg.lesson.abbreviation} ({lg.lesson.id})"] = f"{att.mark} ({att.grade})"
                    # students_data[f"lesson_{lg.lesson.id}"] = f"{att.mark} ({att.grade})"
            cls.attendance.append(students_data)
        # for el in cls.attendance:
        #     print(el)
