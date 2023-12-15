from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from blog.forms import CommentForm
from blog.models import Post, Tag,  Category, Comment


def blog_grid(request):
    posts = Post.is_published_manager.all()

    # Create a Paginator object
    page_number = request.GET.get('page')
    paginator = Paginator(posts, 9)

    # Get the current page
    page_obj = paginator.get_page(page_number)

    breadcrumb_data = [{'lable': 'blog', 'title': 'Blog'}]

    context = {
        'page_obj': page_obj,
        'breadcrumb_data': breadcrumb_data,
    }
    return render(request, 'blog/blog_grid.html', context)


def post_detail(request, slug):
    posts = Post.is_published_manager.all()
    post = get_object_or_404(posts, slug=slug)
    # comment section
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            # Check the Honeypot Field
            if comment_form.cleaned_data.get('website') != "Leave this field blank" :
                new_comment.is_spam = True
            new_comment.post = post
            new_comment.author = request.user
            new_comment.save()
            return redirect(post.get_absolute_url())
    else:
        comment_form = CommentForm()

    breadcrumb_data = [{'lable': f'{post.title}', 'title':f'{post.title}', 'middle_lable':'blog', 'middle_url':'blog:blog_gird'}]

    context = {
        'post_detail': post,
        'tags': Tag.objects.all(),
        'categories': Category.objects.all(),
        'third_latest_post': Post.is_published_manager.order_by('-published_date')[:3],
        'comment_form': CommentForm(),
        'comments': Comment.is_not_spam_manager.filter(post=post).order_by('-timestamp'),
        'breadcrumb_data': breadcrumb_data,
    }
    return render(request, 'blog/post_detail.html', context)

def tag_detail_view(request, tag_slug):
    # get posts related to a tag
    tags = Tag.objects.all()
    tag = get_object_or_404(tags, slug=tag_slug)
    # defining 'posts' as a related name for tag field in Blog model
    tag_posts = tag.posts.all()

    # Create a Paginator object
    page_number = request.GET.get('page')
    paginator = Paginator(tag_posts, 9)

    # Get the current page
    page_obj = paginator.get_page(page_number)

    breadcrumb_data = [{'lable': f'{tag.name} tag', 'title':f'{tag.name} Tag', 'middle_lable':'blog','middle_url':'blog:blog_gird'}]
    
    context = {
        'page_obj': page_obj,
        'tag': tag, 
        'breadcrumb_data': breadcrumb_data,
    }
    return render(request, 'blog/tag_detail_view.html', context)



def category_detail_view(request, category_slug):
    # get posts related to a category
    categories = Category.objects.all()
    category = get_object_or_404(categories, slug=category_slug)

    # defining 'posts' as a related name for category field in Blog model
    category_posts = category.posts.all()

     # Create a Paginator object
    page_number = request.GET.get('page')
    paginator = Paginator(category_posts, 9)

    # Get the current page
    page_obj = paginator.get_page(page_number)

    breadcrumb_data = [{'lable': f'{category.name} category', 'title':f'{category.name} Category', 'middle_lable':'blog','middle_url':'blog:blog_gird'}]

    context = {
        'page_obj': page_obj,
        'category': category,
        'breadcrumb_data': breadcrumb_data,
    }
    return render(request, 'blog/category_detail_view.html', context)
