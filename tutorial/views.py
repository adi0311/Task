from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import RegisterForm
from django.contrib import messages
from .models import Student, Teacher, Course, Chapter, Register
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from datetime import datetime, date, timedelta


def homepage(request):
    return render(request, 'tutorial/home.html', {})

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            email = form.cleaned_data.get('email')
            usertype = form.cleaned_data.get('usertype')
            form.save()
            new_user = User.objects.filter(username=username, email=email).first()
            if usertype == 'student':
                Student.objects.create(user=new_user)
            else:
                Teacher.objects.create(user=new_user)
            messages.success(request, f'Hey, {first_name} your account is created successfully! You can now login.')
            return redirect('site-profile')
    else:
        form = RegisterForm()
    return render(request, 'tutorial/register.html', {'form': form})


def courses(request):
    return render(request, "tutorial/course.html", {'courses': Course.objects.all()})


def register_for_course(request):
    courseid = request.POST['courseid']
    course = Course.objects.filter(id=courseid).first()
    course_chapters = Chapter.objects.filter(course=course)
    due_date = date(datetime.now().year, datetime.now().month, datetime.now().day)
    # course.add(request.user)
    # student, teacher = Student.objects.filter(user=request.user), Teacher.objects.filter(user=request.user)
    # if len(student) > 0:
    #     course.students.add(student.first())
    #     course.save()
    # else:
    #     course.teachers.add(teacher.first())
    #     course.save()
    # print(due_date)
    # print(course_chapters)
    # print(course)
    for chapters in course_chapters:
        register = Register.objects.create(course=course, user=request.user, chapter=chapters, due_date=due_date + timedelta(days=chapters.due))
        register.save()
    return redirect("site-profile")



@login_required
def profile(request):
    return render(request, "tutorial/profile.html", {})
