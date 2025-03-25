from django.contrib import admin
from .models import Teacher, DurationCourse, Course, CustomUser
from django import forms
from django.utils.html import format_html
from django.contrib.auth.admin import UserAdmin

class TeacherAdmin(admin.ModelAdmin):
    list_display = ('middle_name', 'first_name')
    fields = ('middle_name', 'first_name', ('experience', 'photo'))
    readonly_fields = ['show_photo']
    def show_photo(self, obj):
        return format_html(
            f'<img src="{obj.photo.url}" style="max-height: 100px">')
    show_photo.short_description = 'Фото'

admin.site.register(Teacher, TeacherAdmin)
admin.site.register(DurationCourse)
admin.site.register(Course)
admin.site.register(CustomUser, UserAdmin)