from django.urls import path
from .views import ListCategoryView
urlpatterns = [
    path("list/", ListCategoryView.as_view(), name="category_list")
]
