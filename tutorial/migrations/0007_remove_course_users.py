# Generated by Django 3.0.4 on 2020-10-03 15:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tutorial', '0006_auto_20201003_2056'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course',
            name='users',
        ),
    ]
