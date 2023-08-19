from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from orders.forms import OrderForm
from .forms import CustomUserChangeForm
from allauth.account.forms import ChangePasswordForm
from django.http import HttpResponseServerError
import logging
from django.utils import timezone
from .utils import persian_to_western_digits



@login_required
def wishlist_view(request):
    return render(request, 'accounts/wishlist.html')


@login_required
def my_account(request):
    context = {
        'order_form': OrderForm(),
        'user_change_form': CustomUserChangeForm(),
        'password_change_form': ChangePasswordForm(),
        'current_time': persian_to_western_digits(timezone.now().strftime('%Y-%m-%d')),
    }
    print(persian_to_western_digits(timezone.now().strftime('%Y-%m-%d')))
    return render(request, 'accounts/my_account.html', context)


@login_required
@require_POST
def edit_user_profile(request):
    user = request.user
    if request.method == 'POST':
        print(request.POST)
        user_change_form = CustomUserChangeForm(request.POST, instance=user)
        if user_change_form.is_valid():
            user_change_form.save()
            return redirect('account:my_account')
        else:
            # Log form errors
            logger = logging.getLogger(__name__)
            logger.error("Form validation failed: %s", user_change_form.errors)
            # creating an error response
            error_message = f"Form validation failed: {user_change_form.errors}"
            response = HttpResponseServerError(error_message)
            return response
    else:
        user_change_form = CustomUserChangeForm()

        
