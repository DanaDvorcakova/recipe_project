from django.urls import path
from .views import (
    PostListView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    UserPostListView,
    CategoryPostListView,
    like_post,
    recipe_detail_json,
    live_search,
    load_more_comments,
    about,
    publish_post,
    toggle_save,
    saved_posts,
    delete_post,
    post_detail,  # Add post_detail here
)

urlpatterns = [
    # Home page with Post List
    path('', PostListView.as_view(), name='blog-home'),

    # Post detail view with comments
    path('post/<int:pk>/', post_detail, name='post-detail'),

    # Post creation, update, delete
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),

    # User-specific posts
    path('user/<str:username>', UserPostListView.as_view(), name='user-posts'),

    # Category-specific posts
    path('category/<str:category>/', CategoryPostListView.as_view(), name='category-posts'),

    # Like and other post interactions
    path('post/<int:post_id>/like/', like_post, name='like-post'),
    path('post/<int:pk>/json/', recipe_detail_json, name='recipe-detail-json'),
    path('live-search/', live_search, name='live_search'),
    path('post/<int:pk>/load-more-comments/', load_more_comments, name='load-more-comments'),

    # About page
    path('about/', about, name='blog-about'),

    # Post publish action
    path('post/<int:pk>/publish/', publish_post, name='publish-post'),

    # Toggle save action
    path('toggle-save/', toggle_save, name='toggle-save'),

    # Saved posts route
    path('saved/', saved_posts, name='saved-posts'),

    # Route for deleting post (based on the class or function view chosen)
    path('post/<int:pk>/delete/', delete_post, name='delete-post'),
]