import logging
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest
from django.shortcuts import render, redirect
from django.utils import timezone
from django.utils.translation import gettext as _
from django.views.decorators.http import require_POST
from accounts.forms import CustomUserChangeForm, CustomChangePasswordForm
from accounts.models import CustomUserModel
from accounts.utils import persian_to_western_digits
from orders.forms import CustomerWithAddressForm
from orders.models import Order

# const values for breadcrumb data
breadcrumb_my_account = _('my_account')


@login_required
def wishlist_view(request):

    login_user = CustomUserModel.objects.prefetch_related('wished_product').get(username=request.user.username)


    breadcrumb_data = [{'lable': _('wishlist'), 'title': _('wishlist')}]
    return render(request, 'accounts/wishlist.html', context={'breadcrumb_data': breadcrumb_data, 'login_user': login_user,})


@login_required
def current_user_account(request):
    # accsesing users order
    user_orders = Order.objects.prefetch_related('items').filter(customer__user=request.user)

    breadcrumb_data = [{'lable': breadcrumb_my_account,'title': breadcrumb_my_account}]

    context = {
        'order_form': CustomerWithAddressForm(),
        'user_change_form': CustomUserChangeForm(),
        'password_change_form': CustomChangePasswordForm(user=request.user),
        'user_orders': user_orders,
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