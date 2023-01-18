
import uuid
from django.db import models
from apps.category.models import Category
from django.utils import timezone
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from apps.accounts.models import UserProfile

# Create your models here.

def post_thumbnail_directory(instance, filename):
    return 'blog/{0}/{1}'.format(instance, filename)

class Post(models.Model):
    id=             models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title=          models.CharField(max_length=255)
    slug=           models.SlugField(max_length=255, unique=True)
    thumbnail=      models.ImageField(upload_to=post_thumbnail_directory, blank=True, null=True, max_length=500)
    excerpt=        models.CharField(max_length=255)
    content=        RichTextUploadingField(blank=True, null=True)
    description=    models.TextField(blank=True, null=True)
    time_read=      models.IntegerField(default=0)
    published=      models.DateTimeField(auto_now=timezone.now())
    category=       models.ForeignKey(Category, on_delete=models.PROTECT)
    views=          models.IntegerField(default=0)
    parent=         models.ForeignKey("self",blank=True, null=True, on_delete=models.CASCADE, related_name="children")
    user=           models.ForeignKey(UserProfile, null=True, on_delete=models.SET_NULL)

    class Meta:
        ordering=["-published"]

    def __str__(self):
        return self.title
        
    
    def get_view_count(self):
        views=ViewCount.object.filter(post=self).count()
        return views

class ViewCount(models.Model):
    post=models.ForeignKey(Post, related_name="post_view_count", on_delete=models.CASCADE)
    ip_address=models.CharField(max_length=255)
    def __str__(self):
        return f'{self.ip_address}'

class AdminPost(models.Model):
    title=          models.CharField(max_length=255)
    slug=           models.SlugField(max_length=255, unique=True)
    thumbnail=      models.ImageField(upload_to=post_thumbnail_directory, blank=True, null=True, max_length=500)
    excerpt=        models.CharField(max_length=255)
    content=        RichTextUploadingField(blank=True, null=True)
    description=    models.TextField(blank=True, null=True)
    time_read=      models.IntegerField(default=0)
    published=      models.DateTimeField(auto_now=timezone.now())
    category=       models.ForeignKey(Category, on_delete=models.PROTECT)
    views=          models.IntegerField(default=0)
    user=           models.ForeignKey(UserProfile, null=True, on_delete=models.SET_NULL)

class Comment(models.Model):
    id=             models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    post=           models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    description=    RichTextField(null=True, blank=True)
    user=           models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="user_posts")
    parent=         models.ForeignKey("self",blank=True, null=True, on_delete=models.CASCADE, related_name="children")
    