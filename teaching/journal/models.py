from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class Semester(models.Model):
    ACADEMIC_YEARS = (
        ('2016/2017', '2016/2017'),
        ('2017/2018', '2017/2018'),
        ('2018/2019', '2018/2019'),
        ('2019/2020', '2019/2020'),
        ('2020/2021', '2020/2021'),
        ('2021/2022', '2021/2022'),
        ('2022/2023', '2022/2023'),
    )
    SEASONS = ((1, 'Осенний семестр'), (2, 'Весенний семестр'))
    academic_year = models.CharField(
        max_length=9, choices=ACADEMIC_YEARS, verbose_name="Учебный год")
    season = models.SmallIntegerField(
        choices=SEASONS, verbose_name="Вид семестра")

    class Meta:
        ordering = ["academic_year", "season"]
        constraints = [
            models.UniqueConstraint(fields= ['academic_year','season']),
        ]
        verbose_name = "Семестр"
        verbose_name_plural = "Семестры"

    def __str__(self):
        return f"{self.academic_year} уч. г.; {self.season}-й семестр"


class Student(models.Model):
    name = models.CharField(max_length=200, verbose_name="ФИО")
    # first_name = models.CharField(max_length=100, verbose_name="Имя")
    # middle_name = models.CharField(max_length=100, verbose_name="Отчество")
    # last_name = models.CharField(max_length=100, verbose_name="Фамилия")
    grade_book_number = models.CharField(
        max_length=50, verbose_name="Номер зачетной книжки")
    email = models.EmailField(verbose_name="E-mail", blank=True, null=True)
    phone = models.CharField(max_length=50, verbose_name="Телефон")
    profile = models.URLField(verbose_name="Ссылка на профиль", blank=True, null=True)
    photo = models.ImageField(verbose_name="Фото", blank=True, null=True)
    comments = models.TextField(verbose_name="Комментарии")
    expelled = models.BooleanField(verbose_name="Отчислен", default=False)

    class Meta:
        ordering = ["name"]
        constraints = [
            models.UniqueConstraint(fields= ['name','grade_book_number']),
        ]
        verbose_name = "Студент"
        verbose_name_plural = "Студенты"

    # @property
    # def full_name(self):
    #     return f"{self.last_name} {self.first_name} {self.middle_name}"

    def __str__(self):
        return self.name


class Group(models.Model):
    group_number = models.CharField(max_length=10, verbose_name="Номер группы")
    course_number = models.SmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(6)], verbose_name="Курс")
    semester = models.ForeignKey('Semester', on_delete=models.CASCADE)
    head_student = models.ForeignKey('Student', on_delete=models.CASCADE)

    class Meta:
        ordering = ["group_number"]
        verbose_name = "Семестр"
        verbose_name_plural = "Семестры"

    def __str__(self):
        return f"группа {self.group_number}"


class StudentInGroup(models.Model):
    student = models.ForeignKey('Student', on_delete=models.CASCADE)
    group = models.ForeignKey('Group', on_delete=models.CASCADE)
    subgroup_number = models.SmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(2)], verbose_name="Номер подгруппы", default=1)


class Discipline(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название")
    semester = models.ForeignKey('Semester', on_delete=models.CASCADE)

    class Meta:
        ordering = ["name"]
        verbose_name = "Дисциплина"
        verbose_name_plural = "Дисциплины"

    def __str__(self):
        return f"{self.name}"


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
    discipline = models.ForeignKey('Discipline', on_delete=models.CASCADE)
    deadline = models.DateField(verbose_name="Дата (план)")
    topic = models.CharField(max_length=100, verbose_name="Тема")
    abbreviation = models.CharField(max_length=20, verbose_name="Сокращение")
    task_kind = models.CharField(
        max_length=10, choices=TASK_KINDS, verbose_name="Вид занятия")
    comments = models.TextField(verbose_name="Комментарии")

    class Meta:
        ordering = ["deadline"]
        verbose_name = "Задание"
        verbose_name_plural = "Задания"

    def __str__(self):
        return f"{self.abbreviation}"


class TaskInGroup(models.Model):
    task = models.ForeignKey("Task", on_delete=models.CASCADE)
    group = models.ForeignKey("Group", on_delete=models.CASCADE)
    subgroup_number = models.SmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(2)], verbose_name="Номер подгруппы", default=1)
    attendance_coef = models.FloatField(
        validators=[MinValueValidator(0), ], verbose_name="Коэффициент за задание", default=1.0)


