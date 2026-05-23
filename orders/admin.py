from django.contrib import admin
from .models import Order, OrderItem, ShipmentTracking

admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ShipmentTracking)