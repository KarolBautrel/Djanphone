import datetime
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from django_extensions.db.fields import AutoSlugField
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


DELIVERY =(
    ('Inpost', 'Inpost'),
    ('Courier','Courier'),
    ('Post','Post'),
    ('Local Store ZG', 'Local Store - Carrefour Zielona Gora'),
    ('Local Store JP2GMD', 'Local Store - Vaticano'),
)


class User(AbstractUser):
    name = models.CharField(max_length=200,null=True)
    email= models.EmailField(null=True, unique = True)
    address = models.CharField(max_length=200,null=True)
    bio = models.TextField(null=True)
    avatar = models.ImageField(null=True, default = 'avatar.svg')
    budget = models.IntegerField(null=True, default=3000)
    
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
    image = models.ImageField( blank=True, default = 'pobrane.png')
    description = models.TextField(max_length=200,null=True, default = 'This is test field')
    created = models.DateTimeField(auto_now_add = True)
    is_approved = models.BooleanField(default=False)
    slug = AutoSlugField(populate_from=['title'],max_length=50,null=True, blank=True)

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





class Order(models.Model):

    product = models.ManyToManyField(OrderItem, blank=True ,null=True,  )
    status = models.CharField(default = 'Processed', choices = STATUS, max_length = 30,null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True, blank=True)
    start_date = models.DateTimeField(auto_now_add = True)
    ordered_date = models.DateTimeField()
    delivery = models.CharField(max_length = 200,choices = DELIVERY, null=True, blank=True)
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return self.user.name


class Store(models.Model):
    address = models.CharField(max_length=30)
    owner = models.CharField(max_length = 20)
    contact = models.IntegerField(null=True)
    products = models.ManyToManyField(Product, blank=True)
    picture = models.ImageField(null=True, default = 'avatar.svg')
    moderator = models.ForeignKey(User, on_delete=models.CASCADE,null=True, blank=True)


    def __str__(self):
        return self.address


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


class Ticket(models.Model):
    body = models.TextField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE,null=True, blank=True)
    ticket_creator = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    is_open = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add = True)


    def __str__(self):
        return str(self.ticket_creator)


