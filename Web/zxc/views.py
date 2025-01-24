from django.shortcuts import render
from django.http import HttpResponse
from .models import Course, Teacher
from django.views.generic import ListView, DetailView
from django.contrib.auth.decorators import login_required
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import CourseSerializer
from rest_framework.generics import get_object_or_404, GenericAPIView, ListCreateAPIView, RetrieveUpdateAPIView
from rest_framework.mixins import ListModelMixin

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

class CourseView(ListCreateAPIView):
    quaryset = Course.objects.all()
    serializer_class = CourseSerializer
    def perform_create(self, serializer):
        teacher = get_object_or_404(Teacher, id=self.request.data.get('teacher'))
        return serializer.save(teacher=teacher) 
class SingleCourseView(RetrieveUpdateAPIView):
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