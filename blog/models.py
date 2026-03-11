from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from cloudinary_storage.storage import MediaCloudinaryStorage
from cloudinary.utils import cloudinary_url
from django.templatetags.static import static

# -------------------- Recipe Post --------------------
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

    # Required Fields
    title = models.CharField(max_length=100)
    description = models.TextField()
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Draft')
    stakeholders = models.ManyToManyField(User, related_name='contributed_posts', blank=True)

    # Recipe Fields
    ingredients = models.TextField()
    instructions = models.TextField()
    cooking_time = models.PositiveIntegerField(help_text="Cooking time in minutes")
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='Main Course')

    image = models.ImageField(
        upload_to='post_images/',
        storage=MediaCloudinaryStorage(),
        blank=True,
        null=True,
        default=None  # Keep None; fallback handled in get_image_url()
    )

    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')

    # Like & Save functionality
    likes = models.ManyToManyField(User, related_name='liked_posts', blank=True)
    saved_by = models.ManyToManyField(User, related_name='saved_posts', blank=True)

    def total_likes(self):
        return self.likes.count()

    def total_saves(self):
        return self.saved_by.count()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})

    def get_image_url(self):
        """
        Returns:
        - Cloudinary URL if an image is uploaded
        - Otherwise, fallback to default static image
        """
        if self.image and hasattr(self.image, 'name') and self.image.name:
            # Uploaded image
            return cloudinary_url(self.image.name, width=800, height=600, crop="fill")[0]
        # Fallback default image
        return static('blog/images/default_recipe_image.jpg')

# -------------------- Comments --------------------
class Comment(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-date_posted']

    def __str__(self):
        return f"{self.user.username} - {self.post.title}"

