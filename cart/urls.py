from django.urls import path
from .views import *

urlpatterns = [
    path('', cart_view, name='cart_view'),
    path('add/<int:product_id>/', add_to_cart_view, name='add_to_cart_view'),
    path('delete/<int:cart_product_id>/', delete_product_from_cart, name='delete_product_from_cart'),
    path('checkout/<int:cart_product_id>/', checkout, name='checkout'),
    path('delivery-address/add/', add_delivery_address, name='add_delivery_address'),
    path('update-cart/<int:cart_product_id>/', update_cart_quantity, name='update_cart_quantity'),
    path('place-order/', place_order, name='place_order'),
    path('get-districts/', get_districts, name='get_districts'),
    path('get-municipalities/', get_municipalities, name='get_municipalities'),
    path('add-delivery-address/', add_delivery_address, name='add_delivery_address'),
   
    
]