from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status, serializers
from rest_framework.views import APIView
from .models import Course, Teacher

# Serializer using ModelSerializer for automatic handling of CRUD operations
class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ('id', 'title', 'categorycourse', 'price', 'teacher')

    # def create(self, validated_data):
    #     teacher_id = validated_data.pop('teacher_id')
    #     teacher = Teacher.objects.get(pk=teacher_id) #Get the teacher instance
    #     course = Course.objects.create(teacher=teacher, **validated_data) #pass the validated fields to the constructor
    #     return course

    # def update(self, instance, validated_data):
    #     teacher_id = validated_data.pop('teacher_id', instance.teacher.id)
    #     teacher = Teacher.objects.get(pk=teacher_id)
    #     instance.teacher = teacher
    #     instance.title = validated_data.get('title', instance.title)
    #     instance.categorycourse = validated_data.get('categorycourse', instance.categorycourse)
    #     instance.price = validated_data.get('price', instance.price)

    #     instance.save()
    #     return instance