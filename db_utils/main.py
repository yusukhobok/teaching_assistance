import datetime
import os
import pandas as pd
import psycopg2
from contextlib import closing
from psycopg2.sql import SQL
from typing import Tuple, Dict, Sequence


class db():
    SETTINGS = {
        'dbname': 'teaching_assistance',
        'user': 'yuri',
        'password': 'yurist',
        'host': '127.0.0.1',
        'port': '5432',
    }

    TABLES = ("journal_rating",
              "journal_progress",
              "journal_attendance",
              "journal_controlpoints",
              "journal_lessoningroup",
              "journal_lesson",
              "journal_taskingroup",
              "journal_task",
              "journal_discipline",
              "journal_studentingroup",
              "journal_student",
              "journal_group",
              "journal_semester",
              )

    @staticmethod
    def apply_to_db(*args):
        with closing(psycopg2.connect(**db.SETTINGS)) as conn:
            with conn.cursor() as cursor:
                cursor.execute(*args)
                conn.commit()

    @staticmethod
    def select_one_from_db(*args):
        with closing(psycopg2.connect(**db.SETTINGS)) as conn:
            with conn.cursor() as cursor:
                cursor.execute(*args)
                return cursor.fetchone()

    @staticmethod
    def select_all_from_db(*args):
        with closing(psycopg2.connect(**db.SETTINGS)) as conn:
            with conn.cursor() as cursor:
                cursor.execute(*args)
                return cursor.fetchall()

    @staticmethod
    def select_iterator(*args):
        with closing(psycopg2.connect(**db.SETTINGS)) as conn:
            with conn.cursor() as cursor:
                cursor.execute(*args)
                for row in cursor:
                    yield row

    @staticmethod
    def clear_all():
        with closing(psycopg2.connect(**db.SETTINGS)) as conn:
            with conn.cursor() as cursor:
                for table in db.TABLES:
                    db.apply_to_db(SQL(f"DELETE FROM {table}"))

    @staticmethod
    def insert_record(table_name: str, params: dict):
        keys = list(params.keys())
        values = list(params.values())
        keys_values_list = [f"{key}='{value}'" for key,
                            value in zip(params.keys(), params.values())]

        template_fields = ", ".join(keys)
        template_values = ", ".join(('%s',)*len(values))
        template_fields_values = "AND ".join(keys_values_list)

        db.apply_to_db(SQL(
            f"INSERT INTO {table_name} ({template_fields}) VALUES ({template_values})"), values)

        for row in db.select_iterator(SQL(f"SELECT * FROM {table_name} ")):
            print(row)

        res = db.select_one_from_db(
            SQL(f"SELECT id FROM {table_name} WHERE {template_fields_values}"))
        return res[0]


def insert_semester(academic_year: str, season: int):
    ACADEMIC_YEARS = ('2016/2017', '2017/2018', '2018/2019',
                      '2019/2020', '2020/2021', '2021/2022', '2022/2023')
    if academic_year not in ACADEMIC_YEARS:
        raise ValueError("Academic year is incorrect")
    if season not in (1, 2):
        raise ValueError("Season must be 1 or 2")
    semester_id = db.insert_record('journal_semester',
                                   {
                                       "academic_year": academic_year,
                                       "season": season
                                   })
    return semester_id


def insert_group(group_number: str, course_number: int, semester_id: int):
    group_id = db.insert_record('journal_group',
                                {
                                    "group_number": group_number,
                                    "course_number": course_number,
                                    "semester_id": semester_id
                                })
    return group_id


def insert_student(name: str, grade_book_number: str, email: str = "", phone: str = "", profile: str = "", comments: str = "", expelled: bool = False):
    student_id = db.insert_record('journal_student',
                                  {
                                      "name": name,
                                      "grade_book_number": grade_book_number,
                                      "email": email,
                                      "phone": phone,
                                      "profile": profile,
                                      "comments": comments,
                                      "expelled": expelled
                                  })
    return student_id


def import_students_from_CSV(filename: str, group_id: int):
    students_data = pd.read_csv(filename, sep=';', header=0)
    students_data.fillna('', inplace=True)
    print(students_data)

    def add_student(row):
        student_id = insert_student(row['name'], row['grade_book_number'],
                                    row['email'], row['phone'], row['profile'], row['comments'])
        db.insert_record('journal_studentingroup',
                         {
                             "student_id": student_id,
                             "group_id": group_id,
                             "subgroup_number": row['subgroup_number']
                         })
    students_data.apply(add_student, axis=1)


def insert_discipline(name: str, short_name: str, semester_id: int):
    discipline_id = db.insert_record('journal_discipline',
                                     {
                                         "name": name,
                                         "short_name": short_name,
                                         "semester_id": semester_id
                                     })
    return discipline_id


