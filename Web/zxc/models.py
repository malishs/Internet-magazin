from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from datetime import date
    

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
        return self.middle_name

class DurationCourse(models.Model):
    duration = models.IntegerField(help_text="Введите длительность курса",
                                    verbose_name="Длительность курса")

    def __str__(self):
        return str(self.duration)

class Course(models.Model):
    title = models.CharField(max_length=200,
                            help_text="Введите название курса",
                            verbose_name="Название курса")
    categorycourse = models.CharField(max_length=50,
                                        choices=[('programming', 'Программирование'),
                                                ('english', 'Английский язык'),
                                                ('game', 'Игры'),
                                                ('music_and_cinema', 'Кино и музыка')], default='programming')
    description = models.TextField(help_text="Введите описание курса",
                                    verbose_name="Описание курса")
    teacher = models.ManyToManyField('Teacher',
                                help_text="Выберите преподавателя (преподавателей) для курса",
                                verbose_name="Преподаватель (преподаватели) курса")
    duration = models.ForeignKey('DurationCourse', on_delete=models.CASCADE,
                                help_text="Введите длительность курса",
                                verbose_name="Длительность курса")
    student = models.ForeignKey(User, on_delete=models.SET_NULL,
                                null=True, blank=True,
                                verbose_name="Студент",
                                help_text='Выберите студента курса')
    price = models.DecimalField(decimal_places=2, max_digits=7,
                                help_text="Введите стоимость курса",
                                verbose_name="Стоимость курса")
    photo = models.ImageField(upload_to='course_photos/',
                                help_text="Введите обложку курса",
                                verbose_name="Обложка курса",
                                null=False)

    def __str__(self):
        return self.title

    def display_teacher(self):
        return ', '.join([teacher.middle_name for teacher in self.teacher.all()])
    
    display_teacher.short_description = "Преподаватели"

class User(models.Model):
    STATUS_CHOICES = [
                ('Да', 'Да'),
                ('Нет', 'Нет'),
    ]

    first_name = models.CharField(max_length=100,
                                help_text="Введите имя студента",
                                verbose_name="Имя студента")
    middle_name = models.CharField(max_length=100,
                                help_text="Введите фамилию студента",
                                verbose_name="Фамилия студента")
    last_name = models.CharField(max_length=100,
                                help_text="Введите отчество студента",
                                verbose_name="Отчество студента")
    statusych = models.CharField(max_length=3,
                                help_text="Введите статус прохождения курса",
                                verbose_name="Статус прохождения курса",
                                choices=STATUS_CHOICES)
    course = models.ForeignKey('Course', 
                        on_delete=models.CASCADE,
                        null=True, blank=True,
                        help_text="Выберите курс",
                        verbose_name="Курс")
    completion_date = models.DateField(null=True, blank=True,
                                        help_text="Введите дату окончания прохождения курса",
                                        verbose_name="Дата окончания прохождения курса")
    datereg = models.DateField(null=True, blank=True,
                                help_text="Введите дату регистрации на сайт",
                                verbose_name="Дата регистрации на сайт")
    

    def __str__(self):
        return self.middle_name
    