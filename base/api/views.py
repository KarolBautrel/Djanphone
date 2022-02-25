from base.models import Product, Store
from .serializers import ProductSerializer, StoreSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import Http404

class ProductList(APIView):
    '''
    Get all products
    '''
    def get(self, request, format = None):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

class ProductDetail(APIView):
    '''
    Get product detail
    '''
    def get_object(self, slug):
        try:
            return Product.objects.get(slug=slug)
        except Product.DoesNotExist:
            raise Http404

    def get(self, request, slug, format=None):
        product = self.get_object(slug)
        serializer = ProductSerializer(product, many=False)
        return Response(serializer.data)

class StoreList(APIView):
    '''
    Get all local stores
    '''

    def get(self,request, format=None):
        stores = Store.objects.all()
        serializer = StoreSerializer(stores, many=True)
        return Response(serializer.data)

class StoreDetail(APIView):
    '''
    Get store detail
    '''
    def get_object(self,pk):
        try:
            return Store.objects.get(pk=pk)
        except Store.DoesNotExist:
            return Http404
    
    def get(self,request,pk, format=None):
        store = self.get_object(pk)
        serializer = StoreSerializer(store, many=False)
        return Response(serializer.data)