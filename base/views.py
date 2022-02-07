from itertools import product
from django.shortcuts import render, redirect
from .models import Product, User, Comment, Shipment, Ticket,Store,Brand
from .forms import UserForm, EmailChangeForm, ProductForm,TicketForm, CommentForm, ShipmentForm, BudgetForm, StoreForm
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

# Create your views here.


def home(request):
    return render(request,'base/home.html')


def is_valid_queryparam(param):
    return param != '' and param is not None


def products(request):
    products = Product.objects.all()
    brands = Brand.objects.all()
    name_contains = request.GET.get('name_contains')
    view_price_min = request.GET.get('product_price_min')
    view_price_max = request.GET.get('product_price_max')
    date_min = request.GET.get('date_min')
    date_max = request.GET.get('date_max')
    brand = request.GET.get('brand')
    if is_valid_queryparam(name_contains):
        products = products.filter(name__icontains=name_contains)
    if is_valid_queryparam(view_price_min):
        products = products.filter(price__gte=view_price_min) #__gte = greater than equ
    if is_valid_queryparam(view_price_max):
        products = products.filter(price__lte=view_price_max) #__lte = less than 
    if is_valid_queryparam(date_min):
        products = products.filter(created__lt=date_min) 
    if is_valid_queryparam(date_max):
        products = products.filter(created__gte=date_max) 
    if is_valid_queryparam(brand) and brand != 'All':
        products = products.filter(brand__brand=brand) 
    context = {'products':products, 'brands':brands}
    return render(request,'base/products.html', context)


def productInfo(request,pk):
    product = Product.objects.get(id = pk)
    product_comments = product.comment_set.all()
    context = {'product':product, 'product_comments':product_comments}
    return render(request,'base/product_info.html', context)


def addProduct(request):
    form = ProductForm()
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('confirm-product-creation')
    context = {'form': form}
    return render(request,'base/add_product_form.html', context)


def addProductConfirmation(request):
    return render(request,'base/product_add_confirmation.html')


@login_required
def buyProduct(request, pk):
    product = Product.objects.get(id = pk)
    shipment_form = ShipmentForm()
    user = request.user
    if request.method == 'POST':
        if request.user.budget >= product.price:
            product.owner = user
            user.budget -= product.price 
            user.save()
            shipment_form = ShipmentForm(request.POST)
            if shipment_form.is_valid():
                shipment = shipment_form.save(commit=False)
                shipment.ship_to = user
                shipment.product = product
                shipment.save()              
                shipment_form.save()
                messages.success(request, f'You bought {product.name}')
                redirect('home')
        else:
            messages.error(request, 'not enough money')
    context = {'shipment_form':shipment_form}
    return render(request,'base/buy_product.html',context)


# TODO
@login_required
def addComment(request,pk):
    form = CommentForm()
    product = Product.objects.get(id = pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
           comment = form.save(commit=False)
           comment.user = request.user
           comment.product = product
           comment.save()
        return redirect('product-info', pk=product.id)
    if request.method == 'GET':
          product = Product.objects.get(id = pk)
    context = {'product':product, 'form':form}
    return render(request,'base/add_comment.html', context)


@login_required
def deleteComment(request, pk):
    comment = Comment.objects.get(id=pk)
    if request.user != comment.user:
        messages.error(request, 'You are not allowed to delete')
        return redirect('home')
    if request.method == 'POST': 
        comment.delete() # usuniecie
        return redirect('home')
    context ={"comment":comment} 
    return render(request,'base/delete.html', context)


# TODO
def userProfile(request, pk):
    user = User.objects.get(id = pk)
    context = {'user':user}
    return render(request,'base/profile.html', context)


@login_required
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


def shipmentsPanel(request,pk):
    user = User.objects.get(id = pk)
    shipments = user.shipment_set.all()
    context = {'user':user,'shipments': shipments}  
    return render(request,'base/shipments.html', context)


def budgetPanel(request,pk):
    user = User.objects.get(id = pk) 
    return render(request,'base/budget_panel.html')


@login_required
def contactPanel(request):
    return render(request,'base/contact_panel.html')


@login_required
def ticketCreation(request, pk):
    user = User.objects.get(id = pk)
    shipments = user.shipment_set.all()
    form = TicketForm(user=user)
    if request.method == 'POST':
        form = TicketForm(request.POST, user=user)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.ticket_creator = user
            ticket.shipment
            print(ticket.shipment) 
            ticket.save()
            return redirect('ticket-confirm')
    context = {'form':form, 'shipments':shipments}
    return render(request,'base/shipment_ticket.html', context)


def ticketConfirmation(request):
    return render(request, 'base/ticket_confirm.html')


@login_required
def ticketPanel (request, pk):
    user = User.objects.get(id=pk)
    tickets = user.ticket_set.all()
    context = {'user':user, 'tickets':tickets}
    return render(request,'base/tickets.html', context)


def ticketInfo(request,pk):
    ticket = Ticket.objects.get(id=pk)
    context= {'ticket':ticket}
    return render(request, 'base/ticket_info.html', context)


def stores(request):
    store = Store.objects.get(id=1)
    store2=Store.objects.get(id=2)
    context = {'store':store, 'store2':store2}
    return render(request, 'base/stores.html', context)


#
def storeInfo(request, pk):
    store = Store.objects.get(id=pk)
    products = store.products.all()
 
    context = {'store':store, 'products':products}
    return render(request, 'base/store_info.html', context)


# TODO
@login_required
def modifyStoreProducts(request,pk):
    
    store = Store.objects.get(id=pk)
    if request.user == store.moderator:
        store_form = StoreForm(instance = store)
        if request.method == 'POST':
            store_form = StoreForm(request.POST, instance = store)
            if store_form.is_valid() and request.user == store.moderator:
                store_form.save()
                messages.success(request, f'You added new product')
                return redirect('home')
            else:
                return HttpResponse(status=404)
    else:
        return HttpResponse(status=404) 

    context = {'store':store, 'store_form':store_form}
    return render(request, 'base/modify_product_store.html', context)


@login_required
def addBudget(request, pk):
    user = User.objects.get(id = pk)
    if request.method == 'POST':
        form = BudgetForm(request.POST)
        if form.is_valid():
            budget_form = form.save(commit=False)
            user.budget += budget_form.budget
            user.save()
            messages.error(request, f'You added {budget_form.budget}$')
            return redirect('home')
    if request.method == 'GET':
        form = BudgetForm()
    context = {'form':form}
    return render(request,'base/add_budget.html', context)