from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from orders.forms import OrderForm
from .forms import CustomUserChangeForm, CustomChangePasswordForm
from django.http import HttpResponseBadRequest
import logging
from django.utils import timezone
from .utils import persian_to_western_digits
from django.contrib import messages



@login_required
def wishlist_view(request):
    breadcrumb_data = [{'lable': 'wishlist', 'title': 'wishlist'}]
    return render(request, 'accounts/wishlist.html', context={'breadcrumb_data': breadcrumb_data})


@login_required
def my_account(request):
    breadcrumb_data = [{'lable': 'my_account','title': 'my account'}]
    context = {
        'order_form': OrderForm(),
        'user_change_form': CustomUserChangeForm(),
        'password_change_form': CustomChangePasswordForm(user=request.user),
        'current_time': persian_to_western_digits(timezone.now().strftime('%Y-%m-%d')),
        'breadcrumb_data': breadcrumb_data,
    }
    return render(request, 'accounts/my_account.html', context)


@login_required
@require_POST
def edit_user_information(request):
    user = request.user
    if request.method == 'POST':
        user_change_information_form = CustomUserChangeForm(request.POST, instance=user)
        if user_change_information_form.is_valid():
            user_change_information_form.save()
            messages.success(request, 'your information updated successfully')
            return redirect('account:my_account')
        else:
            # Log form errors
            logger = logging.getLogger(__name__)
            logger.error("Form validation failed: %s", user_change_information_form.errors)
            # creating an error response
            error_message = f"Form validation failed: {user_change_information_form.errors}"
            response = HttpResponseBadRequest(error_message)
            return response
    else:
        user_change_information_form = CustomUserChangeForm()


@login_required
def change_user_password(request):
    user = request.user
    if request.method == 'POST':
        change_password_form = CustomChangePasswordForm(user, request.POST)
        if change_password_form.is_valid():
            change_password_form.save()
            messages.success(request, 'your password has been changed successfully')
            return redirect('account:my_account')
        else:
            # Log form errors
            logger = logging.getLogger(__name__)
            logger.error("Form validation failed: %s", change_password_form.errors)
            # creating an error response
            error_message = f"Form validation failed: {change_password_form.errors}"
            response = HttpResponseBadRequest(error_message)
            return response
    else:
        change_password_form = CustomChangePasswordForm()