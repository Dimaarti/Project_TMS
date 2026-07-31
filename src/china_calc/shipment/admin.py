from django.contrib import admin

from china_calc.shipment.models import Product, Shipment, ShipmentExpense, ShipmentItem

admin.site.register(Shipment)
admin.site.register(Product)
admin.site.register(ShipmentItem)
admin.site.register(ShipmentExpense)
