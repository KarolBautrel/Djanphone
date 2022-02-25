from django.test import TestCase, Client
from base.models import User, Store, Product, Order,Coupon, Comment, OrderItem, Address, Message, MessageReceiver,Ticket
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone
from .forms import CheckoutShippingForm
from django.core.files.uploadedfile import SimpleUploadedFile

class RegisterTest(TestCase):

    def test_create_user_with_email_successfull(self):
        '''
        Test creating a new user with an email is successful
        '''
        email = 'test@gmsail.com'
        password = 'testpass123'
        username =  'testpass123'
        user = get_user_model().objects.create_user(
                email = email,
                password = password,
                username = username
            )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))


class AuthorizationTestCase(TestCase):
    
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create(
            email = 'email@gmamg.com',
            password = 'test21',
            name = 'tes ffasf',
        )
        self.client.force_login(self.user)

    def test_authorized_user_access_to_contact_page(self):
        '''
        Authorized user getting into contact page
        '''
        response = self.client.get(reverse('contact'))
        self.assertEqual(response.status_code,200)
        
    def test_unauthorized_is_able_to_contact_page(self):    
        '''
        Unauthorized user is able to get to contact view
        '''
        self.user = Client()
        url = reverse('contact')
        response = self.user.get(url)
        self.assertEqual(response.status_code, 200)    

    def test_authorized_user_is_able_to_add_to_cart(self):
        '''
        Authorized user is able to add product to cart
        '''
        product = Product.objects.create(title='test1234',  price=200, slug='test1234')
        url = reverse('add-to-cart', kwargs={'slug': product.slug})
        response = self.client.get(url)
        response_button = self.client.post(url, {'submit':'Confirm'})
        self.assertRedirects(response, '/order_summary/', status_code = 302)
        self.assertEqual(response_button.status_code, 302)
    
    def test_redirect_unauthorized_user_to_login_after_add_to_cart_action(self):
        '''
        Unauthorized user is unable to add to cart product
        '''
        self.user = Client()
        product = Product.objects.create(title='test1234',  price=200, slug='test1234')
        url = reverse('add-to-cart', kwargs={'slug': product.slug})
        response = self.user.get(url)
        self.assertEqual(response.status_code, 302)
        
    def test_regular_user_denied_acces_to_shop_management(self):
        '''
        User who is not moderator of shop cant enter shop management
        '''
        store = Store.objects.create(moderator = None)
        url = reverse('modify-product-store', args =str((store.id)))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
    
    def test_moderator_user_got_acces_to_shop_management(self):
        '''
        User who is moderator of shop cant enter shop management
        '''
        store = Store.objects.create(moderator = self.user)
        url = reverse('modify-product-store', args =str((store.id)))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_regular_user_is_unable_to_use_mass_message(self):
        '''
        Superuser is able to send messages to users
        '''
        url = reverse('message')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

    def test_uanuthorized_user_has_acces_to_products_page(self):
        '''
        Unauthorized user is able to get to products list page
        '''
        self.client = Client()
        url = reverse('products')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['products']),0)

    def test_unauthorized_user_is_unable_to_checkout(self):
        '''
        Unauthorized user is unable to force proceed to checkout view(billing, shipping)
        and redirected to login view
        '''
        self.client = Client()
        url_shipping = reverse('shipping')
        url_billing = reverse('billing')
        response_shipping = self.client.get(url_shipping)
        response_billing = self.client.get(url_billing)
        self.assertEqual(response_shipping.status_code, 302)
        self.assertEqual(response_billing.status_code, 302)

    def test_authorized_user_without_orders_is_unable_to_checkout(self):
        '''
        Authorized user is unable to force proceed to checkout view(billing, shipping)
        and redirected to home page.
        '''
     
        url_shipping = reverse('shipping')
        url_billing = reverse('billing')
        response_shipping = self.client.get(url_shipping)
        response_billing = self.client.get(url_billing)
        self.assertEqual(response_shipping.status_code, 302)
        self.assertEqual(response_billing.status_code, 302)


class ProductsaActionTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create(
            email = 'email@gmamg.com',
            password = 'test21',
            name = 'tes ffasf',
        )
        self.client.force_login(self.user)
        self.product = Product.objects.create(
                                            title='test1234',
                                            price=200,
                                            slug='test1234')
        self.comment = Comment.objects.create(
                                        user = self.user,
                                        product = self.product,
                                        body = 'test123'
                                        )
        
    def test_product_list_view(self):
        '''
        Checking if number of product in list view is correct
        '''
        self.client = Client()
        url = reverse('products')
        response = self.client.get(url)
        self.assertEqual(len(response.context['products']),1)

    def test_product_detail_view(self):
        '''
        Test which show correct detail product view
        '''
        url = reverse('product-detail', kwargs={'slug': self.product.slug})
        response = self.client.get(url)
        self.assertEqual(response.status_code,200)
        self.assertEqual(response.context['product'], self.product)

    def test_single_comment_creation_view(self):
        '''
        Test which shows created comment in product view
        '''
        url = reverse('product-detail', kwargs={'slug': self.product.slug})
        response = self.client.get(url)
        self.assertEqual(response.context['comments'][0], self.comment)

    def test_comments_queryset(self):
        '''
        Test if the comments queryset contains correct comments
        '''
        comments_qs = Comment.objects.filter(
                                            product = self.product
                                            )
        url = reverse('product-detail', kwargs={'slug': self.product.slug})
        response = self.client.get(url)
        self.assertQuerysetEqual(response.context['comments'], comments_qs)
    
    def test_add_comment(self):
        '''
        Test adding comment to product by authorized user
        '''
        url = reverse('add-comment', kwargs={'slug': self.product.slug})
        self.client.post(url, {'body':'This is test'})
        self.assertEqual(Comment.objects.last().body, "This is test")

    def test_adding_blank_comment(self):
        '''
        Test adding blank comment which is not gonna be add
        '''
        url = reverse('add-comment', kwargs={'slug': self.product.slug})
        self.client.post(url, {'body':''})
        self.assertEqual(Comment.objects.last().body, "test123") # body from setUp comment

    def test_delete_comment(self):
        '''
        Test of deleting comment, assertEqual remains 1 because there is one more comment
        created in setUp function.
        '''
        comment = Comment.objects.create(user = self.user,product = self.product,body = 'test123425')
        url = reverse('delete-comment', kwargs= {'pk': comment.id})
        comment_list_url = reverse('product-detail', kwargs={'slug': self.product.slug})
        self.client.post(url)
        response_product = self.client.get(comment_list_url)
        self.assertEqual(len(response_product.context['comments']), 1 )


