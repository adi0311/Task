from django.db import models
from django.contrib.auth.models import User


class Student(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class Teacher(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class Course(models.Model):
    name = models.CharField(max_length=100)
    students = models.ManyToManyField(Student)
    teachers = models.ManyToManyField(Teacher)

class Chapter(models.Model):
    name = models.CharField(max_length=120, null=False)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    due = models.IntegerField()

    def __str__(self):
        return self.name

class Register(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)
    due_date = models.DateField(auto_now=False)
