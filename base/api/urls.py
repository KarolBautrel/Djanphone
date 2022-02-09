from django.urls import include, path
from rest_framework import routers
from base.api import views




urlpatterns = [
    path('', views.getRoutes),
    path('products/', views.getProducts),
    path('products/<str:pk>', views.getProduct),

    path('stores/', views.getStores),
    path('stores/<str:pk>', views.getStore),]