from blog.models import Post


def blog_posts(request):
    
    data = {
        'posts': Post.objects.select_related('category').filter(is_published=True)[:3]
    }
    return data