class Lesson(models.Model):
    LESSON_KINDS = (
        ("LK", "Лекция"),
        ("PR", "Практическое занятие"),
        ("LR", "Лабораторное занятие"),
        ("CONS", "Консультация"),
        ("EXAM", "Экзамен")
    )
    discipline = models.ForeignKey('Discipline', on_delete=models.CASCADE)
    date_plan = models.DateField(verbose_name="Дата (план)")
    date_fact = models.DateField(verbose_name="Дата (факт)")
    topic = models.CharField(max_length=100, verbose_name="Тема")
    abbreviation = models.CharField(max_length=20, verbose_name="Сокращение")
    lesson_kind = models.CharField(
        max_length=10, choices=LESSON_KINDS, verbose_name="Вид задания")
    comments = models.TextField(verbose_name="Комментарии")

    class Meta:
        ordering = ["date_plan"]
        verbose_name = "Занятие"
        verbose_name_plural = "Занятия"

    def __str__(self):
        return f"{self.abbreviation}"


class LessonInGroup(models.Model):
    lesson = models.ForeignKey("Lesson", on_delete=models.CASCADE)
    group = models.ForeignKey("Group", on_delete=models.CASCADE)
    subgroup_number = models.SmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(2)], verbose_name="Номер подгруппы", default=1)
    lesson_coef = models.FloatField(
        validators=[MinValueValidator(0), ], verbose_name="Коэффициент за занятие", default=1.0)


class Attendance(models.Model):
    ATTENDANCE_MARKS = (
        ("", ""),
        ("+", "Был"),
        ("н", "Не был"),
        ("оп", "Опоздал"),
        ("н(у)", "Не был по уважительной причине")
    )

    student_in_group = models.ForeignKey(
        "StudentInGroup", on_delete=models.CASCADE)
    lesson = models.ForeignKey("Lesson", on_delete=models.CASCADE)
    mark = models.CharField(
        max_length=10, choices=ATTENDANCE_MARKS, verbose_name="Отметка о присутствии", default="")
    grade = models.FloatField(validators=[MinValueValidator(
        0), ], verbose_name="Балл за работу на занятии", default=10.0)

    class Meta:
        verbose_name = "Посещаемость"


class Progress(models.Model):
    student_in_group = models.ForeignKey(
        "StudentInGroup", on_delete=models.CASCADE)
    task = models.ForeignKey("Task", on_delete=models.CASCADE)
    passed = models.BooleanField(verbose_name="Сдано", default=False)
    grade = models.FloatField(validators=[MinValueValidator(
        0), ], verbose_name="Оценка за задание", blank=True, null=True)
    delivery_date = models.DateField(verbose_name="Дата сдачи", null=True)

    class Meta:
        verbose_name = "Успеваемость"


class ControlPoints(models.Model):
    discipline = models.ForeignKey('Discipline', on_delete=models.CASCADE)
    date = models.DateField(verbose_name="Дата")
    max_score = models.FloatField(validators=[MinValueValidator(
        0), ], verbose_name="Максимальный рейтинг")

    class Meta:
        ordering = ["date"]
        verbose_name = "Контрольная точка"
        verbose_name_plural = "Контрольные точки"

    def __str__(self):
        return f"{self.date} - {self.max_score}"


class Rating(models.Model):
    student_in_group = models.ForeignKey(
        'StudentInGroup', on_delete=models.CASCADE)
    control_point = models.ForeignKey(
        'ControlPoints', on_delete=models.CASCADE)
    score = models.FloatField(validators=[MinValueValidator(
        0), ], verbose_name="Рейтинг")

    class Meta:
        verbose_name = "Рейтинг"
