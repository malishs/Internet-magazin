# Generated by Django 4.2 on 2024-11-29 07:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('zxc', '0013_remove_course_teachers_course_teachers'),
    ]

    operations = [
        migrations.RenameField(
            model_name='course',
            old_name='teachers',
            new_name='teacher',
        ),
    ]