class CartTestCase(TestCase):

    def setUp(self):
            self.client = Client()
            self.user = get_user_model().objects.create(
                email = 'email@gmamg.com',
                password = 'test21',
                name = 'tes ffasf',
            )
            self.client.force_login(self.user)
            self.product = Product.objects.create(
                                                title='test1234',
                                                price=200,
                                                slug='test1234')
            
    def test_add_to_cart(self):
        '''
        Test of adding product to cart
        '''
        url = reverse('add-to-cart', kwargs={'slug': self.product.slug})
        self.client.get(url)
        cart_url = reverse('order-summary')
        cart = self.client.get(cart_url)
        order_qs = cart.context['order'].product.all()
        order_list = [i.product for i in order_qs]
        self.assertEqual(order_list[0], self.product)
        self.assertEqual((len(order_list)), 1)

    def test_remove_from_cart(self):
        '''
        Test of removing product from cart, in this case there is need to 
        create another product in the cart to show, that one will be deleted
        '''
        product = Product.objects.create(title='secondTest',price=200,slug='secondTest')
        url = reverse('add-to-cart', kwargs={'slug': product.slug})
        self.client.get(url)
        url_delete = reverse('remove-from-cart', kwargs={'slug': self.product.slug})
        self.client.get(url_delete)
        cart_url = reverse('order-summary')
        cart = self.client.get(cart_url)
        order_qs = cart.context['order'].product.all()
        order_list = [i.product for i in order_qs]
        self.assertEqual(cart.status_code, 200)
        self.assertEqual(len(order_list), 1) 

    def test_removing_last_product_in_cart_redirect(self):
        '''
        Test that deleting last object from cart will redirect to homepage
        '''
        url = reverse('add-to-cart', kwargs={'slug': self.product.slug})
        self.client.get(url)
        url_delete = reverse('remove-from-cart', kwargs={'slug': self.product.slug})
        self.client.get(url_delete)
        cart_url = reverse('order-summary')
        cart = self.client.get(cart_url)
        self.assertEqual(cart.status_code, 302)
        
    def test_total_price_in_cart(self):
        '''
        Test if total price of products in cart is correct including floating numbers.
        '''
        product1 = Product.objects.create(title='test1', price=200.4, slug='test12345')
        product2 = Product.objects.create(title='test12', price=500.2, slug='test123456')
        product3 = Product.objects.create(title='test123', price=400.2, slug='test1234567')
        self.client.get(reverse('add-to-cart', kwargs={'slug': product1.slug}))
        self.client.get(reverse('add-to-cart', kwargs={'slug': product2.slug}))
        self.client.get(reverse('add-to-cart', kwargs={'slug': product3.slug}))
        cart = self.client.get(reverse('order-summary'))
        order_total = cart.context['order'].get_total()
        self.assertEqual(order_total, 1100.8)
        
    def test_add_single_item_to_cart(self):
        '''
        Test of adding single item to cart
        '''
        product1 = Product.objects.create(title='test1', price=200, slug='test12345')
        product2 = Product.objects.create(title='test12', price=200, slug='test123456')
        self.client.get(reverse('add-to-cart', kwargs={'slug': product1.slug}))
        self.client.get(reverse('add-to-cart', kwargs={'slug': product2.slug}))
        self.client.get(reverse('add-to-cart', kwargs={'slug': product1.slug}))
        self.client.get(reverse('remove-single-item-from-cart', kwargs={'slug': product1.slug}))
        cart = self.client.get(reverse('order-summary'))
        order_qs=cart.context['order'].product.all()
        order_quantity = sum(i.quantity for i in order_qs)
        self.assertEqual(order_quantity, 2)
        
    def test_removing_last_objects_redirects_home(self):
        '''
        Test of redirecting user after deleteing last object from cart with minus symbol
        '''
        self.client.get(reverse('remove-single-item-from-cart', kwargs={'slug': self.product.slug}))
        cart = self.client.get(reverse('order-summary'))
        self.assertEqual(cart.status_code, 302)
        self.assertRedirects(cart, '/', 302)

    def test_removing_last_objects_from_one_product_type_not_redirects_home(self):
        '''
        Test of preventing bug which redirect to homepage if u delete completely one of product
        '''
        product = Product.objects.create(title='test1', price=200, slug='test12345')
        self.client.get(reverse('add-to-cart', kwargs={'slug': product.slug}))
        self.client.get(reverse('remove-single-item-from-cart', kwargs={'slug': self.product.slug}))
        cart = self.client.get(reverse('order-summary'))
        self.assertEqual(cart.status_code, 200)


