from db_actions import actions


class init_db():
    academic_year = "2019/2020"
    season = 2
    semester_id = None

    @staticmethod
    def clear_all():
        answer = input(
            "This command delete all data from the database. Print Yes if you are sure.")
        if answer == "Yes":
            actions.clear_all()

    @staticmethod
    def add_semester():
        init_db.semester_id = actions.insert_semester(
            academic_year=init_db.academic_year, season=init_db.season)

    @staticmethod
    def get_semester():
        init_db.semester_id = actions.get_semester(
            academic_year=init_db.academic_year, season=init_db.season)

    @staticmethod
    def add_web_design():
        semester_id = init_db.semester_id
        if semester_id is None:
            raise Exception("semester_id is not defined")

        group_id = actions.insert_group(
            group_number="931", course_number=3, semester_id=semester_id)
        discipline_id = actions.insert_discipline(
            name="Web-дизайн", short_name="Web-дизайн", semester_id=semester_id)
        actions.import_students_from_CSV(
            filename="db_utils/data/2019-2020/web-дизайн/students.csv", group_id=group_id, discipline_id=discipline_id)
        groups_and_subgroups = ((group_id, 1), (group_id, 2))
        actions.import_tasks_from_CSV(filename="db_utils/data/2019-2020/web-дизайн/tasks.csv",
                                      discipline_id=discipline_id, groups_and_subgroups=groups_and_subgroups)
        actions.import_lessons_from_CSV(filename="db_utils/data/2019-2020/web-дизайн/lessons.csv",
                                        discipline_id=discipline_id, groups_and_subgroups=groups_and_subgroups, lesson_coef=1)
        actions.import_control_points_from_CSV(
            filename="db_utils/data/2019-2020/web-дизайн/controlpoints.csv", discipline_id=discipline_id)
        actions.init_attendance(discipline_id=discipline_id,
                                groups_and_subgroups=groups_and_subgroups, max_grade=10)
        actions.init_progress(discipline_id=discipline_id,
                              groups_and_subgroups=groups_and_subgroups)
        actions.init_rating(discipline_id=discipline_id)

    @staticmethod
    def add_porkp():
        semester_id = init_db.semester_id
        if semester_id is None:
            raise Exception("semester_id is not defined")
        discipline_id = actions.insert_discipline(
            name="Программное обеспечение расчетов конструкций железнодорожного пути", short_name="ПОРКП", semester_id=semester_id)
        group_id_445 = actions.insert_group(
            group_number="445", course_number=4, semester_id=semester_id)
        actions.import_students_from_CSV(
            filename="db_utils/data/2019-2020/ПОРКП/students_445.csv", group_id=group_id_445, discipline_id=discipline_id)
        group_id_446 = actions.insert_group(
            group_number="446", course_number=4, semester_id=semester_id)
        actions.import_students_from_CSV(
            filename="db_utils/data/2019-2020/ПОРКП/students_446.csv", group_id=group_id_446, discipline_id=discipline_id)

        groups_and_subgroups_445_446_all = (
            (group_id_445, 1), (group_id_445, 2), (group_id_446, 1), (group_id_446, 2))
        groups_and_subgroups_445_446_half = (
            (group_id_445, 1), (group_id_446, 1))
        groups_and_subgroups_445_all = ((group_id_445, 1), (group_id_445, 2))
        groups_and_subgroups_446_all = ((group_id_446, 1), (group_id_446, 2))
        groups_and_subgroups_445_half = ((group_id_445, 1), )
        groups_and_subgroups_446_half = ((group_id_446, 1), )

        actions.import_tasks_from_CSV(filename="db_utils/data/2019-2020/ПОРКП/tasks_445_446_half.csv",
                                      discipline_id=discipline_id, groups_and_subgroups=groups_and_subgroups_445_446_half)
        actions.import_tasks_from_CSV(filename="db_utils/data/2019-2020/ПОРКП/tasks_445_446_all.csv",
                                      discipline_id=discipline_id, groups_and_subgroups=groups_and_subgroups_445_446_all)

        actions.import_lessons_from_CSV(filename="db_utils/data/2019-2020/ПОРКП/lessons_445_446_all.csv",
                                        discipline_id=discipline_id, groups_and_subgroups=groups_and_subgroups_445_446_all, lesson_coef=1)
        actions.import_lessons_from_CSV(filename="db_utils/data/2019-2020/ПОРКП/lessons_445_all.csv",
                                        discipline_id=discipline_id, groups_and_subgroups=groups_and_subgroups_445_all, lesson_coef=1)
        actions.import_lessons_from_CSV(filename="db_utils/data/2019-2020/ПОРКП/lessons_445_half.csv",
                                        discipline_id=discipline_id, groups_and_subgroups=groups_and_subgroups_445_half, lesson_coef=1)
        actions.import_lessons_from_CSV(filename="db_utils/data/2019-2020/ПОРКП/lessons_446_all.csv",
                                        discipline_id=discipline_id, groups_and_subgroups=groups_and_subgroups_446_all, lesson_coef=1)
        actions.import_lessons_from_CSV(filename="db_utils/data/2019-2020/ПОРКП/lessons_446_half.csv",
                                        discipline_id=discipline_id, groups_and_subgroups=groups_and_subgroups_446_half, lesson_coef=1)

        actions.import_control_points_from_CSV(
            filename="db_utils/data/2019-2020/ПОРКП/controlpoints.csv", discipline_id=discipline_id)

        actions.init_attendance(discipline_id=discipline_id,
                                groups_and_subgroups=groups_and_subgroups_445_446_all, max_grade=10)
        actions.init_progress(discipline_id=discipline_id,
                              groups_and_subgroups=groups_and_subgroups_445_446_all)
        actions.init_rating(discipline_id=discipline_id)


if __name__ == "__main__":
    init_db.add_semester()
    init_db.add_web_design()
    # init_db.get_semester()
    init_db.add_porkp()
