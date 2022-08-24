from django.db import models
from django.contrib.auth.models import User
from customerMngment.models import Tag 
import datetime
# Create your models here.
class Customer(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,null=True,blank=True)
    name=models.CharField(max_length=200,null=True,blank=True)
    email=models.CharField(max_length=200,null=True,blank=True)
    phone=models.CharField(max_length=200,null=True,blank=True)
    date_ordered=models.DateTimeField(auto_now_add=True,null=True)
    def __str__(self):
        return self.name


class Product(models.Model):
    CATEGORIES=(('Leggings','Leggings'),
    ('Bhandni','Bhandni'),
    ('Net','Net'),('Ajrak','Ajrak'),('Plaso','Plaso'))
    name=models.CharField(max_length=200,null=True,blank=True)
    price=models.DecimalField(max_digits=9,decimal_places=2)
    image=models.ImageField(null=True,blank=True)
    category=models.CharField(max_length=200,null=True,blank=True,choices=CATEGORIES)
    description=models.CharField(max_length=200,null=True,blank=True)
    stock=models.IntegerField(default=0,null=True,blank=True)
    tag=models.ManyToManyField(Tag)
    def __str__(self):
        return self.name
    @property
    def imageUrl(self):
        try:
            url=self.image.url
        except:
            url=''
        return url        
    

class Order(models.Model):
    STATUS=(('Pending','Pending'),
    ('Out for Delivery','Out for Delivery'),
    ('Delivered','Delivered'))
    customer=models.ForeignKey(Customer,on_delete=models.SET_NULL,null=True,blank=True)
    date_ordered=models.DateTimeField(auto_now_add=True)
    complete=models.BooleanField(default=False,null=True,blank=False)
    product=models.ForeignKey(Product,null=True,on_delete=models.SET_NULL)
    status=models.CharField(max_length=200,null=True,choices=STATUS)
    transaction_id=models.CharField(max_length=200,default=datetime.datetime.now().timestamp(),editable=False,null=True,blank=True)
    @property
    def get_cart_total(self):
        order_items=self.orderitem_set.all()
        total=sum([item.get_total for item in order_items])
        return total
    @property
    def get_cart_quantity(self):
        order_items=self.orderitem_set.all()
        total=sum([item.quantity for item in order_items])
        return total  
    @property
    def get_stock_total(self):
        order_items=self.orderitem_set.all()
        total=sum([item.get_stock for item in order_items])
        return total

    def __str__(self):
        return self.customer.name



    
    
    