class CheckoutTestCase(TestCase):
    def setUp(self):
            self.client = Client()
            self.user = get_user_model().objects.create(
                email = 'email@gmamg.com',
                password = 'test21',
                name = 'tes ffasf',
            )
            self.client.force_login(self.user)
            self.product = Product.objects.create(
                                                title='test1234',
                                                price=200,
                                                slug='test1234'
                                                )
            self.order_item = OrderItem.objects.create(
                                                       user = self.user,
                                                       product = self.product)
            self.order = Order.objects.create(
                                            user =self.user,
                                            ordered_date=timezone.now(),
                                            )
            self.order.product.add(self.order_item)

    def test_shipping_form_valid(self):
        form = CheckoutShippingForm(data = {'shipping_city':'Test city',
                            'shipping_zip':'Test Zip',
                            'shipping_address':'Test Address',
                            'same_billing_address':'True',
                            })
        self.assertTrue(form.is_valid())

    def test_shipping_address(self):
        '''
        Test for redirect after shipping to billing form.
        '''

        url = reverse('shipping')
        shipping_address = self.client.post(url, 
                            {'shipping_city':'Test city',
                            'shipping_zip':'Test Zip',
                            'shipping_address':'Test Address'},
                            user = self.user)
        self.assertEqual(shipping_address.status_code, 302)
        self.assertRedirects(shipping_address, '/checkout/billing', 302)

    def test_redirect_payment_after_same_shipping_as_billing_radio(self):
        '''
        Test for saving billing address same as shipping address after selecting it
        and redirect directly to payment view
        '''
        
        url = reverse('shipping')
        shipping_address = self.client.post(url,    
                            {'shipping_city':'Test city',
                            'shipping_zip':'Test Zip',
                            'shipping_address':'Test Address',
                            'same_billing_address':'True',
                            },
                            user = self.user)
       
        self.assertRedirects(shipping_address, '/checkout/paypal/', 302)

    def test_redirect_to_shipping_from_billing_if_shipping_is_not_created(self):
        '''
        Test if view is redirecting user to shipping if its not created and 
        user is trying to get to billing address before.
        '''
        self.order.shipping_address = None
        url = reverse('billing')
        response = self.client.get(url)
        self.assertRedirects(response, '/checkout/shipping', 302)
   

    def test_billing_address_redirect_to_payment_after_creation(self):
        '''
        Test of redirecting user to payment after succesfully created billing address
        '''
        url_shipping = reverse('shipping')
        self.client.post(url_shipping,    
                        {'shipping_city':'Test city',
                        'shipping_zip':'Test Zip',
                        'shipping_address':'Test Address',
                        'same_billing_address':'True',
                        },
                        user = self.user)
        url = reverse('billing')
        response = self.client.post(url,
                            {'billing_city':'Test city',
                            'billing_zip':'Test Zip',
                            'billing_address':'Test Address',
                            },
                            user = self.user )
        self.assertRedirects(response, '/checkout/paypal/', 302)

    def test_billing_address_wont_redirect_if_not_all_required_fields_fullfiled(self):
        '''
        Test of redirecting user to payment after succesfully created billing address
        '''
        url_shipping = reverse('shipping')
        self.client.post(url_shipping,    
                        {'shipping_city':'Test city',
                        'shipping_zip':'Test Zip',
                        'shipping_address':'Test Address',
                        'same_billing_address':'True',
                        },
                        user = self.user)
        url = reverse('billing')
        response = self.client.post(url,
                            {'billing_city':'Test city',
                            'billing_zip':'Test Zip',
                            'billing_address':'',
                            },
                            user = self.user )
        self.assertRedirects(response, '/checkout/billing', 302)    
         ## TODO QUERYSETS


class SuperUserTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create(
                        email = 'email@gmamg.com',
                        password = 'test21',
                        name = 'tes ffasf',
                        is_moderator = True
                        )
        self.client.force_login(self.user)

    def test_superuser_can_send_mass_messages(self):
        '''
        Admin(superuser) is able to send mass messages to regular users
        '''
        url=reverse('message')
        self.client.post(url,{ 'subject':'Test Subject','body':'Test body'})
        self.assertEqual(Message.objects.count(), 1)
        self.assertEqual(Message.objects.last().subject, 'Test Subject')

    def test_superuser_can_create_new_product(self):
        '''
        Admin is able to create new product
        '''
        url = reverse('create-product')
        self.client.post(url,{'title':'Test title', 
                                'brand':'Samsung',
                                'description':'test description',
                                'price':200,
                                })
        
        self.assertEqual(Product.objects.count(), 1)


