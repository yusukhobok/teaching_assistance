from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class Semester(models.Model):
    ACADEMIC_YEARS = (
        ("2016/2017", "2016/2017"),
        ("2017/2018", "2017/2018"),
        ("2018/2019", "2018/2019"),
        ("2019/2020", "2019/2020"),
        ("2020/2021", "2020/2021"),
        ("2021/2022", "2021/2022"),
        ("2022/2023", "2022/2023"),
    )
    SEASONS = ((1, "Осенний семестр"), (2, "Весенний семестр"))
    academic_year = models.CharField(
        max_length=9, choices=ACADEMIC_YEARS, verbose_name="Учебный год")
    season = models.SmallIntegerField(
        choices=SEASONS, verbose_name="Вид семестра")
    is_current = models.BooleanField(verbose_name="Текущий", default=False)

    class Meta:
        ordering = ["academic_year", "season"]
        constraints = [
            models.UniqueConstraint(
                fields=["academic_year", "season"], name="unique semester"),
        ]
        verbose_name = "Семестр"
        verbose_name_plural = "Семестры"

    def __str__(self):
        return f"{self.academic_year} уч. г.; {self.season}-й сем."


class Student(models.Model):
    first_name = models.CharField(max_length=100, verbose_name="Имя")
    middle_name = models.CharField(max_length=100, verbose_name="Отчество")
    last_name = models.CharField(max_length=100, verbose_name="Фамилия")
    last_name_with_stress = models.CharField(max_length=100, verbose_name="Фамилия с ударением", null=True)
    grade_book_number = models.CharField(
        max_length=50, verbose_name="Номер зачетной книжки")
    email = models.EmailField(verbose_name="E-mail", blank=True, null=True)
    phone = models.CharField(max_length=50, verbose_name="Телефон", null=True)
    profile = models.URLField(
        verbose_name="Ссылка на профиль", blank=True, null=True)
    photo = models.ImageField(verbose_name="Фото", blank=True, null=True)
    comments = models.TextField(verbose_name="Комментарии", null=True)
    expelled = models.BooleanField(verbose_name="Отчислен", default=False)

    class Meta:
        ordering = ["last_name", "first_name", "middle_name", "grade_book_number"]
        constraints = [
            models.UniqueConstraint(
                fields=["last_name", "first_name", "middle_name", "grade_book_number"], name="unique student"),
        ]
        verbose_name = "Студент"
        verbose_name_plural = "Студенты"

    @property
    def full_name(self):
        return f"{self.last_name} {self.first_name} {self.middle_name}"

    @property
    def surname_and_initials(self):
        return f"{self.last_name} {self.first_name[0]}. {self.middle_name[0]}."

    def __str__(self):
        return self.surname_and_initials if not self.expelled else f"{self.surname_and_initials} (отчислен)"

    # def natural_key(self):
    #     model_dict = model_to_dict(self, fields=[field.name for field in self._meta.fields if field.name != "photo"])
    #     return model_dict


class Group(models.Model):
    group_number = models.CharField(max_length=10, verbose_name="Номер группы")
    course_number = models.SmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(6)], verbose_name="Курс")
    semester = models.ForeignKey("Semester", on_delete=models.CASCADE)
    is_current = models.BooleanField(verbose_name="Текущая", default=False)

    class Meta:
        ordering = ["semester", "group_number"]
        constraints = [
            models.UniqueConstraint(
                fields=["group_number", "semester"], name="unique group"),
        ]
        verbose_name = "Группа"
        verbose_name_plural = "Группы"

    def __str__(self):
        return f"гр. {self.group_number} ({self.semester})"


class StudyingStudent(models.Model):
    student = models.ForeignKey("Student", on_delete=models.CASCADE)
    group = models.ForeignKey("Group", on_delete=models.CASCADE)
    subgroup_number = models.SmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(2)], verbose_name="Номер подгруппы", default=1)
    discipline = models.ForeignKey("Discipline", on_delete=models.CASCADE)
    is_head = models.BooleanField("Head", default=False)

    class Meta:
        ordering = ["discipline", "group", "student"]
        verbose_name = "Студент учащийся"
        verbose_name_plural = "Студенты учащиеся"

    def __str__(self):
        head_marker = "!!" if self.is_head else ""
        return f"{self.student} {head_marker} - {self.group} (подгруппа {self.subgroup_number}) - {self.discipline}"


class Discipline(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название")
    short_name = models.CharField(
        max_length=20, verbose_name="Сокращенное название")
    semester = models.ForeignKey("Semester", on_delete=models.CASCADE)
    is_current = models.BooleanField(verbose_name="Текущая", default=False)

    class Meta:
        ordering = ["name"]
        constraints = [
            models.UniqueConstraint(
                fields=["name", "semester"], name="unique discipline"),
        ]
        verbose_name = "Дисциплина"
        verbose_name_plural = "Дисциплины"

    def __str__(self):
        return f"{self.short_name} ({self.semester})"


class Task(models.Model):
    TASK_KINDS = (("LB", "Лабораторная работа"),
                  ("PR", "Практическая работа"),
                  ("KONTR", "Контрольная работа"),
                  ("TEST", "Тест"),
                  ("RGR", "РГР"),
                  ("KR", "Курсовая работа"),
                  ("KP", "Курсовой проект"),
                  ("SECTION", "Раздел"),
                  ("ALLOW", "Допуск"),
                  ("ZACHET", "Зачет"),
                  ("EXAM", "Экзамен"))
    discipline = models.ForeignKey("Discipline", on_delete=models.CASCADE)
    deadline = models.DateField(verbose_name="Дедлайн")
    topic = models.CharField(max_length=1000, verbose_name="Тема")
    abbreviation = models.CharField(max_length=20, verbose_name="Сокращение")
    task_kind = models.CharField(
        max_length=10, choices=TASK_KINDS, verbose_name="Вид занятия")
    comments = models.TextField(verbose_name="Комментарии")
    task_coef = models.FloatField(
        validators=[MinValueValidator(0), ], verbose_name="Коэффициент за задание", default=1.0)

    class Meta:
        ordering = ["discipline", "deadline"]
        verbose_name = "Задание"
        verbose_name_plural = "Задания"

    def __str__(self):
        return f"{self.abbreviation} - {self.discipline}"


class TaskInGroup(models.Model):
    task = models.ForeignKey("Task", on_delete=models.CASCADE)
    group = models.ForeignKey("Group", on_delete=models.CASCADE)
    subgroup_number = models.SmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(2)], verbose_name="Номер подгруппы", default=1)

    class Meta:
        ordering = ["task", "group", "subgroup_number"]
        verbose_name = "Задание в группе"
        verbose_name_plural = "Задания в группах"

    def __str__(self):
        return f"{self.task} - {self.group} ({self.subgroup_number})"


