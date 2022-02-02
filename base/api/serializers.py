from rest_framework import serializers
from base.models import Product, Shipment, Store, Brand

class BrandSerializer(serializers.Serializer):
    class Meta:
        model = Brand
        fields = '__all__'



class ProductSerializer (serializers.ModelSerializer):
    brand_name = serializers.StringRelatedField(source='brand.brand')
    class Meta:
        model = Product
        fields = ['model','brand_name','price','description'] 

class ShipmentSerializer (serializers.ModelSerializer):

    ship_to_name = serializers.StringRelatedField(source='ship_to.name')
    product_name = serializers.StringRelatedField(source='product.name')
    class Meta:
        model = Shipment 
        fields = ['product_name','status','ship_to_name']


class StoreSerializer (serializers.ModelSerializer):
    class Meta:
        model = Store 
        fields = ['address','owner','contact']