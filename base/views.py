from django.shortcuts import render, redirect
from .models import Product, User
from .forms import UserForm, EmailChangeForm, ProductForm
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
# Create your views here.

def home(request):
    return render(request,'base/home.html')



def products(request):
    products = Product.objects.all()
    context = {'products':products}

    return render(request,'base/products.html', context)

def productInfo(request,pk):
    products = Product.objects.get(id = pk)
    context = {'products':products}

    return render(request,'base/product_info.html', context)



def addProduct(request):
    form = ProductForm()
    if request.method == 'POST':
        Product.objects.create(name = request.POST.get('name'),
                                price = request.POST.get('price'),
                                image = request.POST.get('image'),
                                description = request.POST.get('description'))

        return redirect ('home')
    context = {'form': form}
    return render(request,'base/product_form.html', context)




























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



def changeEmail(request):
    user = request.user

    if request.method == 'POST':
        form = EmailChangeForm(request.POST, instance = user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Change completed')
            return redirect('home')
        else:
             messages.error(request, 'Invalid email')


    else:
        request.method == 'GET'
        form = EmailChangeForm(instance = user) 
    context={'form':form}
    return render(request, 'base/change_email.html', context)



def changePassword(request):
    user = request.user

    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Change completed')
            return redirect('home')
        else:
            messages.error(request, 'Old password incorrect or new passwords doesnt match')

    else:
        form = PasswordChangeForm(request.user)
    context = {'form':form}
    return render(request, 'base/change_password.html', context)