class Lesson(models.Model):
    LESSON_KINDS = (
        ("LK", "Лекция"),
        ("PR", "Практическое занятие"),
        ("LB", "Лабораторное занятие"),
        ("CONS", "Консультация"),
        ("EXAM", "Экзамен")
    )
    discipline = models.ForeignKey("Discipline", on_delete=models.CASCADE)
    date_plan = models.DateField(verbose_name="Дата (план)")
    date_fact = models.DateField(verbose_name="Дата (факт)")
    topic = models.CharField(max_length=1000, verbose_name="Тема")
    abbreviation = models.CharField(max_length=20, verbose_name="Сокращение")
    lesson_kind = models.CharField(
        max_length=10, choices=LESSON_KINDS, verbose_name="Вид задания")
    comments = models.TextField(verbose_name="Комментарии")
    lesson_coef = models.FloatField(
        validators=[MinValueValidator(0), ], verbose_name="Коэффициент за занятие", default=1.0)

    class Meta:
        ordering = ["discipline", "date_plan"]
        verbose_name = "Занятие"
        verbose_name_plural = "Занятия"

    def __str__(self):
        return f"{self.abbreviation} ({self.date_fact}; {self.lesson_kind}) - {self.discipline}"


class LessonInGroup(models.Model):
    lesson = models.ForeignKey("Lesson", on_delete=models.CASCADE)
    group = models.ForeignKey("Group", on_delete=models.CASCADE)
    subgroup_number = models.SmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(2)], verbose_name="Номер подгруппы", default=1)

    class Meta:
        ordering = ["lesson", "group", "subgroup_number"]
        verbose_name = "Занятие в группе"
        verbose_name_plural = "Занятия в группах"

    def __str__(self):
        return f"{self.lesson} - {self.group} ({self.subgroup_number})"


class Attendance(models.Model):
    ATTENDANCE_MARKS = (
        ("", ""),
        ("+", "Был"),
        ("н", "Не был"),
        ("оп", "Опоздал"),
        ("н(у)", "Не был по уважительной причине")
    )

    studying_student = models.ForeignKey(
        "StudyingStudent", on_delete=models.CASCADE)
    lesson_in_group = models.ForeignKey(
        "LessonInGroup", on_delete=models.CASCADE)
    mark = models.CharField(
        max_length=10, choices=ATTENDANCE_MARKS, verbose_name="Отметка о присутствии", default="")
    grade = models.FloatField(validators=[MinValueValidator(
        0), ], verbose_name="Балл за работу на занятии", default=10.0)

    class Meta:
        ordering = ["studying_student", "lesson_in_group"]
        verbose_name = "Посещаемость"
        verbose_name_plural = "Посещаемость"

    def __str__(self):
        return f"{self.studying_student} ::: {self.lesson_in_group}"


class Progress(models.Model):
    studying_student = models.ForeignKey(
        "StudyingStudent", on_delete=models.CASCADE)
    task_in_group = models.ForeignKey("TaskInGroup", on_delete=models.CASCADE)
    passed = models.BooleanField(verbose_name="Сдано", default=False)
    grade = models.FloatField(validators=[MinValueValidator(
        0), ], verbose_name="Оценка за задание", blank=True, null=True)
    delivery_date = models.DateField(verbose_name="Дата сдачи", null=True)

    class Meta:
        ordering = ["studying_student", "task_in_group"]
        verbose_name = "Успеваемость"
        verbose_name_plural = "Успеваемость"

    def __str__(self):
        return f"{self.studying_student} ::: {self.task_in_group}"


class ControlPoint(models.Model):
    discipline = models.ForeignKey("Discipline", on_delete=models.CASCADE)
    date = models.DateField(verbose_name="Дата")
    max_score = models.FloatField(validators=[MinValueValidator(
        0), ], verbose_name="Максимальный рейтинг")

    class Meta:
        ordering = ["date"]
        constraints = [
            models.UniqueConstraint(
                fields=["discipline", "date"], name="unique control point"),
        ]
        verbose_name = "Контрольная точка"
        verbose_name_plural = "Контрольные точки"

    def __str__(self):
        return f"{self.date} ({self.discipline})"


class Rating(models.Model):
    studying_student = models.ForeignKey(
        "StudyingStudent", on_delete=models.CASCADE)
    control_point = models.ForeignKey(
        "ControlPoint", on_delete=models.CASCADE)
    score = models.FloatField(validators=[MinValueValidator(
        0), ], verbose_name="Рейтинг")

    class Meta:
        verbose_name = "Рейтинг"
        verbose_name_plural = "Рейтинг"

    def __str__(self):
        return f"{self.studying_student} ::: {self.control_point}"
