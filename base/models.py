from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    name = models.CharField(max_length=200,null=True)
    email= models.EmailField(null=True, unique = True)
    address = models.CharField(max_length=200,null=True)
    bio = models.TextField(null=True)
    avatar = models.ImageField(null=True, default = 'avatar.svg')
    budget = models.IntegerField(null=True, default=3000)
    

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

class Brand(models.Model):
    brand = models.CharField(max_length=20, null=True, blank=True)
    
    def __str__(self):
        return self.brand






class Product(models.Model):
    model = models.CharField(max_length = 20,null=True)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE,null=True, blank=True)
    name = models.CharField(max_length=30)
    price = models.IntegerField(null=True)
    image = models.ImageField(null=True, blank=True)
    description = models.TextField(max_length=200,null=True)
    owner = models.ForeignKey(User,on_delete = models.SET_NULL, null=True, blank=True) 
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add = True)
    is_approved = models.BooleanField(default=False)
   
    class Meta:
        ordering = ['-created', '-updated']



    def __str__(self):
        return self.name


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


class Delivery(models.Model):
    home = models.BooleanField(default=False)
    courier = models.BooleanField(default=False)
    inpost = models.BooleanField(default=False)
    post = models.BooleanField(default=False)
    store = models.ForeignKey(Store, on_delete=models.CASCADE,null=True, blank=True)


 



class Shipment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE,null=True, blank=True)
    finished = models.BooleanField(default = False)
    ship_to = models.ForeignKey(User, on_delete=models.CASCADE,null=True, blank=True)
    created = models.DateTimeField(auto_now_add = True)
    delivery = models.ForeignKey(Delivery, on_delete=models.CASCADE,null=True, blank=True)


    def __str__(self):
        return str(self.product)

class Ticket(models.Model):
    body = models.TextField()
    shipment = models.ForeignKey(Shipment, on_delete=models.CASCADE,null=True, blank=True)
    ticket_creator = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    is_open = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return str(self.shipment)

    

