from django.urls import path, include
from .views import CourseViewSet, SingleCourseView
from rest_framework.routers import DefaultRouter
from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets

router = DefaultRouter()
router.register(r'courses', CourseViewSet, basename='user')
urlpatterns = router.urls

# urlpatterns = [
#     path('courses/', CourseViewSet.as_view({'get': 'list'})),
#     path('courses/<int:pk>/', CourseViewSet.as_view({'get': 'retrieve'})),
# ]