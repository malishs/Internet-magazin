from django.urls import path
from .views import CourseView, SingleCourseView


urlpatterns = [
    path('courses/', CourseView.as_view()),
    path('courses/<int:pk>/', SingleCourseView.as_view()),
]