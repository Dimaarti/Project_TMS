from django.contrib import admin
from china_calc.shipment.models import Shipment, Product, ShipmentItem, ShipmentExpense

admin.site.register(Shipment)
admin.site.register(Product)
admin.site.register(ShipmentItem)
admin.site.register(ShipmentExpense)


