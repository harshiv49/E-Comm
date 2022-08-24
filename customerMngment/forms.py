#apparently in django we can create forms as classes 
from django.forms import ModelForm
from utils.models import Order
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
# we can create our form as a class .as a  convention which we can use is writing the  name of model with form 
class OrderForm(ModelForm):
    class Meta:
        model=Order
        fields="__all__"

class CreateUserForm(UserCreationForm):
    class Meta:
    #we have to specify the model of which we are creating the form 
        model=User
        #The fields are of default django we can look it up from documentation 
        #fields(of the form) can be specified as a list in python  
        fields=['username','email','password1','password2']

