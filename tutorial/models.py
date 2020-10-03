from django.db import models
from django.contrib.auth.models import User


class Student(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, unique=True)

    def __str__(self):
        return self.user.username

class Teacher(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, unique=True)
    
    def __str__(self):
        return self.user.username

class Course(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=250, default="Description of the course.")
    # students = models.ManyToManyField(Student, blank=True)
    # teachers = models.ManyToManyField(Teacher, blank=True)
    # users = models.ManyToManyField(User, blank=True)

    def __str__(self):
        return self.name

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
