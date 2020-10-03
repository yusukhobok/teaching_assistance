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
              "journal_controlpoint",
              "journal_lessoningroup",
              "journal_lesson",
              "journal_taskingroup",
              "journal_task",
              "journal_studyingstudent",
              "journal_student",
              "journal_discipline",
              "journal_group",
              "journal_semester",
              )

    ACADEMIC_YEARS = ('2016/2017', '2017/2018', '2018/2019',
                      '2019/2020', '2020/2021', '2021/2022', '2022/2023')

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
        for table in db.TABLES:
            db.apply_to_db(SQL(f"DELETE FROM {table}"))


    @staticmethod
    def clear_semester(semester_id: int):
        db.apply_to_db(SQL("DELETE FROM journal_semester WHERE id = '%s'"), semester_id)


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

        # for row in db.select_iterator(SQL(f"SELECT * FROM {table_name} ")):
        #     print(row)

        res = db.select_one_from_db(
            SQL(f"SELECT id FROM {table_name} WHERE {template_fields_values}"))
        return res[0]
