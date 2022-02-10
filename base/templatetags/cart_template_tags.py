from django import template
from base.models import Order

register = template.Library()

@register.filter
def cart_product_count(user):
    if user.is_authenticated:
        qs = Order.objects.filter(user=user, ordered = False)
        if qs.exists():
            return qs[0].product.count()
    else:
        return 0