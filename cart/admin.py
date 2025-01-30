from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Cart)
admin.site.register(CartProduct)
admin.site.register(State)
admin.site.register(District)
admin.site.register(Municipality)
admin.site.register(DeliveryAddress)
admin.site.register(Order)