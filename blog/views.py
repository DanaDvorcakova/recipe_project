from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.http import JsonResponse, HttpResponseForbidden
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Count
from django.contrib import messages
from django.conf import settings


from .models import Post, Comment
from .forms import PostForm, CommentForm

User = get_user_model()

# ---------------- Helper Functions ----------------

def paginate_queryset(queryset, request, per_page=6):
    """Helper function for pagination."""
    paginator = Paginator(queryset, per_page)
    page_number = request.GET.get('page', 1)
    return paginator.get_page(page_number)

def get_most_liked_post():
    """Helper function to fetch the most liked post."""
    return Post.objects.annotate(
        total_likes=Count('likes')
    ).order_by('-total_likes', '-date_posted').first()

# ---------------- Home / Post List ----------------
class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    paginate_by = 6

    def get_queryset(self):
        queryset = Post.objects.all().order_by('-date_posted')
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query) |
                Q(ingredients__icontains=query)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = (
            Post.objects.exclude(category='')
            .values('category')
            .annotate(count=Count('id'))
            .order_by('category')
        )
        context['latest_posts'] = Post.objects.order_by('-date_posted')[:3]
        context['most_liked_post'] = get_most_liked_post()
        return context

# ---------------- Post Detail ----------------
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments_list = post.comments.all().order_by('-date_posted')
    page_obj = paginate_queryset(comments_list, request, per_page=2)

    if request.method == 'POST' and request.user.is_authenticated:
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.post = post
            comment.save()
            messages.success(request, "Comment added successfully!")
            return redirect('post-detail', pk=post.pk)
    else:
        form = CommentForm()

    context = {
        'post': post,
        'comments': page_obj,
        'form': form,
        'has_more_comments': page_obj.has_next(),
        'next_page': page_obj.next_page_number() if page_obj.has_next() else None,
        'comments_count': post.comments.count(),
    }
    return render(request, 'blog/post_detail.html', context)

# ---------------- Load More Comments ----------------
def load_more_comments(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments_list = post.comments.all().order_by('-date_posted')
    page_obj = paginate_queryset(comments_list, request, per_page=2)

    comments_data = []
    for c in page_obj:
        # Default profile image
        profile_image_url = '/media/default_images/default_profile.jpg'

        # Check if profile exists and has an image
        if hasattr(c.user, 'profile') and getattr(c.user.profile, 'image', None):
            profile_image_url = c.user.profile.image.url

        comments_data.append({
            'id': c.id,
            'username': c.user.username,
            'profile_image_url': profile_image_url,
            'content': c.content,
            'date_posted': c.date_posted.strftime("%b %d, %Y %H:%M")
        })

    return JsonResponse({
        'comments': comments_data,
        'has_next': page_obj.has_next(),
        'next_page': page_obj.next_page_number() if page_obj.has_next() else None
    })

# ---------------- Post Create / Update / Delete ----------------
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author or self.request.user in post.stakeholders.all()

    def handle_no_permission(self):
        return HttpResponseForbidden("You cannot edit this post.")

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

    def handle_no_permission(self):
        return HttpResponseForbidden("You cannot edit this post.")

    def post(self, request, *args, **kwargs):
        # Ensure the post is deleted and a success message is sent
        post = self.get_object()
        if self.request.user == post.author:
            post.delete()
            messages.success(request, f"The post '{post.title}' has been deleted successfully.")
            return redirect('blog-home')  # Redirect to the home page or wherever you want
        else:
            messages.error(request, "You are not authorized to delete this post.")
            return redirect('blog-home')

# ---------------- User & Category Posts ----------------
class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'
    context_object_name = 'posts'
    paginate_by = 6

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return user.posts.order_by('-date_posted')

class CategoryPostListView(ListView):
    model = Post
    template_name = 'blog/category_posts.html'
    context_object_name = 'posts'
    paginate_by = 6

    def get_queryset(self):
        category = self.kwargs.get('category')
        return Post.objects.filter(category=category).order_by('-date_posted')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category_name'] = self.kwargs.get('category')
        return context

# ---------------- Like Post ----------------
@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    user = request.user

    if user in post.likes.all():
        post.likes.remove(user)
        liked = False
    else:
        post.likes.add(user)
        liked = True

    total_likes = post.likes.count()

    # Find the post with the most likes
    most_liked_post = get_most_liked_post()

    return JsonResponse({
        'liked': liked,
        'total_likes': total_likes,
        'most_liked_post_id': most_liked_post.id if most_liked_post else None,
        'most_liked_post_likes': most_liked_post.likes.count() if most_liked_post else 0
    })

# ---------------- Toggle Save ----------------
@login_required
def toggle_save(request):
    if request.method == "POST":
        post_id = request.POST.get("post_id")
        post = get_object_or_404(Post, id=post_id)

        if request.user in post.saved_by.all():
            post.saved_by.remove(request.user)
            saved = False
        else:
            post.saved_by.add(request.user)
            saved = True

        # Build saved posts list with image URLs
        saved_posts_qs = request.user.saved_posts.order_by('-date_posted')
        saved_posts_list = [{
            "id": p.id,
            "title": p.title,
            "image_url": p.image.url if p.image else None
        } for p in saved_posts_qs]

        return JsonResponse({
            'saved': saved,
            'total_saves': saved_posts_qs.count(),
            'saved_posts': saved_posts_list
        })

# ---------------- Saved Posts List ----------------
@login_required
def saved_posts(request):
    posts = request.user.saved_posts.all().order_by('-date_posted')
    return render(request, 'blog/saved_posts.html', {'posts': posts})

# ---------------- About ----------------
def about(request):
    featured_posts = Post.objects.order_by('-date_posted')[:3]
    return render(request, 'blog/about.html', {'title': 'About', 'featured_posts': featured_posts})

# ---------------- Recipe JSON for Modal ----------------
def recipe_detail_json(request, pk):
    try:
        post = Post.objects.get(pk=pk)
        return JsonResponse({
            'title': post.title,
            'image_url': post.image.url if post.image else None,
            'description': post.description,
            'ingredients': post.ingredients,
            'instructions': post.instructions,
        })
    except Post.DoesNotExist:
        return JsonResponse({'error': 'Recipe not found'}, status=404)

# ---------------- Live Search ----------------
def live_search(request):
    query = request.GET.get('q', '')
    if query:
        recipes = Post.objects.filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        )[:10]
        results = list(recipes.values('id', 'title'))
    else:
        results = []
    return JsonResponse(results, safe=False)

# ---------------- Publish Post ----------------
@login_required
def publish_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user == post.author and post.status == 'Draft':
        post.status = 'Published'
        post.save()
    return redirect('post-detail', pk=pk)

# ---------------- Delete Post ----------------
def delete_post(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if post.author == request.user:
        if request.method == "POST":
            post.delete()
            messages.success(request, f"The post '{post.title}' has been deleted successfully.")
            return redirect('blog-home')
    else:
        messages.error(request, "You are not authorized to delete this post.")
        return redirect('blog-home')

    return render(request, 'blog/post_confirm_delete.html', {'object': post})