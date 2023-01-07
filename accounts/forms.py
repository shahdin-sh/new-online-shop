from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import CustomUserModel


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUserModel
        fields = ['username', 'email', 'profile_avatar']


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUserModel
        fields = ['username', 'email', 'profile_avatar']


class SignupForm(UserCreationForm):
    class Meta:
        model = CustomUserModel
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

