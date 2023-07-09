from django.shortcuts import get_object_or_404, HttpResponseRedirect
from django.urls import reverse
from django.http import HttpResponseRedirect
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from apps.category.models import Category
from apps.blog.pagination import (
    SmallSetPagination,
    MediumSetPagination,
    LargeSetPagination,
)
from . import permissions as custom_permissions
from .serializers import (
    ProductSerializer,
    OrderSerializer,
    CartSerializer,
    ItemSerializer,
    CustomerSerializer,
)
from .cart import CartObject
from rest_framework import permissions
from .models import (
    Product,
    Order,
    CartItem,
    Customer,
    Cart,
)
from rest_framework.generics import RetrieveUpdateAPIView

# Create your views here.

class CustomerView(APIView):
    def get(self, request, *args, **kwargs):
        pk=request.query_params.get("id")
        query=Customer.objects.get(pk=pk)
        serializer=CustomerSerializer(query)
        return Response(data={"message":serializer.data}, status=status.HTTP_200_OK)
    
class ProductsListView(APIView):
    permission_classes=(permissions.AllowAny,)
    def get(self, request):
        if Product.objects.all().exists():
            initial_products = Product.objects.order_by("name").all()
            paginator = SmallSetPagination()
            results = paginator.paginate_queryset(initial_products, request)
            serializer = ProductSerializer(results, many=True, context={"request":request})
            return paginator.get_paginated_response({"products":serializer.data})
        else:
            return Response({"Error":"No content"}, status=status.HTTP_204_NO_CONTENT)

    def post(self, request):
        product = request.data
        serializer = ProductSerializer(data=product, context={"request":request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({"product":serializer.data}, status=status.HTTP_201_CREATED)
        else:
            return Response({"Error":"Couldn\'t be created"}, status=status.HTTP_400_BAD_REQUEST)

class ProductDetailView(RetrieveUpdateAPIView):
    permission_classes=(permissions.AllowAny,)
    serializer_class=ProductSerializer

    def get_object(self):
        object = Product.objects.get(pk=self.kwargs["pk"])
        return object

    def get(self, request, format=None, *args, **kwargs):
        product = self.get_object()
        serializer = ProductSerializer(product, context={"request":request})
        return Response({"product":serializer.data}, status=status.HTTP_200_OK)
    
    def patch(self, request, format=None, *args, **kwargs):
        product = self.get_object()
        serializer = ProductSerializer(product, data=request.data, partial=True, context={"request":request})
        if serializer.is_valid():
            serializer.save()
            return Response({"product":serializer.data}, status=status.HTTP_200_OK)

        else:
            return Response({"error":"error"}, status=status.HTTP_400_BAD_REQUEST)

    # def delete(self, request, format=None, *args, **kwargs):
    #     product=self.get_object()
    #     product.delete()
    #     return Response({"Success":"its been deleted"}, status= status.HTTP_204_NO_CONTENT)



# class ProductDetailView(RetrieveUpdateDestroyAPIView):
#     serializer_class=ProductSerializer
#     permission_classes=(custom_permissions.IsAuthorOrReadOnly,)
#     queryset=Product.objects.all()

class ProductListByCategory(APIView):
    permission_classes=(permissions.IsAuthenticated,)
    def get(self, request, format=None):
        if Product.objects.all().exists():
            slug=self.request.query_params.get("slug")
            category=Category.objects.get(slug=slug)
            products=Product.objects.order_by("name").all()
            if Category.objects.filter(parent=category).exists():
                sub_categories = Category.objects.select_related("parent").filter(parent=category)
                filtered_categories = [category]
                for sub_category in sub_categories:
                    filtered_categories.append(sub_category)

                filtered_categories = tuple(filtered_categories)
                products=products.filter(category__in=filtered_categories)
            else:
                products = products.filter(category=category)
            
        paginator = MediumSetPagination()
        results = paginator.paginate_queryset(products, request)
        serializer=ProductSerializer(results, many=True)

        return paginator.get_paginated_response({"products":serializer.data})

class OrdersView(APIView):
    permission_classes=(custom_permissions.IsAuthorOrReadOnly,)
    def get(self, request, format=None, *args, **kwargs):
        if Order.objects.filter(customer=request.user.user_customer).exists():
                orders=Order.objects.select_related("customer").filter(customer=request.user.user_customer)
                paginator=MediumSetPagination()
                results=paginator.paginate_queryset(orders, request)
                serializer=OrderSerializer(results, many=True)
                return paginator.get_paginated_response({"orders":serializer.data})
        else:
            return Response({"No content", "No orders"}, status=status.HTTP_204_NO_CONTENT)
    def post(self, request, format=None):
        serializer=OrderSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({"Order":serializer.data}, status=status.HTTP_201_CREATED)
        else:
            return Response({"Error":"Could not be created"}, status=status.HTTP_400_BAD_REQUEST)

class CartView(APIView):
    permission_classes=(permissions.AllowAny,)
    cart = CartObject
    def get(self, request, format=None):
        cart=self.cart(request)
        serializer = CartSerializer(cart.cart, context={"request":request})
        return Response({"cart" : serializer.data}, status=status.HTTP_200_OK)

class ItemView(APIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = ItemSerializer
    cart = CartObject
    
    def get(self, request, *args, **kwargs):
        cart = self.cart(request=request)
        product = Product.objects.get(pk=self.kwargs["pk"])
        item = cart.add(product=product, quantity=+1)    
        serializer = ItemSerializer(item, context={"request":request})
        return Response(data={"item":serializer.data}, status=status.HTTP_200_OK)

    # def patch(self, request, *args, **kwargs):
    #     cart = self.cart(request=request)
    #     product = Product.objects.get(pk=self.kwargs["pk"])
    #     item = cart.add(product=product)
    #     serializer = ItemSerializer(item, context={"request":request})
    #     return Response({"item" : serializer.data}, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        cart = self.cart(request=request)
        product = Product.objects.get(pk=self.kwargs["pk"])
        item=cart.remove(product=product)
        serializer=ItemSerializer(item, context={"request":request})
        return Response(data={"data":serializer.data})
