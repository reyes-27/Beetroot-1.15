from django.contrib import admin
from .models import UserProfile
# Register your models here.

class UserProfileAdmin(admin.ModelAdmin):
    list_per_page=25
    list_display=[
        "user",
        "first_name",
        "last_name",
    ]
    list_display_links=[
        "user"
    ]

admin.site.register(UserProfile, UserProfileAdmin)
