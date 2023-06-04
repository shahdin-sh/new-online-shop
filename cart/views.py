from django.shortcuts import render


def cart_detail_view(request):
    print(request)
    return render(request, 'cart_detail_view.html')
