from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from  django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    
    #account
    path('account/', include('account.urls')),
    
    # #shop
    path('', include('shop.urls')),
    
    # #cart
    path('cart/', include('cart.urls')),
    
    # #customer
    # path('customer/', include('customer.urls')),
    
    # #vendor
    path('vendor/', include('vendor.urls')),
] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
