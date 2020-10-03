from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import RegisterForm
from django.contrib import messages
from .models import Student, Teacher, Course
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required


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
            messages.success(request, f'Hey, {first_name} your account is created successfully! You can now login')
            return redirect('site-profile')
    else:
        form = RegisterForm()
    return render(request, 'tutorial/register.html', {'form': form})


def courses(request):
    return render(request, "tutorial/course.html", {'courses': Course.objects.all()})


@login_required
def profile(request):
    return render(request, "tutorial/profile.html", {})
