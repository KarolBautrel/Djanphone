from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from . import views
from base.views import (
                HomeView,
                UpdateUserView, 
                ProductListView,
                ProductDetailView, 
                UserDetailView,
                ProductCreateView,
                TicketCreationView,
                CommentCreationView,
                OrderSummaryView,
                CheckoutView,
                ContactView)


urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('products/', ProductListView.as_view(), name='products'),
    path('products/<slug>', ProductDetailView.as_view(), name = 'product-detail'),
    path('add_to_cart/<slug>', views.addToCart, name = 'add-to-cart'),
    path('remove_from_cart/<slug>', views.removeFromCart, name = 'remove-from-cart'),
    path('remove_item_from_cart/<slug>', views.removeSingleItemFromCart, 
                                          name = 'remove-single-item-from-cart'),
    path('order_summary/', login_required(OrderSummaryView.as_view(),
                            login_url='/accounts/login/'),name='order-summary'),
    path('checkout', login_required(CheckoutView.as_view(),
                        login_url='/accounts/login/'),name='checkout'),
    path('accounts/', include('allauth.urls')),
    path('<int:pk>/profile/', UserDetailView.as_view(), name = 'profile'),
    path('update_profile/<int:pk>', login_required(UpdateUserView.as_view(), 
                                    login_url='/accounts/login/'), name='update-user'),
    path('user_panel', views.userPanel, name = 'user-panel'),
    path('change_email', views.changeEmail, name = 'change-email'),
    path('change-password', views.changePassword, name = 'change-password'),
   
    path('createProduct', ProductCreateView.as_view(), name = 'create-product'),
    path('delete_comment/<int:pk>', views.deleteComment, name = 'delete-comment'),
    path('add_comment/<slug>', login_required(CommentCreationView.as_view(),
                               login_url = '/accounts/login/'), name='add-comment' ),
    path('budget/<int:pk>', views.budgetPanel, name = 'budget'),
    path('add_budget/<int:pk>', views.addBudget, name='add-budget'),
    path('ratings/', include('star_ratings.urls', namespace='ratings')),
    path('contact', ContactView.as_view(), name = 'contact'),
    path('create_ticket/', login_required(TicketCreationView.as_view(),
                            login_url='/accounts/login/'),name = 'ticket'),
    path('ticket_panel/<int:pk>', views.ticketPanel, name='ticket-panel'),
    path('ticket_info/<int:pk>', views.ticketInfo, name='ticket-info'),
    path('stores/', views.stores, name = 'stores'),
    path('store_info/<int:pk>', views.storeInfo, name='store-info'),
    path('modify_store_product/<int:pk>', views.modifyStoreProducts, name = 'modify-product-store'),
    

]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)