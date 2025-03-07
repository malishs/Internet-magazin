from django.shortcuts import render, get_object_or_404, redirect
from .models import Course, Teacher, CustomUser
from django.contrib.auth.decorators import login_required
from .serializers import CourseSerializer, TeacherSerializer, UserSerializer
from rest_framework.generics import get_object_or_404, ListCreateAPIView, RetrieveDestroyAPIView
from rest_framework.response import Response
from rest_framework import viewsets
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from .forms import CustomUserCreationForm
from django.contrib.auth.decorators import login_required

def index(request): 
    text_head = 'Online-курс. На нашем сайте вы можете получить опыт в IT-сфере!'
    course = Course.objects.all()
    num_course = Course.objects.all().count()
    teachers = Teacher.objects
    num_teachers = Teacher.objects.count()
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1
    context = {'text_head': text_head,
                'course': course,
                'num_course': num_course,
                'teachers': teachers,
                'num_teachers': num_teachers}
    return render(request, 'zxc/index.html', context)

def about(request):
    text_head = 'Сведения о компании'
    name = 'ООО "Интернет-магазин обучающих курсов Online-Курс"'
    rab1 = 'Лёгкая регистрация на курсы'
    rab2 = 'Вы сами делаете своё расписание!'
    rab3 = 'Наши специалисты помогут в любой ситуации во время обучения'
    rab4 = 'После выпуска трудоустроем на работу'
    context = {'text_head': text_head, 'name': name,
                'rab1': rab1, 'rab2': rab2,
                'rab3': rab3, 'rab4': rab4}
    return render(request, 'zxc/about.html', context)

def contact(request):
    return render(request, 'zxc/contact.html')

def programming_courses(request):
    courses = Course.objects.filter(categorycourse="programming")  # Фильтр по категории
    return render(request, 'zxc/programming_courses.html', {'courses': courses})

def english_courses(request):
    courses = Course.objects.filter(categorycourse="english")
    return render(request, 'zxc/english_courses.html', {'courses': courses})

def musicandcinema_courses(request):
    courses = Course.objects.filter(categorycourse="music_and_cinema")
    return render(request, 'zxc/musicandcinema_courses.html', {'courses': courses})

def game_courses(request):
    courses = Course.objects.filter(categorycourse="game")
    return render(request, 'zxc/game_courses.html', {'courses': courses})


@login_required
def profile(request):
    # Фильтруем только те курсы, где студент — это текущий пользователь
    student_courses = Course.objects.filter(student=request.user)
    return render(request, 'zxc/profile.html', {'student_courses': student_courses})

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Автоматически входим в аккаунт после регистрации
            return redirect('home')  # Перенаправляем на главную страницу (измените 'home' на вашу)
    else:
        form = CustomUserCreationForm()
    return render(request, 'zxc/register.html', {'form': form}) #Укажите путь к шаблону

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')  # Перенаправляем на главную страницу
    else:
        form = AuthenticationForm()
    return render(request, 'zxc/login.html', {'form': form})  #Укажите путь к шаблону

@login_required  # Требует авторизации для доступа
def logout_view(request):
    logout(request)
    return redirect('home') # Перенаправляем на главную страницу

@login_required # Пример страницы, требующей авторизации
def profile_view(request):
    return render(request, 'zxc/profile.html') #Укажите путь к шаблону


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    # def perform_create(self, serializer):
    #     teacher = get_object_or_404(Teacher, id=self.request.data.get('teacher'))
    #     return serializer.save(teacher=teacher) 
    # def list (self, request):
    #     queryset = Course.objects.all()
    #     serializer = CourseSerializer(queryset, many = True)
    #     return Response
    # def retrieve(self, request, pk=None):
    #     queryset = Course.objects.all()
    #     user = get_object_or_404(queryset, pk=pk)
    #     serializer = CourseSerializer(user)
    #     return Response(serializer.data)

class SingleCourseView(RetrieveDestroyAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    # def put(self, request, pk):
    #     saved_course = get_object_or_404(Course.objects.all(), pk=pk)
    #     data = request.data.get('course')
    #     serializer = CourseSerializer(instance=saved_course, data=data, partial=True)

    #     if serializer.is_valid(raise_exception=True):
    #         course_saved = serializer.save()

    #     return Response({
    #         "success": "Course '{}' updated successfully".format(course_saved.title)
    #     })
    # def delete(self, request, pk):
    # # Get object with this pk
    #     course = get_object_or_404(Course.objects.all(), pk=pk)
    #     course.delete()
    #     return Response({
    #         "message": "Article with id `{}` has been deleted.".format(pk)
    #     }, status=204)

# ViewSet для модели Teacher
class TeacherViewSet(viewsets.ModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer

# ViewSet для модели User
class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer