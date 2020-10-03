import datetime
import pandas as pd
from typing import Tuple, Dict, Sequence

from teaching_assistance_db import db


class actions():
    @staticmethod
    def clear_all():
        db.clear_all()

    @staticmethod
    def clear_semester(semester_id: int):
        db.clear_semester(semester_id)

    @staticmethod
    def get_semester(academic_year: str, season: int):
        if academic_year not in db.ACADEMIC_YEARS:
            raise ValueError("Academic year is incorrect")
        if season not in (1, 2):
            raise ValueError("Season must be 1 or 2")
        row = db.select_one_from_db(
            "SELECT id FROM journal_semester WHERE academic_year = %s AND season = %s", (academic_year, season))
        return row[0]

    @staticmethod
    def insert_semester(academic_year: str, season: int):
        if academic_year not in db.ACADEMIC_YEARS:
            raise ValueError("Academic year is incorrect")
        if season not in (1, 2):
            raise ValueError("Season must be 1 or 2")
        semester_id = db.insert_record('journal_semester',
                                       {
                                           "academic_year": academic_year,
                                           "season": season,
                                           "is_current": False,
                                       })
        return semester_id

    @staticmethod
    def insert_group(group_number: str, course_number: int, semester_id: int):
        group_id = db.insert_record('journal_group',
                                    {
                                        "group_number": group_number,
                                        "course_number": course_number,
                                        "semester_id": semester_id,
                                        "is_current": False,
                                    })
        return group_id

    @staticmethod
    def insert_discipline(name: str, short_name: str, semester_id: int):
        discipline_id = db.insert_record('journal_discipline',
                                         {
                                             "name": name,
                                             "short_name": short_name,
                                             "semester_id": semester_id,
                                             "is_current": False,
                                         })
        return discipline_id

    @staticmethod
    def insert_student(last_name: str, first_name: str, middle_name: str, grade_book_number: str, email: str = "", phone: str = "", profile: str = "", comments: str = "", expelled: bool = False):
        student_id = db.insert_record('journal_student',
                                      {
                                          "last_name": last_name,
                                          "first_name": first_name,
                                          "middle_name": middle_name,
                                          "grade_book_number": grade_book_number,
                                          "email": email,
                                          "phone": phone,
                                          "profile": profile,
                                          "comments": comments,
                                          "expelled": expelled,
                                      })
        return student_id

    @staticmethod
    def import_students_from_CSV(filename: str, group_id: int, discipline_id: int):
        students_data = pd.read_csv(filename, sep=';', header=0)
        students_data = students_data.dropna(how='all')
        students_data.fillna('', inplace=True)
        FIO = tuple(students_data["name"].apply(
            lambda value: value.split(" ")))
        FIO = tuple(zip(*FIO))
        students_data["last_name"] = FIO[0]
        students_data["first_name"] = FIO[1]
        students_data["middle_name"] = FIO[2]
        # print(students_data)

        def add_student(row):
            student_id = actions.insert_student(row['last_name'], row['first_name'], row['middle_name'], row['grade_book_number'],
                                        row['email'], row['phone'], row['profile'], row['comments'])
            db.insert_record('journal_studyingstudent',
                             {
                                 "student_id": student_id,
                                 "group_id": group_id,
                                 "subgroup_number": row['subgroup_number'],
                                 "discipline_id": discipline_id,
                                 "is_head": False,
                             })
        students_data.apply(add_student, axis=1)

    @staticmethod
    def insert_task(deadline: str, topic: str, abbreviation: str, task_kind: str, comments: str, task_coef: int, discipline_id: int):
        TASK_KINDS = ("LB", "PR", "KONTR", "TEST", "RGR", "KR",
                      "KP", "SECTION", "ALLOW", "ZACHET", "EXAM")
        if task_kind not in TASK_KINDS:
            raise ValueError(f"Task kind {task_kind} is incorrect")
        task_id = db.insert_record('journal_task',
                                   {
                                       "discipline_id": discipline_id,
                                       "deadline": deadline,
                                       "topic": topic,
                                       "abbreviation": abbreviation,
                                       "task_kind": task_kind,
                                       "comments": comments,
                                       "task_coef": task_coef,
                                   })
        return task_id

    @staticmethod
    def import_tasks_from_CSV(filename: str, discipline_id: int, groups_and_subgroups: Tuple[Tuple[int, int]]):
        tasks_data = pd.read_csv(filename, sep=';', header=0)
        tasks_data = tasks_data.dropna(how='all')
        tasks_data.fillna('', inplace=True)
        tasks_data["task_coef"] = tasks_data["task_coef"].astype("int32")
        tasks_data["deadline"] = pd.to_datetime(
            tasks_data['deadline'], format='%d.%m.%Y')
        # print(tasks_data)

        def add_task(row):
            task_id = actions.insert_task(row['deadline'], row['topic'], row['abbreviation'],
                                  row['task_kind'], row['comments'], row['task_coef'], discipline_id)
            for group_id, subgroup_number in groups_and_subgroups:
                db.insert_record('journal_taskingroup',
                                 {
                                     "task_id": task_id,
                                     "group_id": group_id,
                                     "subgroup_number": subgroup_number,
                                 })
        tasks_data.apply(add_task, axis=1)

    @staticmethod
    def insert_lesson(date_plan: datetime.date, topic: str, abbreviation: str, lesson_kind: str, comments: str, discipline_id: int, lesson_coef: int):
        LESSON_KINDS = ("LK", "PR", "LB", "CONS", "EXAM")
        if lesson_kind not in LESSON_KINDS:
            raise ValueError(f"Lesson kind {lesson_kind} is incorrect")
        lesson_id = db.insert_record('journal_lesson',
                                     {
                                         "discipline_id": discipline_id,
                                         "date_plan": date_plan,
                                         "date_fact": date_plan,
                                         "topic": topic,
                                         "abbreviation": abbreviation,
                                         "lesson_kind": lesson_kind,
                                         "comments": comments,
                                         "lesson_coef": lesson_coef,
                                     })
        return lesson_id

    @staticmethod
    def import_lessons_from_CSV(filename: str, discipline_id: int, groups_and_subgroups: Tuple[Tuple[int, int]], lesson_coef: int):
        lessons_data = pd.read_csv(filename, sep=';', header=0)
        lessons_data = lessons_data.dropna(how='all')
        lessons_data.fillna('', inplace=True)
        lessons_data["date_plan"] = pd.to_datetime(
            lessons_data['date_plan'], format='%d.%m.%Y')
        # print(lessons_data)

        def add_lesson(row):
            lesson_id = actions.insert_lesson(row['date_plan'], row['topic'], row['abbreviation'],
                                      row['lesson_kind'], row['comments'], discipline_id, lesson_coef=lesson_coef)
            for group_id, subgroup_number in groups_and_subgroups:
                db.insert_record('journal_lessoningroup',
                                 {
                                     "lesson_id": lesson_id,
                                     "group_id": group_id,
                                     "subgroup_number": subgroup_number,
                                 })
        lessons_data.apply(add_lesson, axis=1)

    @staticmethod
    def insert_control_point(date: datetime.date, max_score: float, discipline_id: int):
        control_point_id = db.insert_record('journal_controlpoint',
                                            {
                                                "discipline_id": discipline_id,
                                                "date": date,
                                                "max_score": max_score
                                            })
        return control_point_id

    @staticmethod
    def import_control_points_from_CSV(filename: str, discipline_id: int):
        control_points_data = pd.read_csv(filename, sep=';', header=0)
        control_points_data = control_points_data.dropna(how='all')
        control_points_data.fillna('', inplace=True)
        control_points_data["max_score"] = control_points_data["max_score"].astype("int32")
        control_points_data["date"] = pd.to_datetime(
            control_points_data['date'], format='%d.%m.%Y')
        # print(control_points_data)

        def add_control_point(row):
            actions.insert_control_point(row['date'], row['max_score'], discipline_id)
        control_points_data.apply(add_control_point, axis=1)

    @staticmethod
    def init_attendance(discipline_id: int, groups_and_subgroups: Tuple[Tuple[int, int]], max_grade: int):
        for group_id, subgroup_number in groups_and_subgroups:
            for row in db.select_iterator(
                """
                    SELECT journal_studyingstudent.id, journal_lessoningroup.id 
                    FROM journal_studyingstudent, journal_lessoningroup 
                    WHERE journal_studyingstudent.group_id = %s 
                        AND journal_lessoningroup.group_id = %s 
                        AND journal_studyingstudent.subgroup_number = %s 
                        AND journal_lessoningroup.subgroup_number = %s; 
                """, (group_id, group_id, subgroup_number, subgroup_number)):
                studying_student_id, lessoningroup_id = row
                db.insert_record('journal_attendance',
                                 {
                                     "studying_student_id": studying_student_id,
                                     "lesson_in_group_id": lessoningroup_id,
                                     "mark": "",
                                     "grade": max_grade,
                                 })

    @staticmethod
    def init_progress(discipline_id: int, groups_and_subgroups: Tuple[Tuple[int, int]]):
        for group_id, subgroup_number in groups_and_subgroups:
            for row in db.select_iterator(
                """
                    SELECT journal_studyingstudent.id, journal_taskingroup.id 
                    FROM journal_studyingstudent, journal_taskingroup 
                    WHERE journal_studyingstudent.group_id = %s 
                        AND journal_taskingroup.group_id = %s 
                        AND journal_studyingstudent.subgroup_number = %s 
                        AND journal_taskingroup.subgroup_number = %s; 
                """, (group_id, group_id, subgroup_number, subgroup_number)):
                studying_student_id, task_in_group_id = row
                db.insert_record('journal_progress',
                                 {
                                     "studying_student_id": studying_student_id,
                                     "task_in_group_id": task_in_group_id,
                                     "passed": False,
                                 })

    @staticmethod
    def init_rating(discipline_id: int):
        for row in db.select_iterator(
            """
                SELECT journal_studyingstudent.id, journal_controlpoint.id 
                FROM journal_studyingstudent, journal_controlpoint
                WHERE journal_studyingstudent.discipline_id = %s 
                AND journal_controlpoint.discipline_id = %s; 
            """, (discipline_id, discipline_id)):
            studying_student_id, control_point_id = row
            db.insert_record('journal_rating',
                             {
                                 "studying_student_id": studying_student_id,
                                 "control_point_id": control_point_id,
                                 "score": 0,
                             })
