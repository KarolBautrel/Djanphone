from django.shortcuts import render, redirect
from.models import Product, User
# Create your views here.

def home(request):
    return render(request,'base/home.html')







def products(request):
    products = Product.objects.all()
    context = {'products':products}

    return render(request,'base/products.html', context)


def logout(request):
    logout(request)
    return redirect('home')
