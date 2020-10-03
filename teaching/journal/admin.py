from django.contrib import admin

from .models import (Semester, Student, Group, StudyingStudent, Discipline, Task,
                     TaskInGroup, Lesson, LessonInGroup, Attendance, Progress, ControlPoint, Rating)

admin.site.register(Semester)
admin.site.register(Student)
admin.site.register(Group)
admin.site.register(StudyingStudent)
admin.site.register(Discipline)
admin.site.register(Task)
admin.site.register(TaskInGroup)
admin.site.register(Lesson)
admin.site.register(LessonInGroup)
admin.site.register(Attendance)
admin.site.register(Progress)
admin.site.register(ControlPoint)
admin.site.register(Rating)