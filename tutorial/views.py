from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import RegisterForm
from django.contrib import messages
from .models import Student, Teacher, Course, Chapter, Register
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from datetime import datetime, date, timedelta
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string
from .tasks import deadline_email


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
    user = request.user
    courses = list(Course.objects.all())
    for obj in Register.objects.filter(user=user):
        course_obj = Course.objects.get(id=obj.course.id)
        if course_obj in courses:
            courses.remove(course_obj)
        # s.add(obj.course)
    return render(request, "tutorial/course.html", {'courses': courses})


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
        new_date = due_date + timedelta(days=chapters.due)
        register = Register.objects.create(course=course, user=request.user, chapter=chapters, due_date=new_date)
        register.save()
        # print("MAIL INITIATED")
        deadline_email.delay(register.id, chapters.due)
    return redirect("site-profile")


def validate_chapter(request):
    id = request.POST['complete']
    register = Register.objects.get(id=id)
    register.completed = True
    register.save()
    return redirect('site-profile')


# def testing(request):
#     template = render_to_string(
#         'tutorial/mail.html',
#         {'user': request.user},
#     )
#     email = EmailMessage(
#         'Deadline passed!',
#         template,
#         settings.EMAIL_HOST_USER,
#         ['adipanwar311@gmail.com'],
#     )
#     email.fail_silently = False
#     email.send()
#     print("PREPARING TO SEND EMAIL")
#     deadline_email.delay(request.user.id, 100)
#     return render(request, "tutorial/home.html", {})


@login_required
def profile(request):
    courses = dict()
    for obj in Register.objects.filter(user=request.user):
        course = Course.objects.get(id=obj.course.id)
        if course not in courses.keys():
            courses[course] = list()
        courses[course].append(obj)
    today_date = date(datetime.now().year, datetime.now().month, datetime.now().day)
    # print(courses)
    return render(request, "tutorial/profile.html", {'courses': courses, 'date': today_date})
