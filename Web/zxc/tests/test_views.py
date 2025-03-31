import pytest
from django.urls import reverse
from rest_framework import status
from zxc.models import Course  # Измените импорт на абсолютный
from zxc.serializers import CourseSerializer  # Абсолютный импорт

@pytest.mark.django_db
def test_course_list(api_client):
    url = reverse('course-list')
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.data, list)

@pytest.mark.django_db
def test_create_course(api_client, create_user):
    user = create_user()  # Убедитесь, что эта фикстура верно настроена
    api_client.force_authenticate(user=user)
    url = reverse('course-list')
    data = {
        "title": "Test Course",
        "description": "This is a test course",
        "duration": {"duration": 40},
        "teacher": [],
        "students": []
    }
    response = api_client.post(url, data, format='json')
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data['title'] == "Test Course"

@pytest.mark.django_db
def test_unauthorized_course_create(api_client):
    url = reverse('course-list')
    data = {
        "title": "Test Course",
        "description": "This is a test course",
    }
    response = api_client.post(url, data, format='json')
    assert response.status_code == status.HTTP_401_UNAUTHORIZED