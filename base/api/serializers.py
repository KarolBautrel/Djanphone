from rest_framework import serializers
from base.models import Product, Store, Brand

class BrandSerializer(serializers.Serializer):
    class Meta:
        model = Brand
        fields = '__all__'



class ProductSerializer (serializers.ModelSerializer):
    brand_name = serializers.StringRelatedField(source='brand.brand')
    class Meta:
        model = Product
        fields = ['model','brand_name','price','description'] 



class StoreSerializer (serializers.ModelSerializer):
    class Meta:
        model = Store 
        fields = ['address','owner','contact']