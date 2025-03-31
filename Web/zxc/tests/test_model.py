import pytest
from zxc.models import Course  # Абсолютный импорт

@pytest.mark.django_db
def test_course_creation():
    course = Course.objects.create(
        title="New Course",
        description="This is a new course",
        categorycourse="programming",
        # Добавьте другие обязательные поля, такие как teacher и duration
    )
    assert course.title == "New Course"
    assert course.description == "This is a new course"