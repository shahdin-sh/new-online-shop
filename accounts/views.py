from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required


@login_required
def wishlist_view(request):
    return render(request, 'accounts/wishlist.html')