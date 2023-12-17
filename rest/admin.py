from django.contrib import admin
from rest.models import User
from django.contrib.auth.admin import UserAdmin
# Register your models here.

class CustomUserAdmin(UserAdmin):
    model = User
    # Добавьте поля в fieldsets для изменения пользователя
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('department', 'job_title', 'middle_name')}),
    )
    # Добавьте поля в add_fieldsets для создания нового пользователя
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('department', 'job_title', 'middle_name')}),
    )

admin.site.register(User, CustomUserAdmin)