from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserChangeForm, CustomUserCreationForm
from .models import CustomUserModel


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUserModel
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('profile_avatar', )}),
    )
    list_display = ['username', 'email', 'first_name', 'last_name', 'profile_avatar', 'is_staff']


# Registering admin
admin.site.register(CustomUserModel, CustomUserAdmin)
