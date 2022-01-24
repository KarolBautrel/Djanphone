
from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('products/', views.products, name='products'),
    path('accounts/', include('allauth.urls')),
    path('profile/<str:pk>', views.userProfile, name = 'profile'),
    path('update_profile', views.updateProfile, name = 'update-user'),
    path('user_panel', views.userPanel, name = 'user-panel'),
    path('change_email', views.changeEmail, name = 'change-email'),
    path('change-password', views.changePassword, name = 'change-password'),
    path('product_info/<str:pk>', views.productInfo, name = 'product-info'),
    path('createProduct', views.addProduct, name = 'create-product'),
    path('create_product_confirmation', views.addProductConfirmation, name='confirm-product-creation'),
    path('delete_comment/<str:pk>', views.deleteComment, name = 'delete-comment'),
    path('add_comment/<str:pk>', views.addComment, name='add-comment' ),
    path('buy_product/<str:pk>', views.buyProduct, name = 'buy-product'),
    path('shipments/<str:pk>', views.shipmentsPanel, name = 'shipments'),

]
