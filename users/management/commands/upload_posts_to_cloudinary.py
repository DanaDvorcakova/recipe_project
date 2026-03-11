import os
from django.core.management.base import BaseCommand
from blog.models import Post
from cloudinary.uploader import upload
from cloudinary.utils import cloudinary_url
from django.conf import settings

class Command(BaseCommand):
    help = "Upload all existing post images to Cloudinary"

    def handle(self, *args, **options):
        posts = Post.objects.all()
        for post in posts:
            if post.image and not post.image.url.startswith('http'):
                local_path = os.path.join(settings.MEDIA_ROOT, str(post.image))
                if os.path.exists(local_path):
                    self.stdout.write(f"Uploading {post.image}...")
                    try:
                        res = upload(local_path, folder="post_images")
                        post.image = res['public_id']  # update ImageField to point to Cloudinary
                        post.save()
                        self.stdout.write(self.style.SUCCESS(f"Uploaded: {post.image}"))
                    except Exception as e:
                        self.stdout.write(self.style.ERROR(f"Failed: {post.image} -> {e}"))
                else:
                    self.stdout.write(self.style.WARNING(f"File not found: {local_path}"))
        self.stdout.write(self.style.SUCCESS("Done uploading all post images!"))