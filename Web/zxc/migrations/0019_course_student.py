# Generated by Django 4.2 on 2024-12-04 19:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('zxc', '0018_alter_course_photo'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='student',
            field=models.ForeignKey(blank=True, help_text='Выберите студента курса', null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Студент'),
        ),
    ]