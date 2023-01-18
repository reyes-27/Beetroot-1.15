from rest_framework import serializers
from .models import UserProfile, CustomUser
from djoser.serializers import UserCreateSerializer

# class UserSerializer(UserCreateSerializer):
#     class Meta(UserCreateSerializer.Meta):
#         model=CustomUser
#         fields=[
#             'id',
#             'email',
#             'username',
#             'is_active',
#             'is_superuser',
#         ]

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = [
            "user",
            "first_name",
            "last_name",
        ]