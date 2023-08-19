from django.urls import path, include, re_path
from .views import wishlist_view, my_account, edit_user_profile


app_name = 'account'

urlpatterns = [
    path('wishlist/', wishlist_view, name='wishlist_view'),
    path('my_account/', my_account, name="my_account"),
    path('my_account/edit_profile', edit_user_profile, name='edit_profile')
]