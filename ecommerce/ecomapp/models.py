from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Product(models.Model):
    CAT=((1,'Mobile'),(2,'shoes'),(3,'cloth')) #category changes from 1,2,3 to value
    name=models.CharField(max_length=20,verbose_name="Product Name")
    product_detail=models.CharField(max_length=100)
    category=models.IntegerField(choices=CAT)
    price=models.IntegerField()
    is_active=models.BooleanField(default=True)
    product_image=models.ImageField(upload_to='image') # VideoField(upload_to='video')

    def __str__(self):
        return self.name

class newProduct(models.Model):
    name=models.CharField(max_length=20,verbose_name="Product Name")

class Cart(models.Model):
    uid=models.ForeignKey('auth.User',on_delete=models.CASCADE,db_column='uid')
    pid=models.ForeignKey('Product',on_delete=models.CASCADE,db_column='pid')
    qty=models.IntegerField(default=1)
    address=models.CharField(max_length=40)

class Order(models.Model):
    uid=models.ForeignKey('auth.User',on_delete=models.CASCADE,db_column='uid')
    pid=models.ForeignKey('Product',on_delete=models.CASCADE,db_column='pid')
    qty=models.IntegerField(default=1)
    amt=models.IntegerField()
    address=models.CharField(max_length=40)