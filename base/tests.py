from django.test import TestCase, Client
from base.models import User, Store, Product
from django.contrib.auth import get_user_model
from django.urls import reverse


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
        Unauthorized user is redirect to login page after clicking contact button
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
    
    def test_redirect_unathorized_user_to_login_after_add_to_cart_action(self):
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

    def test_product_list_view(self):
        '''
        Checking if number of product in list view is correct
        '''
        Product.objects.create(title='test1234',  price=200, slug='test1234')
        self.client = Client()
        url = reverse('products')
        response = self.client.get(url)

        self.assertEqual(len(response.context['products']),1)