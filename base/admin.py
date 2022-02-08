from django.contrib import admin
from .models import Product, User, Comment, Shipment, Ticket, Store, Brand, Cart

# Register your models here.
admin.site.register(User)
admin.site.register(Product)
admin.site.register(Comment)
admin.site.register(Shipment)
admin.site.register(Ticket)
admin.site.register(Store)
admin.site.register(Brand)
admin.site.register(Cart)