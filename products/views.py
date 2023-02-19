from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Product, Category, Comment
from .forms import CommentForm


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
    current_user = request.user
    # comment section 
    comments = product_detail.comments.filter(is_active=True, parent=None).order_by('-datetime_created')
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid:
            # reply section
            parent_obj = None
            # get parent comment id from hidden input
                # id integer e.g. 15
            try: 
                parent_id = int(request.POST.get('parent_id'))
            except TypeError:
                parent_id = None
            # if parent_id has been submitted get parent_obj
            if parent_id:
                parent_obj = Comment.objects.get(id=parent_id)
                # if parent_obj exist
                if parent_obj:
                    reply_comment = comment_form.save(commit=False)
                    #assign parent obj to reply comment
                    reply_comment.parent = parent_obj
            # normal comment section
            new_comment = comment_form.save(commit=False)
            new_comment.product = product_detail
            new_comment.author = current_user
            # getting rating from stars label
            rating = request.POST.get('rating')
            new_comment.rating = rating
            new_comment.save()
        return redirect(product_detail_view, product_slug=product_slug)
    else:
        comment_form = CommentForm()
    context = {
        'product_detail': product_detail,
        # showing all of product's comments
        'comments': comments,
        'comment_form': comment_form,
    }
    return render(request, 'products/product_detail_view.html', context)


def add_to_wishlist(request, product_slug):
    products = Product.objects.filter(is_active=True)
    product_detail = get_object_or_404(products, slug=product_slug)
    print(product_detail.user_wished_product.all())
    if request.user not in product_detail.user_wished_product.all():
        product_detail.user_wished_product.add(request.user)
        return redirect(product_detail_view, product_slug=product_slug)
    return HttpResponse('this product has already added to your wishlist.')


def remove_from_wishlist(request, product_slug):
    products = Product.objects.filter(is_active=True)
    product_detail = get_object_or_404(products, slug=product_slug)
    if request.user in product_detail.user_wished_product.all():
        product_detail.user_wished_product.remove(request.user)
        redirect(product_detail_view, product_slug=product_slug)
        return redirect(product_detail_view, product_slug=product_slug)
    return HttpResponse('this product has already removed from your wishlist.')
