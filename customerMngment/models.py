from django.db import models
from sqlalchemy import null

# Create your models here.

# class Customer(models.Model):
#     name=models.CharField(max_length=200,null=True)
#     email=models.CharField(max_length=200,null=True)
#     phone=models.CharField(max_length=200,null=True)
#     date_ordered=models.DateTimeField(auto_now_add=True,null=True)
#     def __str__(self):
#         return self.name

class Tag(models.Model):
    name=models.CharField( max_length=200,null=True)

    def __str__(self):
        return self.name

# class Product(models.Model):
#     name=models.CharField(max_length=200,null=True)
#     price=models.CharField(max_length=200,null=True)
#     category=models.CharField(max_length=200,null=True)
#     description=models.CharField(max_length=200,null=True)
#     date_ordered=models.DateTimeField(auto_now_add=True,null=True)
#     tag=models.ManyToManyField(Tag)
    
#     def __str__(self):
#         return self.name


# class Order(models.Model):
#     STATUS=(('Pending','Pending'),
#     ('Out for Delivery','Out for Delivery'),
#     ('Delivered','Delivered'))
#     customer=models.ForeignKey(Customer,null=True,on_delete=models.SET_NULL)
#     product=models.ForeignKey(Product,null=True,on_delete=models.SET_NULL)
#     date_ordered=models.DateTimeField(auto_now_add=True,null=True)
#     status=models.CharField(max_length=200,null=True,choices=STATUS)

   
  

