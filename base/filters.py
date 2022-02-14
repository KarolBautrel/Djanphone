import django_filters 
from base.models import Product
from django_filters import DateFilter, DateFromToRangeFilter, RangeFilter, CharFilter

class ProductFilter(django_filters.FilterSet):
    model = CharFilter(field_name = 'title', lookup_expr='icontains' )
    price__gt = django_filters.NumberFilter(field_name='price', lookup_expr='gt')
    price__lt = django_filters.NumberFilter(field_name='price', lookup_expr='lt')
    class Meta:
        model = Product
        fields = ('brand','model')