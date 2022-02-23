import datetime
from io import BytesIO 
from PIL import Image
from django.core.files import File
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from django_extensions.db.fields import AutoSlugField
from django_resized import ResizedImageField
from django_countries.fields import CountryField
from django.core.mail import send_mail
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill

STATUS = (
    ('Processed', 'Proccesed'),
    ('Sent', 'Sent'),
    ('Delivered', 'Delivered')
)

BRAND = (
    ('Different','Different'),
    ('Samsung', 'Samsung'),
    ('Iphone', 'Iphone'),
    ('Xiaomi', 'Xiaomi'),
    ('Huawei', 'Huawei')
)

ADDRESS_TYPES = (
    ('Shipping','Shipping'),
    ('Billing', 'Billing')
)


class User(AbstractUser):
    name = models.CharField(max_length=200,blank=True,null=True)
    email= models.EmailField(null=True, unique = True)
    country = models.CharField(max_length = 100,blank=True,null=True)
    city = models.CharField(max_length = 100,blank=True, null=True)
    is_superuser = models.BooleanField(null=True, default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def get_absolute_url(self):
        return reverse('profile', args = [(self.id)])

    def get_update_profile_url(self):
        return reverse('update-user', args = [(self.id)])


class Product(models.Model):

    title = models.CharField(max_length = 100,null=True)
    brand = models.CharField(default = 'Different',max_length = 100,null=True, blank=True, choices = BRAND)
    price = models.FloatField(null=True, blank=True)
    discount_price = models.FloatField(null=True, blank = True)
    image = models.ImageField(  default = 'pobrane.png')
    image_thumbnail = ImageSpecField(source='image',
                                  processors=[ResizeToFill(100, 100)],
                                  format='JPEG',
                                  options={'quality': 60})
    thumbnail = models.ImageField( default = 'pobrane.png')
    description = models.TextField(max_length=200,null=True, default = 'This is test field')
    created = models.DateTimeField(auto_now_add = True)
    is_approved = models.BooleanField(default=False)
    slug = AutoSlugField(populate_from=['title'],max_length=50,null=True, blank=True)
    status = models.CharField(default = 'Different',max_length = 100,null=True, blank=True, choices = BRAND)
    class Meta:
        ordering = ['-created']


    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('product-detail', kwargs={'slug': self.slug})

    def get_add_to_cart_url(self):
        return reverse('add-to-cart', kwargs={'slug': self.slug})

    def get_remove_from_cart_url(self):
        return reverse('remove-from-cart', kwargs={'slug': self.slug})

    


class OrderItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True, blank=True)
    ordered = models.BooleanField(default=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(null=True, blank=True, default = 1)
    
    def __str__(self):
       return f'{self.quantity} of {self.product.title}'

    def get_total_product_price(self):
        return self.quantity * self.product.price

    def get_total_product_discount_price(self):
        return self.quantity * self.product.discount_price
        
    def get_amount_saved(self):
        try:
            percent_save = ((self.get_total_product_discount_price() * 100 )/ self.get_total_product_price())
        except ZeroDivisionError:
            percent_save = 0
        return int(percent_save)

    def get_final_price(self):
        if self.product.discount_price:
            return self.get_total_product_discount_price()
        return self.get_total_product_price()

    def get_cart_item_count(self):
        return self.quantity

        
class Order(models.Model):
    product = models.ManyToManyField(OrderItem, blank=True   )
    status = models.CharField(default = 'Processed', choices = STATUS, max_length = 30,null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True, blank=True)
    start_date = models.DateTimeField(auto_now_add = True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)
    billing_address = models.ForeignKey('Address',related_name = 'billing_address', on_delete=models.SET_NULL, blank=True, null=True)
    shipping_address = models.ForeignKey('Address',related_name = 'shipping_address', on_delete=models.SET_NULL, blank=True, null=True)
    coupon = models.ForeignKey('Coupon', on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.user.name

    def get_total(self):
        total = 0
        for order_item in self.product.all():
            total += order_item.get_final_price()
        if self.coupon:
            total -= self.coupon.amount
        return total


class Store(models.Model):
    city = models.CharField(max_length=30)
    street = models.CharField(max_length=30)
    owner = models.CharField(max_length = 20)
    contact = models.IntegerField(null=True)
    products = models.ManyToManyField(Product, blank=True)
    picture = models.ImageField(null=True, default = 'avatar.svg')
    moderator = models.ForeignKey(User, on_delete=models.CASCADE,null=True, blank=True)

    def __str__(self):
        return self.city

    def get_absolute_url(self):
        return reverse('store_info', args = [str(self.id)])

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.body[0:50]


class Contact(models.Model):
    name = models.CharField(max_length=20)
    email = models.EmailField(max_length=30)
    phone = models.IntegerField()
    body = models.TextField(max_length=30)

    def __str__(self):
        return self.email

    def mail_send(self):
        send_mail(
            'Thank you for contact',
        'Our team is reviewing your message, stay tuned for answer.',
        'Djanphone@gmail.com',
        [f'{self.email}'],
        )


class Ticket(models.Model):
    body = models.TextField(blank=False)
    subject = models.CharField(max_length=25, null=True)
    ticket_creator = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    is_open = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return str(self.ticket_creator)


class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    street_address = models.CharField(max_length=100)
    apartment_address = models.CharField(max_length=100)
    country = CountryField(multiple = False)
    zip = models.CharField(max_length=100)
    address_type = models.CharField(max_length=10,blank=True, choices = ADDRESS_TYPES, default = 'Billing')
    default = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user.username} with {self.street_address} as {self.address_type}'


class Message(models.Model):
    subject = models.CharField(max_length=30, blank=True, null=False)
    creator = models.ForeignKey(User, related_name="sender",on_delete=models.CASCADE)
    receiver = models.ManyToManyField(User,)
    body = models.TextField(max_length=500, null=False)
    created = models.DateTimeField(auto_now_add=True)
    is_readed = models.BooleanField(default=False)
    slug = AutoSlugField(populate_from=['subject'],max_length=50,null=True, blank=True)

    def __str__(self):
        return f'sender:{self.creator.name}, receiver : {self.receiver.name}'


class MessageReceiver(models.Model):
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    is_readed = models.BooleanField(default=False)

    def __str__(self):
        return self.receiver.name


class ShipmentAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    country = CountryField(blank_label='(select country)')
    state = models.CharField( max_length=255, null=False, blank=True)
    city = models.CharField( max_length=255, null=False, blank=True)
    street = models.CharField( max_length=255, null=False, blank=True)
    zip_code = models.CharField( max_length=255, null=False, blank=True)


class Coupon(models.Model):
    code=models.CharField(max_length=15, null=False, blank=True)
    amount = models.FloatField( null=False, blank=True)

    def __str__(self):
        return self.code