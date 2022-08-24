from email import message
from django.core.paginator import Paginator
import json
from django.core.mail import send_mail
from django.conf import settings
from unicodedata import category
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from store.models import OrderItem, ProductImage, ShippingAddress
from utils.models import Product, Order, Customer
import datetime
from django.views.decorators.csrf import csrf_exempt
from store.utils import cookieData,cartData
# Create your views here.
# views.py


def home(request):
    products = Product.objects.all()[0:12]
    products1 = Product.objects.all()[12:24]
    carousel1 = products[0:4]
    carousel2 = products[4:8]
    carousel3 = products[8:12]
    carousel4 = products1[0:4]
    carousel5 = products1[4:8]
    carousel6 = products1[8:12]
    context = {'products': products, 'products1': products1, 'carousel1': carousel1,
               'carousel2': carousel2, 'carousel3': carousel3, 'carousel4': carousel4, 'carousel5': carousel5, 'carousel6': carousel6,
               }
    return render(request, "store/home.html", context)


# single product page if possible
def viewProduct(request, Id):
    product = Product.objects.get(id=Id)
    category = product.category
    # test the randomness once
    categoryProducts = Product.objects.filter(
        category=category).order_by('?')[0:4]
    featuredProducts = Product.objects.all().order_by('?')[0:4]
    productimages = product.productimage_set.all()
    context = {'product': product, 'productimages': productimages,
               'featuredProducts': featuredProducts, 'categoryProducts': categoryProducts}
    return render(request, "store/sproduct.html", context)


# shop
def store(request):
    # data1=json.load(request.body)
    # set up pagination pass in what u want to paginate and pass in the amount of the things u want to keep on the page
    p = Paginator(Product.objects.all(), 3)
    # we set up a paginator
    # nxt line means we request a page as user when we visit the url
    page = request.GET.get('page')

    pro = p.get_page(page)

    # find a way to just acccess the child of that transaction id prpoerty of the childn
    products = Product.objects.all()
    context = {'pro': pro}
    return render(request, "store/store.html", context)

# categories


def categories(request, name):
    leggings = []
    bhandni = []
    net = []
    num = []
    if name == "bhandni":
        bhandni = Product.objects.filter(category="Bhandni")
        num = [1]
    elif name == "leggings":
        leggings = Product.objects.filter(category="Leggings")
        num = [2]
    elif name == "Net":
        net = Product.objects.filter(category="Net")
        num = [3]
    context = {'bhandni': bhandni,
               'leggings': leggings, 'net': net, 'num': num}
    return render(request, "store/categories.html", context)


# checkout
def checkOut(request):
    cartContent=cartData(request)
    items=cartContent['orderItems']
    cartQuantity=cartContent['cartQuantity']
    order=cartContent['order']

    context = {'items': items, 'order': order}
    return render(request, "store/checkout.html", context)


# cart
def cart(request):
    # this doesnt work for unauthenticated user as well as users that dont have one v one relationship with customer
    # if request.user.is_authenticated:
    #     customer = request.user.customer

    #     # instead of completee we can update status
    #     order, created = Order.objects.get_or_create(
    #         customer=customer, complete=False)
    #     items = order.orderitem_set.all()
    #     if items.count()==0:
    #         flag=False
    # else:
    cartContent=cartData(request)
    items=cartContent['orderItems']
    cartQuantity=cartContent['cartQuantity']
    order=cartContent['order']
    cookieContent=cookieData(request)
    items=cookieContent['orderItems']
    cartQuantity=cookieContent['cartQuantity']
    order=cookieContent['order']
    flag=cookieContent['flag']
    print(flag)
    context = {'items': items, 'order': order,'flag':flag}
    return render(request, "store/cart.html", context)


