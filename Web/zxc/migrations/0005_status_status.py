# Generated by Django 4.2 on 2024-11-27 22:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('zxc', '0004_rename_titles_categorydetail_title_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='status',
            name='status',
            field=models.CharField(choices=[('Да', 'Да'), ('Нет', 'Нет')], default=1, max_length=3),
            preserve_default=False,
        ),
    ]
