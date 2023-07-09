import uuid
from django.db import models
from django.db.models import Sum, F
from django.conf import settings
from django.utils.text import gettext_lazy as _
from django.core.validators import RegexValidator
from apps.category.models import Category

# Create your models here.

class Customer(models.Model):
    id=                 models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user =              models.OneToOneField(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL, related_name="user_customer")
    name =              models.CharField(max_length=255, null=False, blank=False)
    phone =             models.PositiveBigIntegerField(null=True, blank=True)
    email =             models.EmailField()
    phone =             models.CharField(max_length=30)
    website =           models.URLField(max_length=255)
    def __str__(self):
        return self.name

class Address(models.Model):
    customer =          models.ForeignKey(Customer, on_delete=models.PROTECT, related_name="addresses")
    name =              models.CharField(max_length=255)
    postal_code =       models.CharField(
        max_length=6,
        validators=[RegexValidator('^[0-9]{6}$', _('Invalid postal code'))],
    )
    city =              models.CharField(max_length=255)

class Discount(models.Model):
    name =              models.CharField(max_length=255)
    description =       models.CharField(max_length=255)
    discount_percent =  models.DecimalField(max_digits=2, decimal_places=2)
    active =            models.BooleanField(default=False)
    created_at =        models.DateTimeField(auto_now_add=True)
    modified_at =       models.DateTimeField(auto_now=True)

def prod_img_directory(instance, filename):
    return "ecommerce/{0}/{1}/".format(instance, filename)

class Product(models.Model):
    id =            models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer =      models.ForeignKey(Customer, on_delete=models.CASCADE)
    prod_img =      models.ImageField(upload_to=prod_img_directory, null=True, blank=True)
    name =          models.CharField(max_length=255)
    description =   models.CharField(max_length=255)
    category =      models.ForeignKey(Category, on_delete=models.PROTECT)
    inventory =     models.PositiveIntegerField()
    discount =      models.ForeignKey(Discount, null=True, blank=True, on_delete=models.SET_NULL)
    unit_price =    models.DecimalField(max_digits=6, decimal_places=2, null = True)

    def __str__(self):
        return self.name

class Cart(models.Model):
    user = models.OneToOneField(Customer, null=True, related_name="customer_cart", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, null=True, blank=True, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, null=True, blank=True, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def get_total(self):
        return CartItem.objects.filter(cart=self.cart).annotate(item_total = F("product__unit_price") * F("quantity")).values("item_total")
    
class Order(models.Model):
    id =            models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer =      models.ForeignKey(Customer, on_delete=models.CASCADE)
    product =       models.ForeignKey(Product, null=True, blank=True, on_delete=models.CASCADE)
    cart =          models.ForeignKey(Cart, on_delete=models.CASCADE, null=True)
    total =         models.DecimalField(max_digits=6, decimal_places=2)
    payment_id =    models.PositiveBigIntegerField()
    created_at =    models.DateTimeField(auto_now_add=True)
    modified_at =   models.DateTimeField(auto_now=True)