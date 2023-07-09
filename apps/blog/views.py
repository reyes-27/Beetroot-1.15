from rest_framework.views import APIView
from rest_framework.generics import (
    CreateAPIView,
    RetrieveAPIView,
    RetrieveUpdateDestroyAPIView
    )
from .serializers import (
    PostSerializer, 
    PostListSerializer, 
    PostCreateSerializer, 
    RePostCreateSerializer,
    CommentSerializer
    )
from .models import Post, ViewCount, Comment
from rest_framework import permissions, status
from . import permissions as custom_permissions
from rest_framework.response import Response
from apps.category.models import Category
from slugify import slugify
from .pagination import *

#=======================================================================================>

class BlogListView(APIView):
    permission_classes=(permissions.IsAuthenticated,)
    def get(self, request, format=None):
        if Post.objects.all().exists():
            posts=Post.objects.all()
            paginator=SmallSetPagination()
            results=paginator.paginate_queryset(posts, request)
            serializer=PostListSerializer(results, many=True)
            return paginator.get_paginated_response({"posts":serializer.data})
        else:
            return Response({"error": "No posts found"}, status=status.HTTP_404_NOT_FOUND)

class BlogListViewByCategories(APIView):
    #If category has a parent it's children(I gotta show children posts only)
    #Else it's a parent(I gotta show parent and children posts)
    #Do it by your own

    permission_classes=(permissions.AllowAny,)
    def get(self, request, format=None):
        if Post.objects.all().exists():
            posts=Post.objects.order_by("-published").all()
            category_slug=request.query_params.get("category_slug")
            category=Category.objects.get(slug=category_slug)
            if Category.objects.filter(parent=category).exists():
                #It's a children and has a parent lmao
                sub_categories=Category.objects.filter(parent=category)
                filtered_categories=[category]
                for sub_category in sub_categories:
                    filtered_categories.append(sub_category)
                filtered_categories=tuple(filtered_categories)
                posts=posts.filter(category__in=filtered_categories)
            else:
                posts=posts.filter(category=category)

            paginator=SmallSetPagination()
            results=paginator.paginate_queryset(posts, request)
            serializer=PostListSerializer(results, many=True)

            return paginator.get_paginated_response({"posts": serializer.data})
        else:
            return Response({"message":"Error"}, status=status.HTTP_404_NOT_FOUND)
    

class PostCreateView(CreateAPIView):
    permission_classes=(permissions.IsAuthenticated,)
    serializer_class=PostCreateSerializer

    def perform_create(self, serializer):
        # data={
        #     'title': self.request.data.get("title"),
        #     'slug': self.request.data.get("title").lower(),
        #     'thumbnail': self.request.data.get("thumbnail"),
        #     'excerpt': self.request.data.get("excerpt"),
        #     'content': self.request.data.get("content"),
        #     'description': self.request.data.get("description"),
        #     'time_read': self.request.data.get("time_read"),
        #     'published': self.request.data.get("published"),
        #     'category': self.request.data.get("category"),
        #     'user': self.request.user,
        # }
        slug=self.request.data["title"]
        slug=slugify(slug)
        if serializer.is_valid():
            serializer.save(user=self.request.user.user_profile, slug=slug)
            return Response({"success":serializer.data}, status=status.HTTP_201_CREATED)
        else:
            return Response({"error": "Your data is not valid"}, status=status.HTTP_400_BAD_REQUEST)

class RepostCreateView(CreateAPIView):
    permission_classes=(permissions.IsAuthenticated,)
    serializer_class=RePostCreateSerializer
    def perform_create(self, serializer):
        data={
            'title': self.request.data.get("title"),
            'slug': self.request.data.get("title").lower(),
            'thumbnail': self.request.data.get("thumbnail"),
            'excerpt': self.request.data.get("excerpt"),
            'content': self.request.data.get("content"),
            'description': self.request.data.get("description"),
            'time_read': self.request.data.get("time_read"),
            'published': self.request.data.get("published"),
            'category': self.request.data.get("category"),
            'parent': self.request.data.get("parent"),
            'user': self.request.user,  
        }
        parent=Post.objects.get(slug=self.request.query_params.get("post_slug"))
        slug=self.request.data["title"]
        slug=slugify(slug)
        if serializer.is_valid():
            serializer.save(user=self.request.user.user_profile, parent=parent, slug=slug, category=parent.category)
            
            return Response({"success":serializer.data,}, status=status.HTTP_201_CREATED)

        else:
            return Response({'error':"couldn't be reposted"}, status=status.HTTP_400_BAD_REQUEST)

class RepostByPostListView(APIView):
    def get(self, request, format=None):
        if Post.objects.all().exists():
            initial_query=Post.objects.order_by("published").all()
            parent=Post.objects.get(slug=request.query_params.get("post_slug"))
            if Post.objects.filter(parent=parent).exists():
                children=Post.objects.select_related("parent").filter(parent=parent)
                query_list=[parent]
                for child in children:
                    query_list.append(child)
                query_list=tuple(query_list)
                
                final_query=initial_query.filter(parent__in=query_list)
                print(final_query)
                
            paginator=MediumSetPagination()
            results=paginator.paginate_queryset(final_query, request)
            serializer=PostListSerializer(results, many=True)

            return paginator.get_paginated_response({"list":serializer.data})
        else:
            return Response({"list":"error"}, status=status.HTTP_400_BAD_REQUEST)


            
class PostDetail(RetrieveUpdateDestroyAPIView):
    queryset=Post.objects.all()
    permission_classes=(permissions.AllowAny,)
    serializer_class=PostSerializer

class CommentCreateView(CreateAPIView):
    permission_classes=(permissions.IsAuthenticated,)
    serializer_class=CommentSerializer
    def perform_create(self, serializer):
        pk=self.kwargs["pk"]
        print(pk, "<--------- PK")
        post=Post.objects.get(id=pk)
        serializer.save(user=self.request.user.user_profile, post=post)
        
        if serializer.is_valid():
            return Response({"success": "Created",}, status=status.HTTP_201_CREATED)
        else:
            return Response({"Error":"Not created"}, status=status.HTTP_400_BAD_REQUEST)

class AnswerCreateView(CreateAPIView):
    permission_classes=(permissions.IsAuthenticated,)
    serializer_class=CommentSerializer
    def perform_create(self, serializer):
        pk=self.kwargs["pk"]
        parent=Comment.objects.get(pk=pk)
        serializer.save(user=self.request.user.user_profile, parent=parent, post=parent.post)



class DashboardView(APIView):
    def get(self, request, format=None):
        if Post.objects.filter(user=request.user.user_profile).exists():
            posts=Post.objects.order_by("-published").all()
            posts=posts.filter(user=request.user.user_profile)
            paginator=LargeSetPagination()
            results=paginator.paginate_queryset(posts, request)
            serializer=PostListSerializer(results, many=True)

            return paginator.get_paginated_response({"posts":serializer.data})
        else:
            return Response({"Error":"You don\'t have any posts"}, status=status.HTTP_204_NO_CONTENT)