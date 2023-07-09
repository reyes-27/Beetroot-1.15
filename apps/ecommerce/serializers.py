from rest_framework import serializers
from apps.category.serializers import CategorySerializer
from .models import (
    Product,
    Order,
    Cart,
    CartItem,
    Customer,
)
from rest_framework.request import Request
from django.http import HttpRequest

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model=Customer
        fields="__all__"

class ProductSerializer(serializers.HyperlinkedModelSerializer):

    # def create(self, validated_data):
    #     return Product.objects.create(**validated_data)

    # def update(self, instance, validated_data):
    #     # instance.prod_img = validated_data.get("prod_img", instance.prod_img)
    #     # instance.name = validated_data.get("name", instance.name)
    #     # instance.description = validated_data.get("description", instance.description)
    #     # instance.category = validated_data.get("category", instance.category)
    #     # instance.inventory = validated_data.get("inventory", instance.inventory)
    #     # instance.discount = validated_data.get("discount", instance.discount)
    #     for field, value in validated_data.items():
    #             setattr(instance, field, value)
            
    #     instance.save()
    #     return instance

    url=serializers.HyperlinkedIdentityField(
        view_name='product_detail',
        lookup_field="id",
        lookup_url_kwarg="pk",
        )
    
    customer=serializers.HyperlinkedRelatedField(
        view_name='customer_detail',
        lookup_field="id",
        lookup_url_kwarg="pk",
        read_only=True,
        )
    category=CategorySerializer()
    
    class Meta:
        model = Product
        fields =[
            "url",
            "id",
            "customer",
            "prod_img",
            "name",
            "description",
            "category",
            "inventory",
            "discount",
            "unit_price",
            ]

    
class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model=Order

        fields=[
            "customer",
            "product",
            "total",
            "payment_id",
            "created_at",
            "modified_at",
        ]

class ItemSerializer(serializers.ModelSerializer):    
    def get_item_total(self, obj):
        return obj.get_total()
    
    item_total = serializers.SerializerMethodField()

    product = ProductSerializer()
    class Meta:
        model = CartItem
        fields=(
            "id",
            "cart",
            "product",
            "quantity",
            "item_total",
        )

class CartSerializer(serializers.ModelSerializer):
    items = ItemSerializer(many=True)
    class Meta:
        model = Cart
        fields=(
            "id",
            "user",
            "created_at",
            "items",
        )