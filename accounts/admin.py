from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from accounts.forms import CustomUserChangeForm, CustomUserCreationForm
from accounts.models import CustomUserModel


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUserModel

    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('profile_avatar', )}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "email", "profile_avatar", "password1", "password2", "first_name", "last_name"),
            },
        ),
    )

    list_display = ['username', 'email', 'first_name', 'last_name', 'profile_avatar', 'is_staff']


# Registering admin
admin.site.register(CustomUserModel, CustomUserAdmin)
