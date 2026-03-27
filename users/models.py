from django.db import models
from django.contrib.auth.models import User

from cloudinary_storage.storage import MediaCloudinaryStorage
from cloudinary.utils import cloudinary_url
from django.templatetags.static import static

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(
        upload_to='profile_pics',
        storage=MediaCloudinaryStorage(),
        null=True, # a missing profile image is handled by get_image_url
    )


    def get_image_url(self):
        if self.image:
            if "default_profile" not in self.image.name:
                return cloudinary_url(self.image.name, width=300, height=300, crop="lfill")[0]
        return static('users/images/default_profile.png')
