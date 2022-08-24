from datetime import datetime
from django.db import models

# Create your models here.
class Blog(models.Model):
    title=models.CharField(max_length=200,null=True,blank=True)
    body=models.TextField(null=True,blank=True)
    date_of_writing=models.DateField(auto_now_add=True)
    image=models.ImageField(null=True,blank=True)

    @property
    def imageUrl(self):
        try:
            url=self.image.url
        except:
            url=''
        return url  
    @property
    def snippet(self):
        return self.body[0:200]

    def __str__(self):
        return self.title

    
