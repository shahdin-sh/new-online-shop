from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUserModel
from allauth.account.forms import SignupForm, BaseSignupForm
from django import forms
from config import settings


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUserModel
        fields = ['username', 'email', 'profile_avatar', 'first_name', 'last_name']


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUserModel
        fields = ['username', 'email', 'profile_avatar', 'first_name', 'last_name']


class CustomSignupForm(SignupForm, forms.Form):

    first_name = forms.CharField(
        max_length=settings.FIRST_NAME_MIN_LENGHT,
        widget=forms.TextInput(
            attrs= {
                'placeholder': 'First Name',
                }
        ),
    )
    last_name = forms.CharField(
        max_length=settings.LAST_NAME_MIN_LENGHT,
        widget=forms.TextInput(
            attrs= {
                'placeholder': 'Last Name',
                }
        ),
    )
    profile_avatar = forms.ImageField.hidden_widget
    # forms.ImageField(widget=forms.HiddenInput())

    # overriding the init method
    def __init__(self, *args, **kwargs):
        # call the init of the parent class which here is Sign up Form
        super().__init__(*args, **kwargs)
        # self.fields['username'].widget = forms.HiddenInput()

    def custom_signup(self, request, user):
        user.profile_avatar = 'default_avatar/img_avatar.png'
        user.save()