class RegularUserTestCase(TestCase):
    def setUp(self):
        self.client = Client()

        self.user = get_user_model().objects.create(
                        username = 'test_username',
                        email = 'email@gmamg.com',
                        password = 'test21',
                        name = 'testing name',
                        country = 'testing country 2',
                        city = 'testing city',
                        is_moderator = False
                        )
        self.client.force_login(self.user)

    def test_change_password(self):
        '''
        Test for changing password by user, unfortunetyl due to django-allauth and django hashing password
        I am not able to check the new password. But status 200 tells us that everything went clear.
        '''
       
        url = reverse('change-password')
        response = self.client.post(url, {
                            'old_password' : 'test21',
                            'new_password1' : 'test',
                            'new_password2' : 'test'
                                })
        
        self.assertEqual(response.status_code, 200)
        
    def test_change_email(self):
        '''
        Test for user change mail
        ''' 
        url = reverse('change-email')
        response = self.client.post(url,{
                            'email':'newemail@gmamg.com',
                            'email2': 'newemail@gmamg.com'
        })
        self.assertEqual(response.status_code, 302)
        
    def test_wrong_mail_confirmation(self):
        url = reverse('change-email')
        response = self.client.post(url,{
                            'email':'newemail@gmamg.com',
                            'email2': 'wrongnewemail@gmamg.com'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Invalid email')

    def test_profile_update_info(self):
        '''
        Test for user updating info
        '''
        url = reverse('update-user', kwargs={'pk': self.user.id})
        response = self.client.post(url,
                    {
                        'name':'Test name2', 
                        'country':'Test Country2',
                        'city':'Test City2'
                    })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(User.objects.last().name, 'Test name2')

    def test_profile_wont_be_updated_without_required_fields(self):
        '''
        Test for user wont update info without fullfill all requireds fields
        '''
        url = reverse('update-user', kwargs={'pk': self.user.id})
        response = self.client.post(url,
                    {
                        'name':'Test name2', 
                        'country':'Test Country2',
                        'city':''
                    })
        self.assertEqual(response.status_code, 200)
        self.assertTrue(User.objects.last().name, 'testing name')

    def test_user_can_delete_message_from_inbox(self):
        '''
        Test of deleting messages from inbox
        '''
        user = User.objects.create(name='testname',is_moderator=True)
        self.client.force_login(user)
        url=reverse('message')
        self.client.post(url,{ 'subject':'Test Subject','body':'Test body'})
        message = Message.objects.last()
        reverse('message-delete', kwargs={'pk':message.id})
        response = self.client.get(reverse('inbox') )
        self.assertEqual(len(response.context['notifications']),0)

    def test_user_can_read_messages_from_inbox(self):
        '''
        Test of making messages "readed" from inbox
        '''
        user = User.objects.create(name='testname',is_moderator=True)
        self.client.force_login(user)
        url=reverse('message')
        self.client.post(url,{ 'subject':'Test Subject','body':'Test body', 'receiver': self.user})
        message = MessageReceiver.objects.filter(receiver = self.user)
        response = self.client.get(reverse('message-read', kwargs = {'pk' : message[0].id}))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(message[0].is_readed, True)

    def test_user_can_view_message_details(self):
        """
        Test of reading the detail view of message
        """
        user = User.objects.create(name='testname',is_moderator=True)
        self.client.force_login(user)
        url=reverse('message')
        self.client.post(url,{ 'subject':'Test Subject','body':'Test body', 'receiver': self.user})
        message = MessageReceiver.objects.filter(receiver = self.user)
        response = self.client.get(reverse('message-detail', kwargs = {'pk' : message[0].id}))
        self.assertEqual(response.status_code, 200)
        

class TicketTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create(
                        email = 'email@gmamg.com',
                        password = 'test21',
                        name = 'tes ffasf',
                        is_moderator = True
                        )
        self.client.force_login(self.user)
        
    def test_user_can_create_ticket(self):
        url = reverse('ticket')
        self.client.post(url,{'subject':'Test subject1', 'body':'Test body1'})
        url_ticket = reverse('ticket-panel', kwargs={'pk': self.user.id})
        tickets = self.client.get(url_ticket)
        self.assertEqual(len(tickets.context['tickets']),1)
        
    def test_user_cant_create_ticket_without_all_req_fields(self):
        url = reverse('ticket')
        self.client.post(url,{'subject':'', 'body':''})
        url_ticket = reverse('ticket-panel', kwargs={'pk': self.user.id})
        tickets = self.client.get(url_ticket)
        self.assertEqual(len(tickets.context['tickets']),0)

    def test_user_can_check_all_tickets_in_ticket_panel(self):
        url = reverse('ticket')
        self.client.post(url,{'subject':'Test subject1', 'body':'Test body1'})
        url_ticket_panel = reverse('ticket-panel', kwargs = {'pk': self.user.id})
        tickets = self.client.get(url_ticket_panel)
        self.assertEqual(tickets.status_code, 200)
    
    def test_user_can_check_detail_of_ticket(self):
        url = reverse('ticket')
        self.client.post(url,{'subject':'Test subject1', 'body':'Test body1'})
        ticket = Ticket.objects.last()
        response = self.client.get(reverse('ticket-detail', kwargs={"pk": ticket.id}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['ticket'].body, 'Test body1')
        


class LocalStoreTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create(
                        email = 'email@gmamg.com',
                        password = 'test21',
                        name = 'tes ffasf',
                        is_moderator = True
                        )
        self.client.force_login(self.user)

        self.store = Store.objects.create(
                    city = 'Test City',
                    street =  'Test Street',
                    owner = 'Test Owner',
                    moderator = self.user
        )
        product = Product.objects.create(title = 'TestProduct',
                                        brand = 'Samsung',
                                        price = 500)
        self.store.products.add(product)

    def test_moderator_of_shop_can_get_to_store_management_view(self):
        url = reverse('modify-product-store', kwargs = {'pk': self.store.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_regular_user_is_404_when_trying_to_get_to_manage_view(self):
        user = User.objects.create(
                        username = 'testing name',
                        email = 'email1@gmamg.com',
                        password = 'test211',
                        name = 'tes ffasf1',
                        is_moderator = False
        )
        self.client.force_login(user)
        url = reverse('modify-product-store', kwargs = {'pk': self.store.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_stores_view(self):
        '''
        Test of getting to the store view
        Unfortunetly in this case, because of view
        there need to be atleast two local stores to get
        to the view, otherwise I couldnt implement google
        map localization.
        '''
        Store.objects.create(
                    city = 'Test City',
                    street =  'Test Street',
                    owner = 'Test Owner',
                    moderator = self.user
        )
        url = reverse('stores')
        stores = self.client.get(url)
        self.assertEqual(stores.status_code, 200)

    def test_store_detail_view(self):
        '''
        Test of getting to the store detail view
        '''
        url = reverse ('store-detail', kwargs= {'pk': self.store.id})
        store = self.client.get(url)
        store_products = store.context['store'].products.all()
        product = [i for i in store_products]
        self.assertEqual(product[0].title, 'TestProduct')
        self.assertEqual(product[0].price, 500)
        self.assertEqual(product[0].brand, 'Samsung')


class CouponTestCase(TestCase):

    def setUp (self):
        self.client = Client()
        self.user = get_user_model().objects.create(
                        email = 'email@gmamg.com',
                        password = 'test21',
                        name = 'tes ffasf',
                        is_moderator = True
                        )
        self.client.force_login(self.user)
        
    coupon = Coupon.objects.get(code='TEST')

    def test_add_coupon(self):
        url = reverse('add-coupon')
        coupon = self.client.post(url, {'code': 'TEST'})
        self.assertEqual(coupon.status_code, 302)
        
       
