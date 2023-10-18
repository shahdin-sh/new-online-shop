from .models import Post


def blog_posts(request):
    data = {
        'posts': Post.is_published_manager.all()[:3]
    }
    return data