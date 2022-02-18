from django.contrib import admin
from .models import (Product, 
                    User, 
                    Comment, 
                    Order, 
                    Ticket, 
                    Store, 
                    OrderItem, 
                    BillingAddress, 
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
admin.site.register(BillingAddress)
admin.site.register(Message)
admin.site.register(MessageReceiver)
admin.site.register(Coupon)

