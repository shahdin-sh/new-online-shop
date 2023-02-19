from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate

def wishlist_view(request):
    return render(request, 'accounts/wishlist.html')