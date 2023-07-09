from .models import (
    Cart,
    CartItem,
    Customer,
)
from django.db.models import Sum, F
from rest_framework.response import Response

class CartObject:
    def __init__(self, request):
        cart = Cart.objects.filter(user=request.user.user_customer).first()
        if cart:
            self.cart = cart
        else:
            self.cart = self.new(request)

    # def __iter__(self):
    #     for item in self.cart.items.all():
    #         yield item
        
    def new(self, request):
        cart = Cart.objects.create(user=request.user.user_customer)
        return cart

    def add(self, product, quantity):
        item=CartItem.objects.filter(cart=self.cart, product=product).first()
        if item in self.cart.items.all():
            if item.quantity<1:
                item.quantity += quantity
            item.save()
        else:
            CartItem.objects.create(cart=self.cart, product=product, quantity=quantity)
            
        return item
    
    def remove(self, product):
        item=CartItem.objects.filter(cart=self.cart, product=product).first()
        if item in self.cart.items.all():
            item.quantity -= 1
            item.save()
            print(item.quantity, "----------------------------")
            if item.quantity == 0:
                item.delete()
        return item