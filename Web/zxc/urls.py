from django.urls import path, include
from .views import CourseViewSet, SingleCourseView, TeacherViewSet, UserViewSet, SnippetViewSet, CustomAuthToken
from rest_framework.routers import DefaultRouter
from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets
from rest_framework.schemas import get_schema_view 
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework.urlpatterns import format_suffix_patterns


router = DefaultRouter()
router.register(r'courses', CourseViewSet, basename='course')
router.register(r'teachers', TeacherViewSet, basename='teacher')
router.register(r'users', UserViewSet, basename='user')
router.register(r'snippets', SnippetViewSet, basename='snippet')
router.register(r'v1/courses', CourseViewSet, basename='course-v1')
router.register(r'v2/courses', CourseViewSet, basename='course-v2')
# urlpatterns = router.urls

# Создаем общие маршруты
urlpatterns = [
    path('api-token-auth/', CustomAuthToken.as_view(), name='api_token_auth'),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('', include(router.urls)),
]

# Включаем ваши маршруты с помощью	router
urlpatterns += router.urls

# Добавляем суффиксы формата
# urlpatterns = format_suffix_patterns(urlpatterns, allowed=['json', 'html'])

# urlpatterns = [
#     path('courses/', CourseViewSet.as_view({'get': 'list'})),
#     path('courses/<int:pk>/', CourseViewSet.as_view({'get': 'retrieve'})),
# ]