# Generated by Django 4.2 on 2024-11-30 17:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('zxc', '0014_rename_teachers_course_teacher'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='categorydetail',
            name='complexity',
        ),
        migrations.RemoveField(
            model_name='categorydetail',
            name='languageprog',
        ),
    ]
