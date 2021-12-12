from django.contrib import admin

# Register your models here.

from .models import *

# tables name from models.py
admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)
admin.site.register(Comment)