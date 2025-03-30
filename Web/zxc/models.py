from django.db import models
from django.urls import reverse
from datetime import date
from django.contrib.auth.models import AbstractUser
from pygments.lexers import get_lexer_by_name
from pygments.formatters.html import HtmlFormatter
from pygments import highlight
    

class Teacher(models.Model):
    first_name = models.CharField(max_length=100,
                                help_text="Введите имя преподавателя",
                                verbose_name="Имя преподавателя")
    middle_name = models.CharField(max_length=100,
                                help_text="Введите фамилию преподавателя",
                                verbose_name="Фамилия преподавателя")
    last_name = models.CharField(max_length=100,
                                help_text="Введите отчество преподавателя",
                                verbose_name="Отчество преподавателя")
    specialization = models.CharField(max_length=200,
                                    help_text="Введите специальность преподавателя",
                                    verbose_name="Специальность преподавателя")
    description = models.TextField(help_text="Введите проекты и языки программирования, которые знает преподаватель",
                                    verbose_name="Описание карьеры")
    experience = models.IntegerField(help_text="Введите стаж работы преподавателя в IT-сфере",
                                    verbose_name="Стаж работы")
    photo = models.ImageField(upload_to='images',
                                help_text="Введите фото преподавателя",
                                verbose_name="Фото преподавателя",
                                null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.middle_name} {self.last_name}"

class DurationCourse(models.Model):
    duration = models.IntegerField(help_text="Введите длительность курса",
                                    verbose_name="Длительность курса")

    def __str__(self):
        return str(self.duration)
    
class CustomUser(AbstractUser):
    bio = models.TextField(blank=False)
    email = models.EmailField(unique=True)  # Ensure emails are unique and enforce email format

    def __str__(self):
        return self.username
    
    @property
    def courses(self):
        return self.students.all()
    
class Course(models.Model):
    title = models.CharField(max_length=200,
                             help_text="Введите название курса",
                             verbose_name="Название курса")
    categorycourse = models.CharField(max_length=50,
                                       choices=[('programming', 'Программирование'),
                                                ('english', 'Английский язык'),
                                                ('game', 'Игры'),
                                                ('music_and_cinema', 'Кино и музыка')],
                                       default='programming')
    description = models.TextField(help_text="Введите описание курса",
                                   verbose_name="Описание курса")
    teacher = models.ManyToManyField('Teacher',
                                      help_text="Выберите преподавателя (преподавателей) для курса",
                                      verbose_name="Преподаватель (преподаватели) курса")
    duration = models.ForeignKey('DurationCourse', on_delete=models.CASCADE,
                                  help_text="Введите длительность курса",
                                  verbose_name="Длительность курса")
    students = models.ManyToManyField(CustomUser, blank=True, related_name='courses', help_text='Выберите студентов, записанных на этот курс')
    price = models.DecimalField(decimal_places=2, max_digits=7,
                                help_text="Введите стоимость курса",
                                verbose_name="Стоимость курса")
    photo = models.ImageField(upload_to='course_photos/',
                              help_text="Введите обложку курса",
                              verbose_name="Обложка курса",
                              null=True)

    def __str__(self):
        return self.title

    def display_teacher(self):
        return ', '.join([teacher.middle_name for teacher in self.teacher.all()])
    
    display_teacher.short_description = "Преподаватели"

class Snippet(models.Model):
    owner = models.ForeignKey(CustomUser, related_name='snippets', on_delete=models.CASCADE)
    code = models.TextField()
    highlighted = models.TextField()
    title = models.CharField(max_length=100, default='A snippet')
    language = models.CharField(max_length=100, default='python')
    linenos = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        lexer = get_lexer_by_name(self.language)
        formatter = HtmlFormatter()
        self.highlighted = highlight(self.code, lexer, formatter)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title