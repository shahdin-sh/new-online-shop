from django.shortcuts import render, redirect, get_object_or_404
from .models import Product


def products_list_view(request):
    products = Product.objects.filter(is_active=True)

    context = {
        'products': products
    }
    return render(request, 'products/products_list_view.html', context)


def product_detail_view(request, pk):
    products = Product.objects.filter(is_active=True)
    products_detail = get_object_or_404(products, pk=pk)

    context = {
        'product_details': products_detail,
    }
    return render(request, 'products/product_detail_view.html', context)
