from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Category


def home_page(request):
    # showing main category
    categories = Category.objects.filter(is_featured=True)
    products = Product.objects.filter(is_featured=True)
    context = {
        'categories': categories,
        'products': products,
    }
    return render(request, 'home.html', context)


def category_detail(request, slug):
    # with parent or none parent categories included.
    categories = Category.objects.all()
    category = get_object_or_404(categories, slug=slug)
    products = category.products.filter(is_active=True)
    context = {
        'category': category,
        'products': products,
    }
    return render(request, 'cateogories/category_detail_view.html', context)


def product_detail_view(request, product_slug):
    products = Product.objects.filter(is_active=True)
    product_detail = get_object_or_404(products, slug=product_slug)
    # develop comment system for users and guest!
    context = {
        'product_detail': product_detail
    }
    return render(request, 'products/product_detail_view.html', context)
