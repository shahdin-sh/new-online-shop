from django.shortcuts import render
from .models import Blog
from django.core.paginator import Paginator

def blog_grid(request):
    posts = Blog.is_published_manager.all()

     # Create a Paginator object
    page_number = request.GET.get('page')
    paginator = Paginator(posts, 4)

    # Get the current page
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'blog/blog_grid.html', context)

