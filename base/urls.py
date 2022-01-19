
from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('products/', views.products, name='products'),
    path('accounts/', include('allauth.urls')),
    path('logout/', views.logout, name='logout')
]