def insert_task(deadline: str, topic: str, abbreviation: str, task_kind: str, comments: str, discipline_id: int):
    TASK_KINDS = ("LB", "PR", "KONTR", "TEST", "RGR", "KR",
                  "KP", "SECTION", "ALLOW", "ZACHET", "EXAM")
    if task_kind not in TASK_KINDS:
        raise ValueError("Task kind is incorrect")
    task_id = db.insert_record('journal_task',
                               {
                                   "discipline_id": discipline_id,
                                   "deadline": deadline,
                                   "topic": topic,
                                   "abbreviation": abbreviation,
                                   "task_kind": task_kind,
                                   "comments": comments
                               })
    return task_id


def import_tasks_from_CSV(filename: str, discipline_id: int, groups_and_subgroups: Tuple[Tuple[int, int]]):
    tasks_data = pd.read_csv(filename, sep=';', header=0)
    tasks_data.fillna('', inplace=True)
    tasks_data["date_plan"] = pd.to_datetime(
        tasks_data['deadline'], format='%d.%m.%Y')
    print(tasks_data)

    def add_task(row):
        task_id = insert_task(row['deadline'], row['topic'], row['abbreviation'],
                              row['task_kind'], row['comments'], discipline_id)
        for group_id, subgroup_number in groups_and_subgroups:
            db.insert_record('journal_taskingroup',
                             {
                                 "task_id": task_id,
                                 "group_id": group_id,
                                 "subgroup_number": subgroup_number,
                                 "task_coef": row['task_coef']
                             })
    tasks_data.apply(add_task, axis=1)


def insert_lesson(date_plan: datetime.date, topic: str, abbreviation: str, lesson_kind: str, comments: str, discipline_id: int):
    TASK_LESSONS = ("LK", "PR", "LR", "CONS", "EXAM")
    if lesson_kind not in TASK_LESSONS:
        raise ValueError("Lesson kind is incorrect")
    lesson_id = db.insert_record('journal_lesson',
                                 {
                                     "discipline_id": discipline_id,
                                     "date_plan": date_plan,
                                     "topic": topic,
                                     "abbreviation": abbreviation,
                                     "lesson_kind": lesson_kind,
                                     "comments": comments
                                 })
    return lesson_id


def import_lessons_from_CSV(filename: str, discipline_id: int, groups_and_subgroups: Tuple[Tuple[int, int]], lesson_coef: int):
    lessons_data = pd.read_csv(filename, sep=';', header=0)
    lessons_data.fillna('', inplace=True)
    lessons_data["date_plan"] = pd.to_datetime(
        lessons_data['date_plan'], format='%d.%m.%Y')
    print(lessons_data)

    def add_lesson(row):
        lesson_id = insert_lesson(row['date_plan'], row['topic'], row['abbreviation'],
                                  row['lesson_kind'], row['comments'], discipline_id)
        for group_id, subgroup_number in groups_and_subgroups:
            db.insert_record('journal_lessoningroup',
                             {
                                 "lesson_id": lesson_id,
                                 "group_id": group_id,
                                 "subgroup_number": subgroup_number,
                                 "lesson_coef": lesson_coef
                             })
    lessons_data.apply(add_lesson, axis=1)


def insert_control_point(date: datetime.date, max_score: float, discipline_id: int):
    control_point_id = db.insert_record('journal_controlpoints',
                                        {
                                            "discipline_id": discipline_id,
                                            "date": date,
                                            "max_score": max_score
                                        })
    return control_point_id


def import_control_points_from_CSV(filename: str, discipline_id: int, max_score: float):
    control_points_data = pd.read_csv(filename, sep=';', header=0)
    control_points_data.fillna('', inplace=True)
    control_points_data["date"] = pd.to_datetime(
        control_points_data['date'], format='%d.%m.%Y')
    print(control_points_data)

    def add_control_point(row):
        insert_control_point(row['date'], row['max_score'], discipline_id)
    control_points_data.apply(add_control_point, axis=1)


def init_attendance():
    pass


def init_progress():
    pass


def init_rating():
    pass


if __name__ == "__main__":
    db.clear_all()
    semester_id = insert_semester(academic_year="2019/2020", season=2)

    group_id = insert_group(
        group_number="931", course_number=3, semester_id=semester_id)
    import_students_from_CSV(
        filename="db_utils/data/students.csv", group_id=group_id)
    discipline_id = insert_discipline(
        name="Web-дизайн", short_name="Web-дизайн", semester_id=semester_id)
    groups_and_subgroups = ((group_id, 1), (group_id, 2))
    import_tasks_from_CSV(filename="db_utils/data/tasks.csv",
                          discipline_id=discipline_id, groups_and_subgroups=groups_and_subgroups)
