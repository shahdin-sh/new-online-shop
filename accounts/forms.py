from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from accounts.models import CustomUserModel
from allauth.account.forms import SignupForm
from config import settings


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUserModel
        fields = ['username', 'email', 'profile_avatar', 'first_name', 'last_name', 'date_joined']


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUserModel
        fields = ['username', 'email', 'profile_avatar', 'first_name', 'last_name', 'date_joined']


# using allauth sign up form
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


# this form process when the users want to change their passwords in their account not during reset password process, that process related to allauth django package
class CustomChangePasswordForm(PasswordChangeForm):
    old_password = forms.CharField(
        strip=False,
        widget=forms.PasswordInput(
            attrs={'autocomplete': 'current-password', 'autofocus': True, 'class': 'form-control',
                   'placeholder': 'Old Password'}),
    )
    new_password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'autocomplete': 'new-password', 'class': 'form-control', 'placeholder': 'New Password'}),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        strip=False,
        widget=forms.PasswordInput(
            attrs={'autocomplete': 'new-password', 'class': 'form-control', 'placeholder': 'Confirm password'}),
    )

        