from django.urls import path
from .views import (
    ProductsListView,
    ProductDetailView,
    ProductListByCategory,
    OrdersView,
    CartView,
    ItemView,
    CustomerView,
    )

urlpatterns = [
    path("customer/<uuid:pk>/", CustomerView.as_view(), name="customer_detail"),
    path("products/", ProductsListView.as_view(), name="products_list"),
    path("products/filtered/", ProductListByCategory.as_view(), name="filtered_products_list"),
    path("products/<uuid:pk>/", ProductDetailView.as_view(), name="product_detail"),
    path("orders/", OrdersView.as_view(), name="orders_list"),
    path("cart/", CartView.as_view(), name="user_cart"),
    path("cart/<uuid:pk>/", ItemView.as_view(), name="add_item"),
]
