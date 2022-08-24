
from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
    path('',views.home,name="home"),
    path('shop/',views.store,name="store"),
    path('shop/<str:Id>',views.viewProduct,name="singleProduct"),
    path('categories/<str:name>',views.categories,name="categories"),
    path('cart/',views.cart,name="cart"),
    path('ContactUs/',views.ContactUs,name="ContactUs"),
    path('checkout/',views.checkOut,name="checkOut"),
    path('update_item/',views.updateItem,name="update_item"),
    path('search_products/',views.searchProducts,name="search-products"),
    path('process_order/',views.ProcessOrder,name="process_order")
]
urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)