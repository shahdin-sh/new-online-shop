import logging
from allauth.account.urls import *
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib import messages
from django.db.models import Prefetch
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from cart.forms import AddToCartForm
from products.forms import CommentForm
from products.models import Product, Category, Comment

# Create a logger
logger = logging.getLogger(__name__)


def shop_categories(request):

    products = Product.objects.select_related('category').filter(category__isnull=False, activation=True).order_by('-datetime_created')

    # Create a Paginator object
    page_number = request.GET.get('page')
    paginator = Paginator(products, 9)

    # Get the current page
    page_obj = paginator.get_page(page_number)

    # Create a range of page numbers (e.g., 3 pages before and 3 pages after the current page)
    page_range = range(max(1, page_obj.number - 3), min(paginator.num_pages, page_obj.number + 3))

    breadcrumb_data = [{'lable':'store', 'title': 'Store'}]
    context = {
        'products': page_obj,
        'page_range': page_range,
        'breadcrumb_data': breadcrumb_data,
    }
    return render(request, 'categories/shop_categories.html', context)


def products_or_category_detail(request, category_slug):
    
    categories = Category.objects.prefetch_related(
        Prefetch(
            'products', queryset=Product.objects.prefetch_related('user_wished_product').filter(activation=True, category__products__isnull=False)
        )).all()
    
    category = get_object_or_404(categories, slug=category_slug)

    breadcrumb_data = [{'lable':f'{category.name}', 'title': f'{category.name}', 'middle_lable': 'store', 'middle_url':'products:product_categories'}]
    context = {
        'category': category,
        'breadcrumb_data': breadcrumb_data,
    }
    return render(request, 'categories/category_detail.html', context)


def product_detail_view(request, product_slug):

    products = Product.objects.prefetch_related('comments').filter(activation=True)
    product_detail = get_object_or_404(products, slug=product_slug)

    # comment section
    current_session = request.session.session_key
    if request.method == 'POST':
        comment_form = CommentForm(request, request.POST)
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
            if comment_form.cleaned_data['website'] != 'please leave this field blank.':
                new_comment.is_spam = True
            new_comment.product = product_detail

            # check if user is authenticated, give author to DB and if it is not just give name and email as a guest
            if request.user.is_authenticated:
                new_comment.author = request.user
            else:
                # restorig name and email in the session
                guest_data  = request.session['guest_data'] = {
                    'name': comment_form.cleaned_data['name'],
                    'email': comment_form.cleaned_data['email'],
                }
                print(guest_data)
                new_comment.session_token = current_session
                new_comment.name = guest_data['name']
                new_comment.email = guest_data['email']

            # The clean_email method will be called during the form validation, and the validation error will be raised if needed.
            comment_form.clean()
            new_comment.save()

            return redirect(reverse('products:product_detail', args=[product_slug]))
        else:
            # Log form errors
            logger.error("Form validation failed: %s", comment_form.errors)
    else:
        comment_form = CommentForm(request)

    breadcrumb_data = [{'lable':f'{product_detail.name}', 
                        'title': f'{product_detail.name}', 
                        'middle_lable': f'{product_detail.category.name}', 
                        'middle_url': 'products:category_detail',
                        'middle_url_args': product_detail.category.slug
                    }]
    
    context = {
        'product_detail': product_detail,
        'comments': product_detail.comments.filter(parent=None, is_spam=False),
        'comment_form': comment_form,
        'add_to_cart_form': AddToCartForm(product_stock=product_detail.quantity),
        'breadcrumb_data': breadcrumb_data,
    }

    return render(request, 'products/product_detail_view.html', context)


@login_required
def add_to_wishlist(request, product_slug):
    # this view is using in product_detail
    products = Product.is_active.all()
    product_detail = get_object_or_404(products, slug=product_slug)
    if request.user not in product_detail.user_wished_product.all():
        product_detail.user_wished_product.add(request.user)
        messages.success(request, f'{product_detail.name} add to your wishlist successfuly.')
        return redirect('account:wishlist_view')
    return HttpResponse('this product has already added to your wishlist.')


@login_required
def remove_from_wishlist(request, product_slug):
    # this view is using in product_detail
    products = Product.is_active.all()
    product_detail = get_object_or_404(products, slug=product_slug)
    if request.user in product_detail.user_wished_product.all():
        product_detail.user_wished_product.remove(request.user)
        messages.success(request, f'{product_detail.name} remove from your wishlist successfuly.')
        return redirect('account:wishlist_view')
    return HttpResponse('this product is not existing in your wishlist.')

# Every function based views should be impelemented as class based views too: 