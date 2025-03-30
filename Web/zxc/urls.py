from django.urls import path, include
from .views import CourseViewSet, SingleCourseView, TeacherViewSet, UserViewSet, SnippetViewSet, CustomAuthToken
from rest_framework.routers import DefaultRouter
from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets

router = DefaultRouter()
router.register(r'courses', CourseViewSet, basename='course')
router.register(r'teachers', TeacherViewSet, basename='teacher')
router.register(r'users', UserViewSet, basename='user')
router.register(r'snippets', SnippetViewSet, basename='snippet')
router.register(r'v1/courses', CourseViewSet, basename='course-v1')
router.register(r'v2/courses', CourseViewSet, basename='course-v2')
# urlpatterns = router.urls

urlpatterns = [
    path('', include(router.urls)),
    path('api-token-auth/', CustomAuthToken.as_view(), name='api_token_auth'),
    
]

# urlpatterns = [
#     path('courses/', CourseViewSet.as_view({'get': 'list'})),
#     path('courses/<int:pk>/', CourseViewSet.as_view({'get': 'retrieve'})),
# ]