import uuid
from django.conf import settings
from django.db import models
from django.utils import timezone
from .managers import CustomUserManager
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
)
# Create your models here.

class CustomUser(AbstractBaseUser, PermissionsMixin):
    id =             models.UUIDField(
                                    primary_key=True,
                                    default=uuid.uuid4,
                                    editable=False,
                                    )

    email =          models.EmailField(max_length=255, unique=True)
    username =       models.CharField(max_length=20, unique=True)
    is_active =      models.BooleanField(default=True)
    is_staff =       models.BooleanField(default=False)
    
    USERNAME_FIELD="email"
    REQUIRED_FIELDS = [
        "username",
    ]
    
    objects = CustomUserManager()
    
    def __str__(self):
        return self.email

def profile_pic_directory(filename, instance):
    return "profiles/{1}/{2}".format(instance, filename)


class UserProfile(models.Model):
    user =              models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="user_profile")
    first_name =        models.CharField(max_length=100)
    last_name =         models.CharField(max_length=100)
    profile_pic =       models.ImageField(upload_to=profile_pic_directory, max_length=500, default="profiles/default.jpg")
    creation_date =     models.DateTimeField(auto_now=timezone.now())

    def __str__(self):
        return self.user.username



