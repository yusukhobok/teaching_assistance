from .db_actions import actions


academic_year = "2019/2020"
season = 2
semester_id = None


def clear_all():
    answer = input(
        "This command delete all data from the database. Print Yes if you are sure.")
    if answer == "Yes":
        actions.clear_all()


def add_semester():
    global semester_id
    semester_id = actions.insert_semester(
        academic_year=academic_year, season=season)


def get_semester():
    global semester_id
    semester_id = get_semester(academic_year=academic_year, season=season)


def add_web_design():
    if semester_id is None: raise Exception("semester_id is not defined")
    group_id = insert_group(
        group_number="931", course_number=3, semester_id=semester_id)
    discipline_id = insert_discipline(
        name="Web-дизайн", short_name="Web-дизайн", semester_id=semester_id)
    import_students_from_CSV(
        filename="db_utils/data/2019-2020/web-дизайн/students.csv", group_id=group_id, discipline_id=discipline_id)
    groups_and_subgroups = ((group_id, 1), (group_id, 2))
    import_tasks_from_CSV(filename="db_utils/data/tasks.csv",
                          discipline_id=discipline_id, groups_and_subgroups=groups_and_subgroups)
    import_lessons_from_CSV(filename="db_utils/data/lessons.csv",
                            discipline_id=discipline_id, groups_and_subgroups=groups_and_subgroups, lesson_coef=1)
    import_control_points_from_CSV(
        filename="db_utils/data/2019-2020/web-дизайн/controlpoints.csv", discipline_id=discipline_id)
    init_attendance(discipline_id=discipline_id,
                    groups_and_subgroups=groups_and_subgroups, max_grade=10)
    init_progress(discipline_id=discipline_id,
                  groups_and_subgroups=groups_and_subgroups)
    init_rating(discipline_id=discipline_id)


def add_porkp():
    if semester_id is None: raise Exception("semester_id is not defined")
    discipline_id = insert_discipline(
        name="Программное обеспечение расчетов конструкций железнодорожного пути", short_name="ПОРКП", semester_id=semester_id)
    group_id_445 = insert_group(
        group_number="445", course_number=4, semester_id=semester_id)
    import_students_from_CSV(
        filename="db_utils/data/2019-2020/ПОРКП/students_445.csv", group_id=group_id_445, discipline_id=discipline_id)
    group_id_446 = insert_group(
        group_number="446", course_number=4, semester_id=semester_id)
    import_students_from_CSV(
        filename="db_utils/data/2019-2020/ПОРКП/students_446.csv", group_id=group_id_446, discipline_id=discipline_id)

    groups_and_subgroups_445_446_all = (
        (group_id_445, 1), (group_id_445, 2), (group_id_446, 1), (group_id_446, 2))
    groups_and_subgroups_445_446_half = ((group_id_445, 1), (group_id_446, 1))
    groups_and_subgroups_445_all = ((group_id_445, 1), (group_id_445, 2))
    groups_and_subgroups_446_all = ((group_id_446, 1), (group_id_446, 2))
    groups_and_subgroups_445_half = ((group_id_445, 1), )
    groups_and_subgroups_446_half = ((group_id_446, 1), )

    import_tasks_from_CSV(filename="db_utils/data/2019-2020/ПОРКП/tasks_445_446_half.csv",
                          discipline_id=discipline_id, groups_and_subgroups=groups_and_subgroups_445_446_half)
    import_tasks_from_CSV(filename="db_utils/data/2019-2020/ПОРКП/tasks_445_446_all.csv",
                          discipline_id=discipline_id, groups_and_subgroups=groups_and_subgroups_445_446_all)

    import_lessons_from_CSV(filename="db_utils/data/2019-2020/ПОРКП/lessons_445_446_all.csv",
                            discipline_id=discipline_id, groups_and_subgroups=groups_and_subgroups_445_446_all, lesson_coef=1)
    import_lessons_from_CSV(filename="db_utils/data/2019-2020/ПОРКП/lessons_445_all.csv",
                            discipline_id=discipline_id, groups_and_subgroups=groups_and_subgroups_445_all, lesson_coef=1)
    import_lessons_from_CSV(filename="db_utils/data/2019-2020/ПОРКП/lessons_445_half.csv",
                            discipline_id=discipline_id, groups_and_subgroups=groups_and_subgroups_445_half, lesson_coef=1)
    import_lessons_from_CSV(filename="db_utils/data/2019-2020/ПОРКП/lessons_446_all.csv",
                            discipline_id=discipline_id, groups_and_subgroups=groups_and_subgroups_446_all, lesson_coef=1)
    import_lessons_from_CSV(filename="db_utils/data/2019-2020/ПОРКП/lessons_446_half.csv",
                            discipline_id=discipline_id, groups_and_subgroups=groups_and_subgroups_446_half, lesson_coef=1)

    import_control_points_from_CSV(
        filename="db_utils/data/2019-2020/ПОРКП/controlpoints.csv", discipline_id=discipline_id)

    init_attendance(discipline_id=discipline_id,
                    groups_and_subgroups=groups_and_subgroups_445_446_all, max_grade=10)
    init_progress(discipline_id=discipline_id,
                  groups_and_subgroups=groups_and_subgroups_445_446_all)
    init_rating(discipline_id=discipline_id)





if __name__ == "__main__":




