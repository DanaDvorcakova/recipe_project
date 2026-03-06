from django.contrib import admin
from .models import Post, Comment

# Admin site branding
admin.site.site_header = "Tasty Recipes Admin Page"
admin.site.site_title = "Tasty Recipes Admin Portal"
admin.site.index_title = "Welcome to Tasty Recipes Blog Admin"

# Custom admin class for Post
class PostAdmin(admin.ModelAdmin):
    class Media:
        css = {
            'all': ('css/custom_admin.css',) 
        }

# Register models
admin.site.register(Post, PostAdmin)  
admin.site.register(Comment)        
