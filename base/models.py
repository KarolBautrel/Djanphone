from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    name = models.CharField(max_length=200,null=True)
    email= models.EmailField(null=True, unique = True)
    bio = models.TextField(null=True)
    avatar = models.ImageField(null=True, default = 'avatar.svg')
    budget = models.IntegerField(null=True, default=1000000)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']






class Product(models.Model):
    name = models.CharField(max_length=30)
    price = models.IntegerField(null=True)
    image = models.ImageField(null=True)
    description = models.TextField(max_length=200)
    owner = models.ForeignKey(User,on_delete = models.SET_NULL, null=True, blank=True) 
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add = True)
    

    class Meta:
        ordering = ['-created', '-updated']



    def __str__(self):
        return self.name





class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.body[0:50]