from .models import Blog


def blog_posts(request):
    data = {
        'posts': Blog.is_published_manager.all()[:3]
    }
    return data