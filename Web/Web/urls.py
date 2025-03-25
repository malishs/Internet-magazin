"""
URL configuration for Web project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from zxc import views
from django.urls import re_path
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from zxc import urls

urlpatterns = [
    path('', views.index, name='home'),
    path('admin/', admin.site.urls),
    path('', include('zxc.urls')),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('programming_courses/', views.programming_courses, name='programming_courses'),
    path('english_courses/', views.english_courses, name='english_courses'),
    path('musicandcinema/', views.musicandcinema_courses, name='musicandcinema_courses'),
    path('game_courses/', views.game_courses, name='game_courses'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('profile/', views.profile, name='profile'),
    path('register/', views.register, name='register'),
    path('api/', include('zxc.urls')),
    path('login/', views.login_view, name='login'),
    path('profile/', views.profile_view, name='profile'),
    path('add_course/<int:course_id>/', views.add_course_to_profile, name='add_course_to_profile'),
    path('courses/', views.CourseListView.as_view(), name='course_list'),

] 
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += [
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]