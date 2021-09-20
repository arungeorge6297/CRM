from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth.models import  User

# Create your models here.

class Customer(models.Model):
    user = models.OneToOneField(User,blank=True, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=100,null=True)
    phone = models.CharField(max_length=200,null=True)
    Email = models.EmailField(max_length=200, null=True)
    profile_pic = models.ImageField(default='Profile.png',null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return  self.name


class Product(models.Model):
    name = models.CharField(max_length=200, null=True)
    price = models.FloatField(null=True)
    description = models.CharField(max_length=200, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return  self.name

class Order(models.Model):

    STATUS = (
        ('Pending','Pending'),
        ('Outfordelivery','Outfordelivery'),
        ('Delivered','Delivered'),
    )

    customer = models.ForeignKey(Customer, null=True, on_delete=models.SET_NULL)
    product = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    status = models.CharField(max_length=100,null=True,choices=STATUS)

    def __str__(self):
        return  self.product.name
