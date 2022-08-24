
from django.urls import path
from . import views


urlpatterns = [
    path('',views.CustomerManage,name="CustomerManage"),
    path('user/',views.userPage,name="user-page"),
    path('login/',views.loginPage,name="login"),
    path('logout/',views.logoutUser,name="logout"),
    path('register',views.register,name="register"),
    path('products/',views.Products,name="products"),
     path('customers/<str:pk>',views.customer,name="Customers"),
     path('create_order/<str:pk>',views.createOrder,name="createOrder"),
     path('update_order/<str:pk>',views.updateOrder,name="updateOrder"),
     path('delete_order/<str:pk>',views.deleteOrder,name="deleteOrder")
]
