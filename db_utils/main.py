import psycopg2
from contextlib import closing


SETTINGS = {
    'dbname': 'teaching_assistance',
    'user': 'yuri',
    'password': 'yurist',
    'host': '127.0.0.1',
    'port': '5432',
}


def apply_to_db(*args, **kwargs):
    with closing(psycopg2.connect(**SETTINGS)) as conn:
        with conn.cursor() as cursor:
            cursor.execute(*args, **kwargs)
            conn.commit()


def add_semester(academic_year, season):
    apply_to_db('INSERT INTO journal_semester (academic_year, season) VALUES (%s, %s)',
                (academic_year, season))


def add_student(name, grade_book_number, email, phone, profile, comments):
    apply_to_db('INSERT INTO journal_student (name, grade_book_number, email, phone, profile, comments) VALUES (%s, %s, %s, %s, %s, %s)',
                (name, grade_book_number, email, phone, profile, comments))


if __name__ == "__main__":
    # add_semester("2020/2021", "2")
    pass
