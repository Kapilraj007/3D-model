from django.db import models
from authentication.models import SellerProfile
from uuid import uuid4

from authentication.models import CustomUser

class Category(models.Model):
    title = models.CharField(max_length=255)
    
    def __str__(self):
        return self.title
    
class Product(models.Model):
    name = models.CharField(max_length=255)
    category  = models.ForeignKey(Category,on_delete=models.CASCADE,related_name='products')
    description = models.TextField()
    stock = models.PositiveIntegerField()
    amount = models.DecimalField(max_digits=6, decimal_places=2)
    brand = models.CharField(max_length=255)
    is_favourate = models.BooleanField(default=False)
    image = models.ImageField(upload_to="store/images")
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    last_update = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
    
    
class Order(models.Model):
    PAYMENT_STATUS_PENDING = 'P'
    PAYMENT_STATUS_COMPLETE = 'C'
    PAYMENT_STATUS_FAILED = 'F'
    PAYMENT_STATUS_CHOICES = [
        (PAYMENT_STATUS_PENDING, 'Pending'),
        (PAYMENT_STATUS_COMPLETE, 'Complete'),
        (PAYMENT_STATUS_FAILED, 'Failed')
    ]

    placed_at = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(
        max_length=1, choices=PAYMENT_STATUS_CHOICES, default=PAYMENT_STATUS_PENDING)
    user = models.ForeignKey(CustomUser, on_delete=models.PROTECT)    
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order,on_delete = models.PROTECT,related_name='items')
    product = models.ForeignKey(Product, on_delete = models.PROTECT,related_name='orderitems')
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=6,decimal_places=2)
    
    def __str__(self):
       return f'{self.quantity}-> {self.unitprice}'
    
    
class Cart(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4)
    created_at = models.DateTimeField(auto_now_add=True)
    
class CartItem(models.Model):
    cart = models.ForeignKey(Cart,on_delete=models.CASCADE ,related_name='items')
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField()
    
class Review(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE,related_name='reviews')
    comment = models.TextField()
    created_at= models.DateTimeField(auto_now_add=True)
    name = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    
    