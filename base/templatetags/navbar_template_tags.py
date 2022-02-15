from django import template
from base.models import Order, MessageReceiver

register = template.Library()

@register.filter
def cart_product_count(user):
    if user.is_authenticated:
        qs = Order.objects.filter(user=user, ordered = False)
        if qs.exists():
            return qs[0].product.count()
        else:
            return ''
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