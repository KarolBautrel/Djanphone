from django import template
from base.models import OrderItem, MessageReceiver, Order

register = template.Library()

@register.filter
def cart_product_count(user):
    if user.is_authenticated:
        qs = OrderItem.objects.filter(user=user, ordered = False) 
        if qs.exists():
            quantity = sum(i.quantity for i in qs)
            if quantity == 0 :
                return ''
            else:
                return quantity
        else:
            return ''


@register.filter
def message_inbox_unreaded(user):
    if user.is_authenticated:
        qs = MessageReceiver.objects.filter(receiver = user,is_readed = False)
        if qs.exists():
            return '!'
        else:
            return ''
    else:
        return ' '