from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from orders.forms import OrderForm


@login_required
def wishlist_view(request):
    return render(request, 'accounts/wishlist.html')


@login_required
def my_account(request):
    context = {
        'order_form': OrderForm()
    }
    return render(request, 'accounts/my_account.html', context)