from django.contrib import admin

from .models import (Semester, Student, Group, StudentInGroup, Discipline, Task,
                     TaskInGroup, Lesson, LessonInGroup, Attendance, Progress, ControlPoints, Rating)

admin.site.register(Semester)
admin.site.register(Student)
admin.site.register(Group)
admin.site.register(StudentInGroup)
admin.site.register(Discipline)
admin.site.register(Task)
admin.site.register(TaskInGroup)
admin.site.register(Lesson)
admin.site.register(LessonInGroup)
admin.site.register(Attendance)
admin.site.register(Progress)
admin.site.register(ControlPoints)
admin.site.register(Rating)