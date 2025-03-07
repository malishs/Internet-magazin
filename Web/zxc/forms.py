from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name') # Поля для формы
        #Если не используете кастомную модель, то fields = UserCreationForm.Meta.fields + ('first_name', 'last_name', 'email')


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name') # Поля для формы
        #Если не используете кастомную модель, то fields = UserChangeForm.Meta.fields + ('first_name', 'last_name', 'email')
