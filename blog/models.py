from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

class Post(models.Model):
    CATEGORY_CHOICES = [
        ('Appetizer', 'Appetizer'),
        ('Main Course', 'Main Course'),
        ('Dessert', 'Dessert'),
        ('Soup', 'Soup'),
    ]

    STATUS_CHOICES = [
        ('Draft', 'Draft'),
        ('Published', 'Published'),
        ('Archived', 'Archived'),
    ]

    # Required Fields (Mapped)
    title = models.CharField(max_length=100)  # project_name
    description = models.TextField()
    start_date = models.DateField(default=timezone.now)  # start_date
    end_date = models.DateField(null=True, blank=True)  # end_date
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Draft')
    stakeholders = models.ManyToManyField(User, related_name='contributed_posts', blank=True)

    # Recipe Fields
    ingredients = models.TextField()
    instructions = models.TextField()
    cooking_time = models.PositiveIntegerField(help_text="Cooking time in minutes")
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='Main Course')
    image = models.ImageField(default='default_images/default_recipe_image.jpg', upload_to='post_images/')
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')

    # Like functionality
    likes = models.ManyToManyField(User, related_name='liked_posts', blank=True)

    # Save/Bookmark functionality
    saved_by = models.ManyToManyField(User, related_name='saved_posts', blank=True)

    def total_likes(self):
        return self.likes.count()

    def total_saves(self):
        return self.saved_by.count()

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})


class Comment(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-date_posted']

    def __str__(self):
        return f"{self.user.username} - {self.post.title}"