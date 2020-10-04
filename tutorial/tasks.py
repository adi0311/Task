from __future__ import absolute_import

from celery import shared_task

from django.contrib.auth.models import User
from .models import Register
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string
from time import sleep


# @shared_task
# def add():
#     print("HELLO")
#     return "HELLO"

@shared_task
def deadline_email(id, time):
    sleep(time * 86400)
    register = Register.objects.get(id=id)
    user = register.user
    chapter = register.chapter
    completed = register.completed
    course = register.course
    if not completed:
        template = render_to_string(
            'tutorial/mail.html',
            {
                'user': user,
                'chapter': chapter,
                'course': course,
            },
        )
        email = EmailMessage(
            'Deadline passed!',
            template,
            settings.EMAIL_HOST_USER,
            [user.email],
        )
        email.fail_silently = False
        email.send()
        # print("EMAIL SEND", user.username)
