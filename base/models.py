import datetime
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse

STATUS = (
    ('Processed', 'Proccesed'),
    ('Sent', 'Sent'),
    ('Delivered', 'Delivered')
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
        return reverse('user-detail', kwargs={'slug': self.slug})


class Brand(models.Model):
    brand = models.CharField(max_length=20, null=True, blank=True)
    

    def __str__(self):
        return self.brand


class Product(models.Model):
    title = models.CharField(max_length = 100,null=True)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE,null=True, blank=True)
    price = models.IntegerField(null=True, blank=True)
    image = models.ImageField( blank=True, default = 'pobrane.png')
    description = models.TextField(max_length=200,null=True)
    created = models.DateTimeField(auto_now_add = True)
    is_approved = models.BooleanField(default=False)
    

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.title


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return self.title





class Order(models.Model):
    products = models.ManyToManyField(OrderItem, blank=True ,null=True,  )
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
    order = models.ForeignKey(Order, on_delete=models.CASCADE,null=True, blank=True)
    ticket_creator = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    is_open = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add = True)


    def __str__(self):
        return str(self.order)


