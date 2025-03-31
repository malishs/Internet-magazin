import pytest
from zxc.serializers import CourseSerializer, UserSerializer  # Исправьте импорты
from zxc.models import Course  # Абсолютный импорт

@pytest.mark.django_db
def test_course_serializer_valid():
    course_data = {
        "title": "Valid Course",
        "description": "This is a valid course",
        "duration": {"duration": 40},
        # Обязательно добавьте все обязательные поля
    }
    serializer = CourseSerializer(data=course_data)
    assert serializer.is_valid()
    assert serializer.validated_data['title'] == "Valid Course"

@pytest.mark.django_db
def test_user_serializer_create():
    user_data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "strongpassword"
    }
    serializer = UserSerializer(data=user_data)
    assert serializer.is_valid()
    user = serializer.save()
    assert user.username == "testuser"