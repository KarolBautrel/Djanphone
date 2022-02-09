from itertools import product
from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, User, Comment, Order, Ticket,Store,OrderItem
from .forms import UserForm, EmailChangeForm, ProductForm,TicketForm, CommentForm, OrderForm, BudgetForm, StoreForm
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import HttpResponse, HttpResponseRedirect
from .filters import ProductFilter
from django.views.generic import UpdateView, ListView, DetailView, View, CreateView
from django.utils import timezone
from django.urls import reverse
# Create your views here.


def home(request):
    return render(request,'base/home.html')


def is_valid_queryparam(param):
    return param != '' and param is not None


class ProductListView(ListView):
    model = Product
    context_object_name = 'products'
    template_name = 'base/products.html'


class ProductDetailView(View):
    
    def get(self, request,slug, *args, **kwargs):
        product = Product.objects.get(slug = slug)
        product_comments = product.comment_set.all()
        context = {'product':product, 'product_comments':product_comments}
        return render(request,'base/product_detail.html', context)


class CommentCreationView(CreateView):
    model = Comment
    fields = ['body']
    template_name  = 'base/add_comment.html'

    def get_queryset(self):
        queryset = Product.objects.get(slug=self.slug)
        return queryset


    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user = self.request.user
        obj.product = self.product
        obj.save()        
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('home')


"""
@login_required
def addComment(request,slug):
    form = CommentForm()
    product = Product.objects.get(slug = slug)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
           comment = form.save(commit=False)
           comment.user = request.user
           comment.product = product
           comment.save()
        return redirect('product-detail', slug=slug)
    if request.method == 'GET':
          product = Product.objects.get(slug = slug)
    context = {'product':product, 'form':form}
    return render(request,'base/add_comment.html', context)
"""


@login_required
def addToCart(request, slug):
    product = get_object_or_404(Product, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(
        product=product,
        user = request.user, 
        ordered = False
    )
    order_qs = Order.objects.filter(user=request.user, ordered = False)
    print(order_qs)
    if order_qs.exists():
        order = order_qs[0]
        print(order)
        #check if the order item is in the order list
        if order.product.filter(product__slug = product.slug).exists():
            order_item.quantity += 1
            order_item.save()
        else:
            order.product.add(order_item)
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user,ordered_date=ordered_date)
        order.product.add(order_item)
    messages.success(request, 'You added the product to your cart')
    return redirect('product-detail', slug=slug)


@login_required
def removeFromCart(request, slug):
    product = get_object_or_404(Product, slug=slug)
    order_qs = Order.objects.filter(user=request.user, ordered = False)
    if order_qs.exists():
        order = order_qs[0]
        #check if the order item is in the order list
        if order.product.filter(product__slug = product.slug).exists():
            order_item = OrderItem.objects.filter(
                product=product,
                user = request.user, 
                ordered = False
            )[0]
            order.product.remove(order_item)
            messages.success(request, 'You removed the product from your cart')
        else:
            messages.success(request, 'There is no product to remove')
            return redirect('product-detail', slug=slug)
    else: 
            
        messages.success(request, 'User doesnt have order')
        return redirect('home')
    return redirect('product-detail', slug=slug)



@login_required
def cart(request,pk):
    user=request.user
    products = user.cart.products.all()
    products_price = sum([i.price for i in products])
    context={'products':products, 'products_price':products_price}
    return render(request, 'base/cart.html', context)



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
    return render(request,'base/delete_comment.html', context)


class UserDetailView(DetailView):
    model = User
    context_object_name = 'user'
    template_name = 'base/profile.html'


class UpdateUserView(UpdateView):
    model = User
    fields = ['name', 'address', 'bio', 'avatar']
    template_name  = 'base/update_profile.html'
    


def userPanel(request):
    return render(request, 'base/user_panel.html')


class ProductCreateView(CreateView):
    model = Product
    fields = ['title','brand','price','image','description']
    template_name = 'base/product_create.html'


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


"""def shipmentsPanel(request,pk):
    user = User.objects.get(id = pk)
    shipments = user.shipment_set.all()
    context = {'user':user,'shipments': shipments}  
    return render(request,'base/shipments.html', context)"""


def budgetPanel(request,pk):
    user = User.objects.get(id = pk) 
    return render(request,'base/budget_panel.html')


@login_required
def contactPanel(request):
    return render(request,'base/contact_panel.html')

    



class TicketCreationView(CreateView):
    model = Ticket
    fields = ['body','product']
    template_name  = 'base/ticket.html'

    
    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.ticket_creator = self.request.user
        obj.save()        
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('home')


"""@login_required
def ticketCreation(request, pk):
    user = User.objects.get(id = pk)
    orders = user.order_set.all()
    form = TicketForm(user=user)
    if request.method == 'POST':
        form = TicketForm(request.POST, user=user)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.ticket_creator = user
            ticket.order
            ticket.save()
            return redirect('ticket-confirm')
    context = {'form':form, 'shipments':shipments}
    return render(request,'base/shipment_ticket.html', context)"""

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
    productFilter = ProductFilter(request.GET, queryset=products)
    products = productFilter.qs
    context = {'store':store, 'products':products, 'productFilter':productFilter}
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