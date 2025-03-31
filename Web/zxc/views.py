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
from rest_framework.views import APIView, exception_handler
from .negotiation import IgnoreClientContentNegotiation  # Импортируем наш класс
from .metadata import CustomMetadata  # Импортируем наш класс метаданных
from drf_spectacular.utils import extend_schema_view, extend_schema
from drf_spectacular.utils import extend_schema
from django.utils.timezone import now
from rest_framework.exceptions import APIException
from rest_framework.reverse import reverse
from rest_framework.settings import api_settings


class SingleCourseView(viewsets.GenericViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

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

class CoursePagination(PageNumberPagination):
    page_size = 3  
    page_size_query_param = 'page_size'
    max_page_size = 100 

@extend_schema_view(
    list=extend_schema(description="Получение списка курсов"),
    retrieve=extend_schema(description="Получение детали курса"),
)
class CourseViewSet(viewsets.ModelViewSet):
    """
    Обработчик для курсов. Поддерживает операции CRUD и обеспечивает фильтрацию,
    дросселирование и кэширование.
    """
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    throttle_classes = [UserRateThrottle]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['title', 'teacher', 'categorycourse']
    pagination_class = CoursePagination

    @method_decorator(cache_page(60 * 60 * 2))
    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        for course in response.data['results']:
            course['url'] = request.build_absolute_uri(reverse('course-detail', args=[course['id']], request=request))
        return response

    @method_decorator(cache_page(60 * 60 * 2))
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    def get_serializer_class(self):
        if self.request.version == 'v1':
            return CourseSerializerVersion1
        elif self.request.version == 'v2':
            return CourseSerializerVersion2
        return CourseSerializer

class TeacherViewSet(viewsets.ModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
    throttle_classes = [UserRateThrottle]

class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    throttle_classes = [UserRateThrottle]
    renderer_classes = [JSONRenderer, BrowsableAPIRenderer]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['username', 'email']
    ordering = ['username']

class SnippetViewSet(viewsets.ModelViewSet):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    throttle_classes = [UserRateThrottle]
    parser_classes = [JSONParser, MultiPartParser]
    renderer_classes = [JSONRenderer, BrowsableAPIRenderer]
    filterset_fields = ['owner', 'title']

    @extend_schema(
        request=SnippetSerializer,
        responses={200: SnippetSerializer},
        description="Создание нового сниппета"
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @action(detail=True, methods=['get'], renderer_classes=[JSONRenderer])
    def highlight(self, request, *args, **kwargs):
        snippet = self.get_object()
        return Response(snippet.highlighted)

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

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    # Добавляем код состояния HTTP в ответ
    if response is not None:
        response.data['status_code'] = response.status_code
    else:
        response = Response(
            {'error': 'Internal Server Error', 'status_code': status.HTTP_500_INTERNAL_SERVER_ERROR},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    return response