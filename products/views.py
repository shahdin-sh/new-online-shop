from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.urls import reverse
from django.http import HttpResponse
from .models import Product, Category, Comment
from .forms import CommentForm
from cart.forms import AddToCartForm
from cart.cart import Cart
# from cart.forms import AddToCartForm


def home_page(request):
    return render(request, 'home.html')


def shop_categories(request):
    products = Product.is_active_manager.filter(category__isnull=False, is_featured=False)
    context = {
        'products': products,
    }
    return render(request, 'categories/shop_categories.html', context)


def products_or_category_detail(request, category_slug):
    categories = Category.is_featured_manager.all()
    category = get_object_or_404(categories, slug=category_slug)
    context = {
        'category': category,
    }
    return render(request, 'categories/category_detail.html', context)

def product_detail_view(request, product_slug):
    products = Product.is_active_manager.filter(is_featured=False)
    product_detail = get_object_or_404(products, slug=product_slug)
    comment_form = CommentForm(request.POST)
    # comment section
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
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
            # comment section
            new_comment = comment_form.save(commit=False)
            new_comment.product = product_detail
            # check if user is authenticated, give author to DB and if it is not just give name and email
            if request.user.is_authenticated:
                new_comment.author = request.user
            else:
                new_comment.session_token = request.session.session_key
            # getting rating from stars label
            # rating = request.POST.get('rating')
            # new_comment.rating = rating
            # The clean_email method will be called during the form validation, and the validation error will be raised if needed.
            new_comment.save()
            return redirect(reverse('products:product_detail', args=[product_slug]))
    else:
        comment_form = CommentForm()
    comments = product_detail.comments.filter(parent=None).order_by('-datetime_created')
    context = {
        'product_detail': product_detail,
        'comments': comments,
        'comment_form': comment_form,
        'add_to_cart_form': AddToCartForm(product_stock=product_detail.quantity),
    }
    return render(request, 'products/product_detail_view.html', context)


@login_required
def add_to_wishlist(request, product_slug):
    # this view is using in product_detail
    products = Product.is_active_manager.filter(is_featured=False)
    product_detail = get_object_or_404(products, slug=product_slug)
    if request.user not in product_detail.user_wished_product.all():
        product_detail.user_wished_product.add(request.user)
        return redirect('account:wishlist_view')
    return HttpResponse('this product has already added to your wishlist.')


@login_required
def remove_from_wishlist(request, product_slug):
    # this view is using in product_detail
    products = Product.is_active_manager.filter(is_featured=False)
    product_detail = get_object_or_404(products, slug=product_slug)
    if request.user in product_detail.user_wished_product.all():
        product_detail.user_wished_product.remove(request.user)
        return redirect('account:wishlist_view')
    return HttpResponse('this product has already removed from your wishlist.')

# Every function based views should be impelemented as class based views too: 