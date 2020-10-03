from django.contrib import admin
from .models import Student, Teacher, Course, Chapter, Register

admin.site.register(Student)
admin.site.register(Teacher)
admin.site.register(Course)
admin.site.register(Chapter)
admin.site.register(Register)
