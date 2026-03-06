from .models import Post
from django.db.models import Count

def categories_processor(request):
    # Categories with counts, exclude empty categories
    categories = (
        Post.objects
        .exclude(category='')  
        .values('category')
        .annotate(count=Count('id'))  
        .order_by('category')
    )

    category_list = [
        {
            'category': item['category'], 
            'count': item['count']
        }
        for item in categories
    ]

    # Latest 3 posts globally
    latest_posts = Post.objects.order_by('-date_posted')[:3]

    return {
        'categories': category_list,
        'latest_posts': latest_posts
    }

def most_liked_recipe(request):
    top_post = Post.objects.annotate(
        total_likes=Count('likes')
    ).order_by('-total_likes').first()
    return {'most_liked_post': top_post}


def saved_posts_count(request):
    if request.user.is_authenticated:
        count = request.user.saved_posts.count()
    else:
        count = 0

    return {
        'saved_count': count
    }

