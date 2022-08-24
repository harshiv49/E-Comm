#an order can have only one customer but a same customer could have multiple orders
from sre_parse import CATEGORIES
from unicodedata import name
from django.db import models
from utils.models import Customer,Order,Product
from django.contrib.auth.models import User 
from sqlalchemy import false, true
# Create your models here.


# class Product(models.Model):
#     CATEGORIES=(('Leggings','Leggings'),
#     ('Bhandni','Bhandni'),
#     ('Net','Net'))
#     name=models.CharField(max_length=200,null=True,blank=True)
#     price=models.FloatField()
#     image=models.ImageField(null=True,blank=True)
#     category=models.CharField(max_length=200,null=True,blank=True,choices=CATEGORIES)
#     description=models.CharField(max_length=200,null=True,blank=True)
#     stock=models.IntegerField(null=True,blank=True)
    
#     @property
#     def imageUrl(self):
#         try:
#             url=self.image.url
#         except:
#             url=''
#         return url        
#     def __str__(self):
#         return self.name

# class Order(models.Model):
#     customer=models.ForeignKey(Customer,on_delete=models.SET_NULL,null=True,blank=True)
#     date_ordered=models.DateTimeField(auto_now_add=True)
#     complete=models.BooleanField(default=False,null=True,blank=False)
#     transaction_id=models.CharField(max_length=200,null=True,blank=True)
#     @property
#     def get_cart_total(self):
#         order_items=self.orderitem_set.all()
#         total=sum([item.get_total for item in order_items])
#         return total
#     @property
#     def get_cart_quantity(self):
#         order_items=self.orderitem_set.all()
#         total=sum([item.quantity for item in order_items])
#         return total  
#     @property
#     def get_stock_total(self):
#         order_items=self.orderitem_set.all()
#         total=sum([item.get_stock for item in order_items])
#         return total 

class OrderItem(models.Model):
    STATUS=(('Pending','Pending'),
    ('Out for Delivery','Out for Delivery'),
    ('Delivered','Delivered'))
    product=models.ForeignKey(Product,on_delete=models.CASCADE,null=True,blank=True)
    #order is the parent to orderItem as one order can have multiple order items 
    order=models.ForeignKey(Order,on_delete=models.SET_NULL,null=True,blank=True)
    quantity=models.IntegerField(default=0,null=True,blank=True)
    status=models.CharField(max_length=200,null=True,choices=STATUS)
    date_ordered=models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        total=self.product.price*self.quantity
        return total
    # @property
    # as we dealt with it in backend we dont need this decorator anymore 
    # def get_stock(self):
    #     total=self.product.stock-self.quantity
    #     return total

class ProductImage(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE,null=True,blank=True)
    image=models.ImageField(null=True,blank=True)

    @property
    def imageUrl(self):
        try:
            url=self.image.url
        except:
            url=''
        return url  
    def __str__(self):
        return self.product.name

class ShippingAddress(models.Model):
    customer=models.ForeignKey(Customer,on_delete=models.SET_NULL,null=True,blank="True")
    order=models.ForeignKey(Order,on_delete=models.SET_NULL,null=True,blank="True")
    address=models.CharField(max_length=500,null=True,blank=True)
    city=models.CharField(max_length=250,null=True,blank=True)
    state=models.CharField(max_length=250,null=True,blank=True)
    zipcode=models.CharField(max_length=250,null=True,blank=True)
    date_added=models.DateField(auto_now_add=True)
    def __str__(self):
        return (self.address)