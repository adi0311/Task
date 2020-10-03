from django import forms
from .models import Student, Teacher, Course
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class RegisterForm(UserCreationForm):

    first_name = forms.CharField(max_length=30, required=True, help_text='')
    last_name = forms.CharField(max_length=30, required=True, help_text='')
    email = forms.EmailField(max_length=254, help_text='')

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
