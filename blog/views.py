from django.shortcuts import render, get_object_or_404
from .models import Blog, Tag,  Category
from django.core.paginator import Paginator

def blog_grid(request):
    posts = Blog.is_published_manager.all()

    # Create a Paginator object
    page_number = request.GET.get('page')
    paginator = Paginator(posts, 9)

    # Get the current page
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'blog/blog_grid.html', context)


def post_detail(request, slug):
    posts = Blog.is_published_manager.all()
    post = get_object_or_404(posts, slug=slug)
    context = {
        'post_detail': post,
        'tags': Tag.objects.all(),
        'categories': Category.objects.all()
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

    context = {
        'page_obj': page_obj,
        'tag': tag, 
    }
    return render(request, 'blog/tag_detail_view.html', context)
