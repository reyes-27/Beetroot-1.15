from django.contrib import admin
from .models import Post, Comment

# Register your models here.

class PostAdmin(admin.ModelAdmin):
    list_display=["id", "title"]
    list_display_links=["title"]
    list_per_page=25

admin.site.register(Post, PostAdmin)

class CommentAdmin(admin.ModelAdmin):
    list_display=["id", "description"]
    list_display_links=["description"]
    list_per_page=25

admin.site.register(Comment, CommentAdmin)