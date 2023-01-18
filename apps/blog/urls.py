from django.urls import path
from .views import (
    BlogListView,
    BlogListViewByCategories,
    PostCreateView,
    RepostCreateView,
    RepostByPostListView,
    PostDetail,
    CommentCreateView,
    AnswerCreateView,
    DashboardView,
    )

urlpatterns = [
    path("list/", BlogListView.as_view(), name="blog_list"),
    path("list_by_category/", BlogListViewByCategories.as_view(), name="blog_list_by_cat"),
    path("create_post/", PostCreateView.as_view(), name="create_post"),
    path('create_repost/', RepostCreateView.as_view(), name='create_repost'),
    path("list/reposts/", RepostByPostListView.as_view(), name="list_reposts"),
    path("post/<uuid:pk>/", PostDetail.as_view(), name="post_detail"),
    path("create_comment/<uuid:pk>/", CommentCreateView.as_view(), name="create_comment"),
    path('answer_comment/<uuid:pk>/', AnswerCreateView.as_view(), name="create_answer"),
    path("dashboard/", DashboardView.as_view(), name="dashboard")
]
