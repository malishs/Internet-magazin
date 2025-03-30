from django.shortcuts import render, get_object_or_404, redirect
from .models import Course, Teacher, CustomUser, Snippet
from django.contrib.auth.decorators import login_required
from .serializers import CourseSerializer, TeacherSerializer, UserSerializer, SnippetSerializer, CourseSerializerVersion1, CourseSerializerVersion2
from rest_framework.generics import get_object_or_404, ListCreateAPIView, RetrieveDestroyAPIView
from rest_framework import viewsets, generics, permissions, status
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomUserCreationForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .forms import CustomUserCreationForm, CustomLoginForm, ProfileUpdateForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.response import Response
from django.views.generic import ListView
from .models import Course
from rest_framework.decorators import action 
from rest_framework import renderers
from rest_framework.parsers import JSONParser, MultiPartParser
from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.throttling import UserRateThrottle
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters 
from rest_framework.pagination import PageNumberPagination
from rest_framework.negotiation import BaseContentNegotiation
from rest_framework.views import APIView
from .negotiation import IgnoreClientContentNegotiation  # Импортируем наш класс
from .metadata import CustomMetadata  # Импортируем наш класс метаданных



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

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirect to login after successful registration
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = CustomLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  # Замените на вашу домашнюю страницу
    else:
        form = CustomLoginForm()
    
    return render(request, 'zxc/login.html', {'form': form})

@login_required
def profile_view(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileUpdateForm(instance=request.user)

    # Retrieve courses for the logged-in user
    user_courses = Course.objects.filter(students=request.user)  # Correctly using the related name

    return render(request, 'zxc/profile.html', {'form': form, 'courses': user_courses})

@login_required
def add_course_to_profile(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    # Add course to the user
    course.students.add(request.user)

    return redirect('course_list')  # Redirects to the course list

class CourseListView(ListView):
    model = Course
    template_name = 'courses/course_list.html'  # Укажите ваш шаблон
    context_object_name = 'courses'

# API

class CourseViewSet(viewsets.ModelViewSet):
    filterset_fields = ['title', 'teacher', 'categorycourse']  # Пример фильтров
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    throttle_classes = [UserRateThrottle]  # Добавляем дросселирование
    filter_backends = [DjangoFilterBackend]
    metadata_class = CustomMetadata  
    

    @method_decorator(cache_page(60 * 60 * 2))  # Кэшируем на 2 часа
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @method_decorator(cache_page(60 * 60 * 2))  # Кэшируем на 2 часа
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    def get_serializer_class(self):
        if self.request.version == 'v1':
            return CourseSerializerVersion1
        elif self.request.version == 'v2':
            return CourseSerializerVersion2  # Используем новый сериализатор для v2
        return CourseSerializer  # Для всех остальных версий

class SingleCourseView(RetrieveDestroyAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

class TeacherViewSet(viewsets.ModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
    throttle_classes = [UserRateThrottle]  # Добавляем дросселирование

class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    throttle_classes = [UserRateThrottle]  # Добавляем дросселирование
    renderer_classes = [JSONRenderer, BrowsableAPIRenderer]
    filter_backends = [filters.OrderingFilter] 
    ordering_fields = ['username', 'email'] 
    ordering = ['username'] 
    negotiation_class = IgnoreClientContentNegotiation


class SnippetViewSet(viewsets.ModelViewSet):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    throttle_classes = [UserRateThrottle]  # Добавляем дросселирование
    parser_classes = [JSONParser, MultiPartParser]
    renderer_classes = [JSONRenderer, BrowsableAPIRenderer]
    filterset_fields = ['owner', 'title']  # Указание, что можно фильтровать по владельцу и заголовку

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @action(detail=True, methods=['get'], renderer_classes=[JSONRenderer])
    def highlight(self, request, *args, **kwargs):
        snippet = self.get_object()
        return Response(snippet.highlighted)

class SnippetDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    throttle_classes = [UserRateThrottle]  # Добавляем дросселирование

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return [permissions.AllowAny()]
        return super().get_permissions()

class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })

class CoursePagination(PageNumberPagination):
    page_size = 10  # Устанавливаем размер страницы
    page_size_query_param = 'page_size'  # Позволяем клиентам устанавливать размер страницы
    max_page_size = 100  # Ограничиваем максимальный размер страницы
