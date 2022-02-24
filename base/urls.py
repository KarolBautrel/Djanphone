from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from . import (views,
               online_shop,
               user,
               communication_user,
               superuser_panel,
               local_stores
               )

from base.views import (
                HomeView,        
                )
from base.online_shop import (
             ProductListView,
             ProductDetailView, 
             CommentCreationView,
             OrderSummaryView,
             CheckoutShippingView,
             CheckoutBillingView,
             PaymentPaypalView,
             PaymentSuccessView,
             AddCouponView
)       
from base.user import (
        UpdateUserView, 
        UserDetailView,
        InboxView,
        MessageDetailView
)
from base.communication_user import (
                                    ContactView,
                                    TicketCreationView
                                    )       
from base.superuser_panel import (
                        ProductCreateView,
                        SendMessageCreationView
                        )
                        
urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('products/', ProductListView.as_view(), name='products'),
    path('products/<slug>', ProductDetailView.as_view(), name = 'product-detail'),
    path('add_to_cart/<slug>', online_shop.addToCart, name = 'add-to-cart'),
    path('remove_from_cart/<slug>', online_shop.removeFromCart, name = 'remove-from-cart'),
    path('remove_item_from_cart/<slug>', online_shop.removeSingleItemFromCart, 
                                          name = 'remove-single-item-from-cart'),
    path('add_comment/<slug>', login_required(CommentCreationView.as_view(),
                               login_url = '/accounts/login/'), name='add-comment' ),
    path('delete_comment/<int:pk>', online_shop.deleteComment, name = 'delete-comment'),
    path('order_summary/', login_required(OrderSummaryView.as_view(),
                            login_url='/accounts/login/'),name='order-summary'),
    path('add_coupon/', login_required(AddCouponView.as_view(),login_url='/accounts/login/'), name = 'add-coupon'),
    path('checkout/shipping', login_required(CheckoutShippingView.as_view(), login_url='/accounts/login/'),name='shipping'),
    path('checkout/billing', login_required(CheckoutBillingView.as_view(), login_url='/accounts/login/'),name='billing'),
    path('checkout/paypal/', login_required(PaymentPaypalView.as_view(),login_url='/accounts/login/'), name='paypal'),
    path('complete',login_required(PaymentSuccessView.as_view(),login_url='/accounts/login/'), name='payment-succes'),
    path('account_settings/', user.settingsPanel, name = 'account-settings'),
    path('account_settings/<int:pk>/profile/', UserDetailView.as_view(), name = 'profile'),
    path('account_settings/update_profile/<int:pk>', login_required(UpdateUserView.as_view(), 
                                    login_url='/accounts/login/'), name='update-user'),
    path('account_settings/change_email', user.changeEmail, name = 'change-email'),
    path('account_settings/change-password', user.changePassword, name = 'change-password'),
    path('inbox', InboxView.as_view(), name='inbox' ),
    path('message_detail/<int:pk>', MessageDetailView.as_view(), name='message-detail'),
    path('read_message/<int:pk>', user.read_message, name= 'message-read' ),
    path('delete_message/<int:pk>', user.delete_message, name= 'message-delete' ),
    
    path('accounts/', include('allauth.urls')),
    path('ratings/', include('star_ratings.urls', namespace='ratings')),
    path('contact', ContactView.as_view(), name = 'contact'),
    path('create_ticket/', login_required(TicketCreationView.as_view(),
                            login_url='/accounts/login/'),name = 'ticket'),
    path('ticket_panel/<int:pk>', communication_user.ticketPanel, name='ticket-panel'),
    path('ticket_info/<int:pk>', communication_user.ticketInfo, name='ticket-detail'),
    path('stores/', local_stores.stores, name = 'stores'),
    path('store_info/<int:pk>', local_stores.storeInfo, name='store-detail'),
    path('modify_store_product/<int:pk>', local_stores.modifyStoreProducts, name = 'modify-product-store'),
    path('superuser_panel', superuser_panel.adminPanel, name = 'superuser'),
    path('superuser_panel/message', SendMessageCreationView.as_view(), name='message'),
    path('superuser_panel/createProduct', ProductCreateView.as_view(), name = 'create-product'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)