from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
# from .forms import CustomSignupForm
#
#
# # usage for django.contrib.auth.urls
# def signup_view(request):
#     signup_form = CustomSignupForm(request.POST)
#     if signup_form.is_valid():
#         user = signup_form.save()
#         # refresh_from_db() method  handle synchronism issue, basically reloading the database after the signal
#         user.refresh_from_db()
#         # choose basic avatar photo for every user
#         user.profile_avatar = 'default/img_avatar.png'
#         user.save()
#         # cleaned_data is holding the validated form data
#         username = signup_form.cleaned_data.get('username')
#         password = signup_form.cleaned_data.get('password1')
#         email = signup_form.cleaned_data.get('email')
#         # authenticate() method takes credentials as keyword arguments
#         user = authenticate(username=username, password=password, email=email)
#         # login() method takes an HttpRequest object and a User object and saves the user’s ID in the session
#         login(request, user)
#         return redirect('homepage')
#     else:
#         signup_form = CustomSignupForm()
#     return render(request, 'account/signup.html', {'signup_form': signup_form})
