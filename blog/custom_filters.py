from django import template
from blog.models import Post

register = template.Library()

# Custom filter to get post count for each category
@register.filter
def get_item(dictionary, key):
    return dictionary.get(key, 0)

# Filter to get the count of posts in a category
@register.filter
def category_post_count(category):
    return Post.objects.filter(category=category).count()