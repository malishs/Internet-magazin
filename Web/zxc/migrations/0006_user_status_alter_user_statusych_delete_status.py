# Generated by Django 4.2 on 2024-11-27 22:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('zxc', '0005_status_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='status',
            field=models.CharField(choices=[('Да', 'Да'), ('Нет', 'Нет')], default=1, max_length=3),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='user',
            name='statusych',
            field=models.CharField(choices=[('Да', 'Да'), ('Нет', 'Нет')], help_text='Введите статус прохождения курса', max_length=3, verbose_name='Статус прохождения курса'),
        ),
        migrations.DeleteModel(
            name='Status',
        ),
    ]
