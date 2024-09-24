from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
from django.db import models



class CustomUser(AbstractUser):
    phone_number = PhoneNumberField(blank=True,unique=True)
    email =  models.EmailField(unique=True)
    is_seller = models.BooleanField(default=False)
    
    

#addres model

class Address(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,related_name='address')
    house_number_street_area = models.CharField(max_length=100)
    locality_town = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)
    

#seller profile model
class SellerProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='seller_profile')
    brand_name = models.CharField(max_length=100,null=True)
    profile_image = models.ImageField(upload_to='seller_profile_images/', blank=True, null=True)
    permit_image = models.ImageField(upload_to='seller_permit_images/', blank=True, null=True)
    license_image = models.ImageField(upload_to='seller_license_images/', blank=True, null=True)
    
