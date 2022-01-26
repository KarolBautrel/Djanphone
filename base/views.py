from django.shortcuts import render, redirect
from .models import Product, User, Comment, Shipment, Ticket
from .forms import UserForm, EmailChangeForm, ProductForm,TicketForm, CommentForm, ShipmentForm, BudgetForm
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
# Create your views here.

def home(request):
    return render(request,'base/home.html')



def products(request):
    products = Product.objects.all()
    context = {'products':products}

    return render(request,'base/products.html', context)

def productInfo(request,pk):
    product = Product.objects.get(id = pk)
    product_comments = product.comment_set.all()
    
    context = {'product':product, 'product_comments':product_comments}
    return render(request,'base/product_info.html', context)


def addProduct(request):
    form = ProductForm()
    if request.method == 'POST':
        Product.objects.create(name = request.POST.get('name'),
                                price = request.POST.get('price'),
                                image = request.POST.get('image'),
                                description = request.POST.get('description'))
    
        return redirect ('confirm-product-creation')
    context = {'form': form}
    return render(request,'base/product_form.html', context)

def addProductConfirmation(request):

    return render(request,'base/product_add_confirmation.html')


def buyProduct(request, pk):
    product = Product.objects.get(id = pk)
    shipment_form = ShipmentForm()
    user = request.user
    if request.method == 'POST':
        if request.user.budget >= product.price:
            product.owner = user
            user.budget -= product.price 
            user.save()
            product.owner.save()
            shipment_form = ShipmentForm(request.POST)
            if shipment_form.is_valid():
                shipment = shipment_form.save(commit=False)
                shipment.ship_to = user
                shipment.product = product
                shipment.save()
               
                shipment_form.save()
                messages.success(request, f'You bought {product.name}')
                redirect ('home')
        else:
            messages.error(request, 'not enough money')
    context = {'shipment_form':shipment_form}
    return render(request,'base/buy_product.html',context)
    









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
        
        return redirect ('product-info', pk=product.id)
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



def shipmentsPanel(request,pk):
    user = User.objects.get(id = pk)
    shipments = user.shipment_set.all()
    context = {'user':user,'shipments': shipments}  
    return render(request,'base/shipments.html', context)

def budgetPanel(request,pk):
    user = User.objects.get(id = pk) 
    return render(request,'base/budget_panel.html')



def addBudget(request, pk):
    user = User.objects.get(id = pk)
    if request.method == 'POST':
        form = BudgetForm(request.POST)
        if form.is_valid():
            budget_form = form.save(commit=False)
            user.budget += budget_form.budget
            user.save()
            messages.error(request, f'You added {budget_form.budget}$')
            return redirect ('home')
    if request.method == 'GET':
        form = BudgetForm()

    context = {'form':form}
    return render(request,'base/add_budget.html', context)




def contactPanel(request):
    
    return render(request,'base/contact_panel.html')


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
            return redirect ('ticket-confirm')
    context = {'form':form, 'shipments':shipments}

    return render(request,'base/shipment_ticket.html', context)


def ticketConfirmation(request):
    return render(request, 'base/ticket_confirm.html')


def ticketPanel (request, pk):
    user = User.objects.get(id=pk)
    tickets = user.ticket_set.all()
    context = {'user':user, 'tickets':tickets}
    return render (request,'base/tickets.html', context)



def ticketInfo(request,pk):
    ticket = Ticket.objects.get(id=pk)

    context= {'ticket':ticket}

    return render(request, 'base/ticket_info.html', context)


def stores(request):
    return render (request, 'base/stores.html')