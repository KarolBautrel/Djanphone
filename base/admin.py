from django.contrib import admin
from .models import (Product, 
                    User, 
                    Comment, 
                    Order, 
                    Ticket, 
                    Store, 
                    OrderItem, 
                    Address,  
                    Message,
                    MessageReceiver,
                    Coupon
                    )

# Register your models here.
admin.site.register(User)
admin.site.register(Product)
admin.site.register(Comment)
admin.site.register(Order)
admin.site.register(Ticket)
admin.site.register(Store)
admin.site.register(OrderItem)
admin.site.register(Address)
admin.site.register(Message)
admin.site.register(MessageReceiver)
admin.site.register(Coupon)

