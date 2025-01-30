from django.urls import path
from . views import *

urlpatterns = [
    path('', shop_view, name='shop_view'),
    
    #get products for specific category and brand
    path('category/<int:category_id>/<int:brand_id>/products/', category_brand_view, name='category_brand_view'),
    path('category/<int:brand_id>/products/', brand_view, name='brand_view'),
    
    path('products/<int:product_id>/detail/', product_detail_view, name='product_detail_view'),

]
