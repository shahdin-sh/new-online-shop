from accounts.views import wishlist_view, my_account, edit_user_information, change_user_password
from django.urls import path


app_name = 'account'

urlpatterns = [
    path('wishlist/', wishlist_view, name='wishlist_view'),
    path('my_account/', my_account, name="my_account"),
    path('my_account/edit_profile', edit_user_information, name='edit_profile'),
    path('my_account/change_password', change_user_password, name='change_password'),
]