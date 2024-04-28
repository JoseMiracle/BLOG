from django.db import models
from django.contrib.auth.models import AbstractUser
from blog.utils.base_class import BaseModel
# Create your models here.


def user_images_upload_location(instance, filename: str) -> str:
    """Get Location for user profile photo upload."""
    return f"accounts/images/{filename}"

class CustomUser(AbstractUser, BaseModel):
    """
        # NOTE: username, last_name, password inherited forom AbstractUser
    """
    email = models.EmailField(max_length=20, unique=True)
    first_name = models.CharField(max_length=25, null=False, blank=False)
    image = models.ImageField(upload_to=user_images_upload_location, blank=True)


    USERNAME_FIELD = "username"

    def __str__(self) -> str:
        return f"{self.username}"



