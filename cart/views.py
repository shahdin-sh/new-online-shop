from django.shortcuts import render


def cart_detail_view(request):
    return render(request, 'cart_detail_view.html')
