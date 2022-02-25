from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [

    
    path('products', views.ProductList.as_view()),
    path('products/<slug:slug>', views.ProductDetail.as_view()),
    path('stores', views.StoreList.as_view()),
    path('stores/<int:pk>', views.StoreDetail.as_view()),

]

urlpatterns = format_suffix_patterns(urlpatterns)