from django.shortcuts import render, redirect
from .models import Product, User
from .forms import UserForm
# Create your views here.

def home(request):
    return render(request,'base/home.html')







def products(request):
    products = Product.objects.all()
    context = {'products':products}

    return render(request,'base/products.html', context)

def userProfile(request, pk):
    user = User.objects.get(id = pk)
    user_products = user.product_set.all()
    context = {'user':user,'user_products':user_products}

    return render(request,'base/profile.html', context)

def updateProfile(request):
    user = request.user
   
    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance = user)
        if form.is_valid():
            form.save()
            return redirect('profile', pk=user.id)
    if request.method == 'GET':
         form = UserForm(instance = user)
    
    context = {'form':form}

    return render(request,'base/update_profile.html', context)   


def userPanel(request):
    return render(request, 'base/user_panel.html')
