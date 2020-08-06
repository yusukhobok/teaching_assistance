from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class Semester(models.Model):
    ACADEMIC_YEARS = (
        ('2020/2021', '2020/2021'),
        ('2021/2022', '2021/2022'),
        ('2022/2023', '2022/2023'),
    )
    SEASONS = ((1, 'Осенний семестр'), (2, 'Весенний семестр'))
    academic_year = models.CharField(
        max_length=9, choices=ACADEMIC_YEARS, verbose_name="Учебный год")
    season = models.SmallIntegerField(
        choices=SEASONS, verbose_name="Вид семестра")

    def __str__(self):
        return f"{self.academic_year} уч. г.; {self.season}-й семестр"


class Student(models.Model):
    first_name = models.CharField(max_length=100, verbose_name="Имя")
    middle_name = models.CharField(max_length=100, verbose_name="Отчество")
    last_name = models.CharField(max_length=100, verbose_name="Фамилия")
    grade_book_number = models.CharField(
        max_length=50, verbose_name="Номер зачетной книжки")
    email = models.EmailField(verbose_name="E-mail", blank=True)
    phone = models.CharField(max_length=50, verbose_name="Телефон", blank=True)
    profile = models.URLField(verbose_name="Ссылка на профиль", blank=True)
    photo = models.ImageField(verbose_name="Фото", blank=True)
    comments = models.TextField(verbose_name="Комментарии", blank=True)
    expelled = models.BooleanField(verbose_name="Отчислен", default=False)

    @property
    def full_name(self):
        return f"{self.last_name} {self.first_name} {self.middle_name}"

    def __str__(self):
        return self.full_name


class Group(models.Model):
    group_number = models.CharField(max_length=10, verbose_name="Номер группы")
    course_number = models.SmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(6)], verbose_name="Курс")
    semester = models.ForeignKey('Semester', on_delete=models.CASCADE)
    head_student = models.ForeignKey('Student', on_delete=models.CASCADE)


class StudentInGroup(models.Model):
    student = models.ForeignKey('Student', on_delete=models.CASCADE)
    group = models.ForeignKey('Group', on_delete=models.CASCADE)
    subgroup_number = models.SmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(2)], verbose_name="Номер подгруппы", default=1)


class Discipline(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название")
    semester = models.ForeignKey('Semester', on_delete=models.CASCADE)


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
    date_plan = models.DateField(verbose_name="Дата (план)")
    date_fact = models.DateField(verbose_name="Дата (факт)")
    topic = models.CharField(max_length=100, verbose_name="Тема")
    abbreviation = models.CharField(max_length=20, verbose_name="Сокращение")
    task_kind = models.CharField(
        max_length=10, choices=TASK_KINDS, verbose_name="Вид занятия")
    comments = models.TextField(verbose_name="Комментарии")


class TaskInGroup(models.Model):
    task = models.ForeignKey("Task", on_delete=models.CASCADE)
    group = models.ForeignKey("Group", on_delete=models.CASCADE)
    subgroup_number = models.SmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(2)], verbose_name="Номер подгруппы", default=1)
    attendance_coef = models.FloatField(
        validators=[MinValueValidator(0), ], verbose_name="Коэффициент за задание")


class Lesson(models.Model):
    LESSON_KINDS = (
        ("LK", "Лекция"),
        ("PR", "Практическое занятие"),
        ("LR", "Лабораторное занятие"),
        ("CONS", "Консультация"),
        ("EXAM", "Экзамен")
    )
    discipline = models.ForeignKey('Discipline', on_delete=models.CASCADE)
    deadline = models.DateField(verbose_name="Дата (план)")
    topic = models.CharField(max_length=100, verbose_name="Тема")
    abbreviation = models.CharField(max_length=20, verbose_name="Сокращение")
    lesson_kind = models.CharField(
        max_length=10, choices=LESSON_KINDS, verbose_name="Вид задания")
    comments = models.TextField(verbose_name="Комментарии")


class LessonInGroup(models.Model):
    lesson = models.ForeignKey("Lesson", on_delete=models.CASCADE)
    group = models.ForeignKey("Group", on_delete=models.CASCADE)
    subgroup_number = models.SmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(2)], verbose_name="Номер подгруппы", default=1)
    lesson_coef = models.FloatField(
        validators=[MinValueValidator(0), ], verbose_name="Коэффициент за занятие")


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
        max_length=10, choices=ATTENDANCE_MARKS, verbose_name="Отметка о присутствии")
    grade = models.FloatField(validators=[MinValueValidator(
        0), ], verbose_name="Балл за работу на занятии")


class Progress(models.Model):
    student_in_group = models.ForeignKey(
        "StudentInGroup", on_delete=models.CASCADE)
    task = models.ForeignKey("Task", on_delete=models.CASCADE)    
    passed = models.BooleanField(verbose_name="Сдано", default=False)
    grade = models.FloatField(validators=[MinValueValidator(
        0), ], verbose_name="Оценка за задание")
    delivery_date = models.DateField(verbose_name="Дата сдачи")


