# Generated by Django 4.2 on 2024-12-04 14:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('zxc', '0015_remove_categorydetail_complexity_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='categorydetail',
            name='title',
        ),
        migrations.AlterField(
            model_name='course',
            name='categorycourse',
            field=models.CharField(choices=[('programming', 'Программирование'), ('design', 'Дизайн'), ('game', 'Игры'), ('music_and_cinema', 'Кино и музыка')], default='programming', max_length=50),
        ),
        migrations.DeleteModel(
            name='Category',
        ),
        migrations.DeleteModel(
            name='CategoryDetail',
        ),
    ]
