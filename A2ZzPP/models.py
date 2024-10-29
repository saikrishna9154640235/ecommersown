from django.db import models
from django.contrib.auth.models import User

class Product(models.Model):
    name=models.CharField(max_length=100)
    image=models.ImageField(null=True,blank=True) 
    price=models.IntegerField(default=10)
    descriptions=models.TextField(max_length=500)
    
    def __str__(self):
        return self.name
   
        
    
class Cart(models.Model):
    is_paid=models.BooleanField(default=False,blank=True)
    user=models.ForeignKey(User,null=True,on_delete=models.CASCADE,related_name='cart')


# Create your models here.
class Cart_item(models.Model):
    cart=models.ForeignKey(Cart,on_delete=models.CASCADE,related_name='cart_items')
    product=models.ForeignKey(Product,on_delete=models.CASCADE,related_name='cart_items',null=True,blank=True)    
    
    