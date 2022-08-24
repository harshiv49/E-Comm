import json
from utils.models import *
from django.shortcuts import render, redirect
#we make seperate functions for cart to reduce code redundancy of views
def cookieData(request):
    try:
        cart = json.loads(request.COOKIES['cart'])
    except:
        cart = {}
    print(cart)
    flag=True
    
    items = []
    order = {'get_cart_total': 0, 'get_cart_quantity': 0}
    cartQuantity = order['get_cart_quantity']
    for i in cart:
        try:
            # total quantity of car
            cartQuantity += cart[i]['quantity']
            product = Product.objects.get(id=i)
            total = (product.price * cart[i]['quantity'])
            order['get_cart_total'] += total
            order['get_cart_quantity'] += cart[i]['quantity']
            item = {
                'product': {
                    'id': product.id,
                    'name': product.name,
                    'price': product.price,
                    'imageUrl': product.imageUrl,
                },
                'quantity': cart[i]['quantity'],
                'get_total': total,
            }
            items.append(item)
        except:
            pass
    if items == []:
        flag=False
    print(flag)
    #we pass the quantity,we pass the total price,we pass the order items  
    return {'cartQuantity':cartQuantity ,'order':order,'orderItems':items,'flag':flag}
    # return render(request, "store/cart.html", context) we can do this but then it wont work as a dynamic funtion which wer can call for various purposes


def cartData(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        # two variable  seperated by a comma in python mean they become a tuple
        # the function get_or_create() Returns a tuple of (object, created), where object is the retrieved or created object and created is a boolean specifying whether a new object was created.
        order, created = Order.objects.get_or_create(
            customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        cookieContent=cookieData(request)
        items=cookieContent['orderItems']
        cartQuantity=cookieContent['cartQuantity']
        order=cookieContent['order']
    return {'cartQuantity':cartQuantity ,'order':order,'orderItems':items}