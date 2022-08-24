from django.shortcuts import render, redirect
from django.core.mail import EmailMessage
from django.conf import settings
from django.contrib.auth.models import Group
from django.http import HttpResponse
from .forms import OrderForm, CreateUserForm
from django.forms import inlineformset_factory
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from utils.decorators import unauthenticated_user, allowed_user, admin_only
# Create your views here.

from utils.models import Product, Customer, Order
# cant call this function as login as that is a default djnago function  so if we use that that cna create conflict

#login
@unauthenticated_user
def loginPage(request):
    form = UserCreationForm()
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            
            #this code work commented for devlopement easily
            # this has to be sent only once
            # subject='Thank you for sign in  mahalaxmi matching center'
            # message=f' hello {username} checkout our catalog book an appointment, enjoy our offerings '
            # email_from=settings.EMAIL_HOST_USER
            # recipent_list=[user.email,'harshivthakkar4@gmail.com']
            # email=EmailMessage(subject,message,email_from,recipent_list)
           
            # email.attach_file('ticket.pdf')
            # email.send()
            return redirect('CustomerManage')
        else:
            messages.info(request, 'Username Or Passwrod is incorrect')

    context = {}
    return render(request, "customerMngment/login.html", context)

#logout
def logoutUser(request):
    logout(request)
    return redirect('login')

#register
@unauthenticated_user
def register(request):
    # This is a default form that django provides us with
    # the password is by default hashed !

    User_form = CreateUserForm()
    if request.method == "POST":
        # User_form=UserCreationForm(request.POST) #(default django form )
        User_form = CreateUserForm(request.POST)
        if User_form.is_valid():
            # dont forget the bracket could waste a couple of hours on that
            # while registering a user we associate it with the customer with the upcoming lines of code
            user = User_form.save()
            # Group at the end of the day is a predefined model we can use objects.get method to get a certain list of objects
            group = Group.objects.get(name="customer")
            # think of the next line as go into the user table then go into the groups table and add the group of the current user
            user.groups.add(group)

            Customer.objects.create(
                user=user,
                name=user.username,
            )
            username = User_form.cleaned_data.get('username')
            messages.success(
                request, "Account was created succesfully"+" "+username)
            return redirect('login')
    context = {'form': User_form}
    return render(request, "customerMngment/register.html", context)


@login_required(login_url='login')
@allowed_user(allowed_roles=['customer'])
def userPage(request):
    # customer is the parent of the one to many relation ship between customer and orders as  a customer can have multiple orders
    #getting all the orders of that customer.Customer is the parent here
    orders = request.user.customer.order_set.all()
    total_orders = orders.count()
    #applying filters to the orders we received for status.html
    orders_delivered = orders.filter(status="Delivered").count()
    order_pending = orders.filter(status="Pending").count()
    context = {'orders': orders,'total_orders':total_orders,'orders_delivered':orders_delivered,'order_pending':order_pending}
    return render(request, "customerMngment/user.html", context)

# login_required is a property that restricts access of a page in absence of login in
# login_url basically redirects us to  url (login page) in this case  if we try to access a page without loginng in


@login_required(login_url='login')
@admin_only
def CustomerManage(request):

    order = Order.objects.all()[0:5]
    customer = Customer.objects.all()
    context = {'customer': customer,
               'order': order}
    return render(request, "customerMngment/dashBoard.html", context)


@login_required(login_url='login')
@allowed_user(allowed_roles=['admin'])
def Products(request):
    order = Order.objects.all()
    products = Product.objects.all()
    total_orders = order.count()
    orders_delivered = Order.objects.filter(status="Delivered").count()
    order_pending = Order.objects.filter(status="Pending").count()
    context = {'products': products,
               'total_orders': total_orders,
               'orders_delivered': orders_delivered,
               'order_pending': order_pending,
               }
    return render(request, "customerMngment/products.html", context)


@login_required(login_url='login')
@allowed_user(allowed_roles=['admin'])
def customer(request, pk):
    customer = Customer.objects.get(id=pk)
    order = customer.order_set.all()
    order_count = order.count()
    context = {'order': order, 'customer': customer,
               'order_count': order_count}
    return render(request, "customerMngment/customers.html", context)
# create


@login_required(login_url='login')
@allowed_user(allowed_roles=['admin'])
def createOrder(request, pk):
    Order_FormSet = inlineformset_factory(
        Customer, Order, fields=('product', 'status'))  # parent to child
    customer = Customer.objects.get(id=pk)
    # sets the initial of the form field of that of the  customer with the id we pass so that we can plaec multiple order  without manually seleceting the customer
    formset = Order_FormSet(instance=customer)
    # form=OrderForm(initial={'customer':customer})
    if request.method == 'POST':
        # works when we wanted to enter was what we sent with post request whihc is often the case
        form = OrderForm(request.POST)
        if form.is_valid:
            form.save()
            return redirect('/Cma')
    # context={'form':form}
    context = {'formset': formset}
    return render(request, "customerMngment/order_form.html", context)

# update


@login_required(login_url='login')
@allowed_user(allowed_roles=['admin'])
def updateOrder(request, pk):
    order = Order.objects.get(id=pk)
    # get us a form that is pre filled with the instance of the cureent data
    form = OrderForm(instance=order)
    if request.method == 'POST':
        # to save the data sent as that instance
        # works when we wanted to enter was what we sent with post request whihc is often the case
        form = OrderForm(request.POST, instance=order)
        if form.is_valid:
            form.save()
            return redirect('/Cma')
    context = {'form': form}
    return render(request, "customerMngment/order_form.html", context)
# delete


@login_required(login_url='login')
@allowed_user(allowed_roles=['admin'])
@unauthenticated_user
def deleteOrder(request, pk):
    order = Order.objects.get(id=pk)
    # when we hit the submit of form its action url redirects us to this function where request.method will be post j
    if request.method == 'POST':
        order.delete()
        return redirect('/Cma')
    # first it will go to the template
    context = {'item': order}
    return render(request, "customerMngment/delete.html", context)
