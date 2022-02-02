from rest_framework import viewsets
from base.models import Product, Shipment, Store, User
from .serializers import ProductSerializer, ShipmentSerializer, StoreSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ShipmentViewSet(viewsets.ModelViewSet):
    queryset = Shipment.objects.all()
    serializer_class = ShipmentSerializer


class StoreViewSet(viewsets.ModelViewSet):
    queryset = Store.objects.all()
    serializer_class = StoreSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = StoreSerializer


@api_view(['GET']) # to oznacza, ze ten view moze tylko miec GET request
def getRoutes(request):
    routes = [
        'GET /api', 
        'GET /api/products', 
        'GET /api/products/:id', 
        'GET /api/shipments',
        'GET /api/shipments/:id',
        'GET /api/stores',
        'GET /api/stores/:id',
    ]
    return Response(routes) 


@api_view(['GET'])
def getProducts(request):
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True) 
    return Response(serializer.data) 


@api_view(['GET'])
def getProduct(request,pk):
    product = Product.objects.get(id=pk)
    serializer = ProductSerializer(product, many=False) 
    return Response(serializer.data) 


@api_view(['GET'])
def getShipments(request):
    shipments = Shipment.objects.all()
    serializer = ShipmentSerializer(shipments, many=True) 
    return Response(serializer.data) 


@api_view(['GET'])
def getShipment(request,pk):
    shipment = Shipment.objects.get(id=pk)
    serializer = ShipmentSerializer(shipment, many=True) 
    return Response(serializer.data) 


@api_view(['GET'])
def getStores(request):
    stores = Store.objects.all()
    serializer = StoreSerializer(stores, many=True) 
    return Response(serializer.data) 


@api_view(['GET'])
def getStore(request,pk):
    store = Store.objects.get(id=pk)
    serializer = StoreSerializer(store, many=False) 
    return Response(serializer.data) 