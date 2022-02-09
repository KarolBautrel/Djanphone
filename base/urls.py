from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from . import views
from base.views import (
                UpdateUserView, 
                ProductList,
                ProductDetail, 
                UserDetailView,
                ProductCreateView)


urlpatterns = [
    path('', views.home, name='home'),
    path('products/', ProductList.as_view(), name='products'),
    path('accounts/', include('allauth.urls')),
    path('<str:pk>/profile/', UserDetailView.as_view(), name = 'profile'),
    path('update_profile', UpdateUserView.as_view(), name='update-user'),
    path('user_panel', views.userPanel, name = 'user-panel'),
    path('change_email', views.changeEmail, name = 'change-email'),
    path('change-password', views.changePassword, name = 'change-password'),
    path('product_detail/<str:pk>', ProductDetail.as_view(), name = 'product-detail'),
    path('createProduct', ProductCreateView.as_view(), name = 'create-product'),
    path('delete_comment/<str:pk>', views.deleteComment, name = 'delete-comment'),
    path('add_comment/<str:pk>', views.addComment, name='add-comment' ),
    path('cart/<str:pk>', views.cart, name='cart'),
    path('add_to_cart/<str:pk>', views.addToCart, name = 'add-to-cart'),
    path('remove_from_cart/<str:pk>', views.removeFromCart, name = 'remove-from-cart'),
    #path('buy_product/', views.buyProduct, name = 'buy-product').
    #path('shipments/<str:pk>', views.shipmentsPanel, name = 'shipments'),
    path('budget/<str:pk>', views.budgetPanel, name = 'budget'),
    path('add_budget/<str:pk>', views.addBudget, name='add-budget'),
    path('ratings/', include('star_ratings.urls', namespace='ratings')),
    path('contact', views.contactPanel, name = 'contact'),
    #path('shipment_ticket/<str:pk>', views.ticketCreation, name = 'shipment-ticket'),
    path('ticket_confirmation', views.ticketConfirmation, name='ticket-confirm'),
    path('ticket_panel/<str:pk>', views.ticketPanel, name='ticket-panel'),
    path('ticket_info/<str:pk>', views.ticketInfo, name='ticket-info'),
    path('stores/', views.stores, name = 'stores'),
    path('store_info/<str:pk>', views.storeInfo, name='store-info'),
    path('modify_store_product/<str:pk>', views.modifyStoreProducts, name = 'modify-product-store'),
    

]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)