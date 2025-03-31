from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status, serializers
from rest_framework.views import APIView
from .models import Course, Teacher, CustomUser, Snippet, DurationCourse
from rest_framework.validators import UniqueValidator
from rest_framework.authtoken.models import Token



class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        ordering = ['title']
        fields = ['id', 'first_name', 'middle_name', 'last_name', 'specialization', 'description', 'experience', 'photo']

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})
    snippets = serializers.PrimaryKeyRelatedField(many=True, queryset=Snippet.objects.all(), required=False)

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'password', 'snippets']
        validators = [UniqueValidator(queryset=CustomUser.objects.all())]

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = CustomUser(**validated_data)
        user.set_password(password)  # Хешируем пароль
        user.save()
        Token.objects.create(user=user)  # Создание токена после создания пользователя
        return user

class LengthSerializer(serializers.ModelSerializer):
    class Meta:
        model = DurationCourse
        fields = ['duration']

class CourseSerializer(serializers.ModelSerializer):
    teacher = TeacherSerializer(many=True)
    students = UserSerializer(many=True, required=False)
    duration = LengthSerializer()
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Course
        fields = '__all__'

    def create(self, validated_data):
        teacher_data = validated_data.pop('teacher', [])
        student_data = validated_data.pop('students', [])
        duration_data = validated_data.pop('duration')

        duration_instance = DurationCourse.objects.create(**duration_data)
        course = Course.objects.create(duration=duration_instance, **validated_data)

        # Создание и добавление учителей
        for teacher in teacher_data:
            teacher_instance = Teacher.objects.create(**teacher)
            course.teacher.add(teacher_instance)

        # Создание и добавление студентов
        for student in student_data:
            student_instance = UserSerializer().create(student)
            course.students.add(student_instance)

        return course

    def update(self, instance, validated_data):
        teacher_data = validated_data.pop('teacher', [])
        student_data = validated_data.pop('students', [])
        duration_data = validated_data.pop('duration', {})

        # Обновляем длительность курса
        if duration_data:
            instance.duration.duration = duration_data['duration']
            instance.duration.save()

        # Обновляем поля курса
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.save()

        # Обновляем учителей
        if teacher_data:
            instance.teacher.clear()  # очищаем старые записи
            for teacher in teacher_data:
                teacher_instance = Teacher.objects.create(**teacher)
                instance.teacher.add(teacher_instance)

        # Обновляем студентов
        if student_data:
            instance.students.clear()
            for student in student_data:
                student_instance = UserSerializer().create(student)
                instance.students.add(student_instance)

        return instance

class SnippetSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Snippet
        fields = ['id', 'owner', 'code', 'highlighted', 'title', 'language', 'linenos']

class CourseSerializerVersion1(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'title', 'description']  # Поля для версии 1

class CourseSerializerVersion2(serializers.ModelSerializer):
    teacher_names = serializers.StringRelatedField(many=True, source='teacher')

    class Meta:
        model = Course
        fields = ['id', 'title', 'teacher_names', 'price']  # Поля для версии 2