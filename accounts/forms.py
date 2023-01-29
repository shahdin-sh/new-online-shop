from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUserModel
from allauth.account.forms import SignupForm
from django import forms


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUserModel
        fields = ['username', 'email', 'profile_avatar', 'first_name', 'last_name']


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUserModel
        fields = ['username', 'email', 'profile_avatar', 'first_name', 'last_name']


class CustomSignupForm(SignupForm, forms.Form):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    profile_avatar = forms.ImageField().hidden_widget

    def save(self, request):
        # Ensure you call the parent class's save.
        # .save() returns a User object.
        user = super(CustomSignupForm, self).save(request)

        # Add your own processing here.
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.profile_avatar = 'default_avatar/img_avatar.png'
        user.save()
        # You must return the original result.
        return user






