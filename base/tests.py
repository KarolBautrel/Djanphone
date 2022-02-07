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
        

    def test_unauthorized_user_redirect_to_login_page_after_contact_page(self):    
        '''
        Unauthorized user is redirect to login page after clicking contact button
        '''
        self.user = Client()
        url = reverse('contact')
        response = self.user.get(url)

        self.assertRedirects(response,'/accounts/login/?next=/contact', 302)        


    def test_authorized_user_to_is_able_to_buy(self):
        '''
        Authorized user is able to buy product
        '''
        product = Product.objects.create(name='test1234',  price=200)
        url = reverse('buy-product', args=str((product.id)))
        response = self.client.get(url)
        response_button = self.client.post(url, {'submit':'Confirm'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_button.status_code, 200)
    

    def test_redirect_unathorized_user_to_login_after_buy_action(self):
        '''
        Unauthorized user is unable to buy a product
        '''
        self.user = Client()
        product = Product.objects.create(name='test1234', price=200)
        url = reverse('buy-product', args=str((product.id)))
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

   