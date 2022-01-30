from django.contrib import admin
from .models import Product, User, Comment, Shipment, Ticket, Store, Delivery, Brand

# Register your models here.
admin.site.register(User)
admin.site.register(Product)
admin.site.register(Comment)
admin.site.register(Shipment)
admin.site.register(Ticket)
admin.site.register(Store)
admin.site.register(Delivery)
admin.site.register(Brand)
