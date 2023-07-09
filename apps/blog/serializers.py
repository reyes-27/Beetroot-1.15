from rest_framework import serializers
from .models import Post, Comment
from apps.category.serializers import CategorySerializer

class PostSerializer(serializers.ModelSerializer):
    category=CategorySerializer()
    class Meta:
        model=Post
        fields=(
            'id',
            'title',
            'slug',            
            'thumbnail',
            'description',
            'excerpt',
            'content',
            'time_read',
            'published',
            'category',
            'views',
            'parent',
            'user',
        )

class PostListSerializer(serializers.ModelSerializer):
    category=CategorySerializer()

    class Meta:
        model=Post
        fields=(
            'id',
            'title',
            'slug',            
            'thumbnail',
            'description',
            'excerpt',
            'time_read',
            'published',
            'category',
            'views',
            'parent',
            "user",
        )

class PostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model=Post
        fields=(
            'title',
            'thumbnail',
            'description',
            'excerpt',
            'content',
            'time_read',
            'published',
            'category',
            'views',
        )

class RePostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model=Post
        fields=(
            'title',
            'thumbnail',
            'description',
            'excerpt',
            'content',
            'time_read',
            'published',
            'category',
            'views',
        )

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model=Comment
        fields=(
            "description",
        )