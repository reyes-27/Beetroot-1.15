from django.contrib import admin
from .models import (
    Customer, 
    Product,
    Order,
    Cart,
    CartItem
    )
# Register your models here.

class CustomerAdmin(admin.ModelAdmin):
    list_display=["user", "email"]
    list_display_links=["email"]
    list_per_page=25

admin.site.register(Customer, CustomerAdmin)

class ProductAdmin(admin.ModelAdmin):
    list_per_page = 25
    list_display = ["id", "name", "customer"]
    list_display_links=["name"]

admin.site.register(Product, ProductAdmin)

class OrderAdmin(admin.ModelAdmin):
    list_per_page = 25
    list_display = ["id", "customer",]
    list_display_links = ["id"]

admin.site.register(Order, OrderAdmin)
admin.site.register(Cart)
admin.site.register(CartItem)