# add to cart,remove from cart
def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    print("Action:", action)
    print("ProductId:", productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    # when we click the add item button we have to create the order if there is no order yet placed for that order we pass in the customer as our loggedin user
    # if transaction!=0:
    order, created = Order.objects.get_or_create(
        customer=customer, complete=False)
    # Now once we either fetch or create an order we place the orderitems in their coressponding orders and the product of that order item from the id we passed whilst fetch request
    orderitem, created = OrderItem.objects.get_or_create(
        order=order, product=product)
    # not working for multiple orders of a customer
    if action == "add":
        # we cant be able to add if the quantity ordered is greater than stock
        if orderitem.product.stock > orderitem.quantity:
            orderitem.quantity += 1
            orderitem.product.stock -= 1

        # probably dont require this is as our stock is eventually being calculated by the quantity
        # something unique to  the order is the transaction id can we figure a way to pass that

    elif action == "remove":
        orderitem.quantity -= 1
        orderitem.product.stock += 1

    orderitem.save()
    orderitem.product.save()

    if orderitem.quantity <= 0:
        orderitem.delete()
    print(orderitem.product.stock)
    return JsonResponse("Item was added", safe=False)

# contact us


def ContactUs(request):
    flag = False
    if request.user.is_authenticated:
        flag = True
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        messages = request.POST.get('message')
        subject = request.POST.get('subject')
        email_to = settings.EMAIL_HOST_USER
        send_mail(subject, messages, email, [email_to])
    context = {'flag': flag}
    return render(request, "store/contact.html", context)


# search
def searchProducts(request):
    flag = True
    featuredProducts = Product.objects.all().order_by('?')[0:4]
    if request.method == "POST":
        searched = request.POST.get('searched')
        products1 = Product.objects.filter(name__contains=searched)
        if products1.count() == 0:
            flag = False
        context = {'searched': searched, 'products1': products1,
                   'flag': flag, 'featuredProducts': featuredProducts}
        return render(request, "store/search.html", context)
    else:
        context = {}
        return render(request, "store/search.html", context)


# process order update shipping address
def ProcessOrder(request):
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer

        order, created = Order.objects.get_or_create(
            customer=customer, complete=False)
        # we access the form data send by us in poSt and acces its total fields
        
        address = data['shipping']['address'],
        city = data['shipping']['city'],
        state = data['shipping']['state'],
        zipcode = data['shipping']['zipcode']

        ShippingAddress.objects.create(
            customer=customer,
            order=order,
            address=address,
            city=city,
            state=state,
            zipcode=zipcode,
        )
        order_items = order.orderitem_set.all()

        print(order_items)
        subject = "Yay Order Received"
        email_from = settings.EMAIL_HOST_USER
        message = "Name:"+str(customer.name)+"\n"+"Phone:"+str(customer.phone)+"\n" + \
            f"Address:\n {address}  City: {city} \n State: {state} \n  Zipcode:{zipcode} \n "
        # convert the tuples to string
        for item in order_items:
            message += "Product \n" + \
                str(item.product)+"\n"+"Quantity\n"+str(item.quantity)

        email_to = ['harshiv49@gmail.com', 'nishiththakkar14@gmail.com']
        send_mail(subject, message, email_from, email_to)

    else:
        print("user is not logged in ")
        print("Cookies",request.COOKIES)
        name=data['form']['name']
        email=data['form']['email']
        cookieContent=cookieData(request)
        items=cookieContent['orderItems']
        # we can still kinda track a guest user
        #they will be just listed as a customer and not a user but when they create a account we can attach all their previous transactions  
        customer,created=Customer.objects.get_or_create(email=email)
        customer.name=name
        customer.save()

        order=Order.objects.create(customer=customer,complete=False)
        for item in items:
            # we can acces js elements with dots we need to use them like key value pairs
            # item.product=Product.objects.get(id=item.product.id) this is wrong
            product=Product.objects.get(id=item['product']['id'])
            quantity=item['quantity']
            OrderItem.objects.create(order=order,product=product,quantity=quantity)
    
    return JsonResponse("Item was added ", safe=False)


@csrf_exempt
def handleRequest(request):
    # paytm will send is status as post request
    pass


# find a way to make recently viewed products
