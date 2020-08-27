# -*- coding: utf-8 -*-

import datetime
import math
from .models import Semester, Student, Group, StudyingStudent, Discipline, Task, TaskInGroup, Lesson, LessonInGroup, \
    Attendance, Progress, ControlPoint, Rating
from django.db.models import F

MAX_GRADE = 10


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
    progress = None
    control_points = None
    rating = None

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
        cls.lessons = []
        for lg in cls.lessons_in_group:
            if lg.lesson not in cls.lessons:
                cls.lessons.append(lg.lesson)

    @classmethod
    def init_tasks_in_group(cls):
        cls.tasks_in_group = TaskInGroup.objects.filter(group=cls.common_data["current_group"],
                                                        task__discipline=cls.common_data["current_discipline"])
        cls.tasks = []
        for tg in cls.tasks_in_group:
            if tg.task not in cls.tasks:
                cls.tasks.append(tg.task)

    @classmethod
    def init_control_points(cls):
        cls.control_points = ControlPoint.objects.filter(discipline=cls.common_data["current_discipline"])

    @classmethod
    def init_attendance(cls):
        cls.init_lessons_in_group()
        cls.init_studying_students()

        attendance = Attendance.objects.filter(studying_student__group=cls.common_data["current_group"],
                                               studying_student__discipline=cls.common_data["current_discipline"],
                                               lesson_in_group__group=cls.common_data["current_group"],
                                               lesson_in_group__lesson__discipline=cls.common_data[
                                                   "current_discipline"],
                                               studying_student__subgroup_number=F("lesson_in_group__subgroup_number"))

        cls.attendance = list()
        for ss in cls.studying_students:
            row = dict()
            for lg in cls.lessons_in_group:
                if ss.subgroup_number == lg.subgroup_number:
                    row[lg.lesson.id] = ""
            cls.attendance.append(row)

        studying_students_list = list(cls.studying_students)
        for record in attendance:
            ss = record.studying_student
            student_index = studying_students_list.index(ss)
            lg = record.lesson_in_group
            cls.attendance[student_index][lg.lesson.id] = record.mark

    @classmethod
    def init_progress(cls):
        cls.init_tasks_in_group()
        cls.init_studying_students()

        progress = Progress.objects.filter(studying_student__group=cls.common_data["current_group"],
                                           studying_student__discipline=cls.common_data["current_discipline"],
                                           task_in_group__group=cls.common_data["current_group"],
                                           task_in_group__task__discipline=cls.common_data["current_discipline"],
                                           studying_student__subgroup_number=F("task_in_group__subgroup_number"))

        cls.progress = list()
        for ss in cls.studying_students:
            row = dict()
            for tg in cls.tasks_in_group:
                if ss.subgroup_number == tg.subgroup_number:
                    row[tg.task.id] = [False, 0]
            cls.progress.append(row)

        studying_students_list = list(cls.studying_students)
        for record in progress:
            ss = record.studying_student
            student_index = studying_students_list.index(ss)
            tg = record.task_in_group
            cls.progress[student_index][tg.task.id] = record

    @classmethod
    def _calc_rating(cls):
        for ss in cls.studying_students:
            base_progress = Progress.objects.filter(studying_student=ss)
            base_attendance = Attendance.objects.filter(studying_student=ss)
            for control_point in cls.control_points:
                progress = base_progress.filter(task_in_group__task__deadline__lte=control_point.date)
                attendance = base_attendance.filter(lesson_in_group__lesson__date_fact__lte=control_point.date)
                max_grade = grade = 0
                for progress_record in progress:
                    max_grade += progress_record.task_in_group.task.task_coef
                    if progress_record.passed:
                        grade += progress_record.task_in_group.task.task_coef
                for attendance_record in attendance:
                    max_grade += attendance_record.lesson_in_group.lesson.lesson_coef
                    if attendance_record.mark == "+":
                        grade += attendance_record.lesson_in_group.lesson.lesson_coef * attendance_record.grade / MAX_GRADE
                    elif attendance_record.mark == "оп":
                        grade += 0.8 * attendance_record.lesson_in_group.lesson.lesson_coef * attendance_record.grade / MAX_GRADE
                score = int(math.ceil(control_point.max_score * grade/max_grade))
                if control_point.max_score-score <= 1:
                    score = control_point.max_score

                rating_record = Rating.objects.filter(studying_student=ss, control_point=control_point)[0]
                rating_record.score = score
                rating_record.save()


    @classmethod
    def init_rating(cls):
        cls.init_studying_students()
        cls.init_control_points()

        cls._calc_rating()

        rating = Rating.objects.filter(studying_student__group=cls.common_data["current_group"],
                                       studying_student__discipline=cls.common_data["current_discipline"],
                                       control_point__discipline=cls.common_data["current_discipline"])

        cls.rating = list()
        for ss in cls.studying_students:
            row = dict()
            for control_point in cls.control_points:
                row[control_point.id] = 0
            cls.rating.append(row)

        studying_students_list = list(cls.studying_students)
        for record in rating:
            ss = record.studying_student
            student_index = studying_students_list.index(ss)
            control_point = record.control_point
            cls.rating[student_index][control_point.id] = record.score
