from django.shortcuts import render, redirect, get_object_or_404
from .models import (Product,
                    Comment,
                    Order,
                    OrderItem,
                    BillingAddress,
                    )
from .forms import CheckoutForm                                 
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import  HttpResponseRedirect
from .filters import ProductFilter
from django.views.generic import (
                                ListView,
                                DetailView,
                                View, 
                                CreateView,
                                )

from django.utils import timezone
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist
import stripe
from django.conf import settings
from django.http import JsonResponse
stripe.api_key = settings.STRIPE_SECRET_KEY

class ProductListView(ListView):
    model = Product
    context_object_name = 'products'
    paginate_by = 4
    template_name = 'base/products.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        filter = ProductFilter(self.request.GET, queryset)
        return filter.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = self.get_queryset()
        filter = ProductFilter(self.request.GET, queryset)
        context['filter'] = filter
        return context


class ProductDetailView(DetailView):
    model = Product
    context_object_name = 'product'
    template_name = 'base/product_detail.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        product = self.get_object().comment_set.all()
        context['comments'] = product
        return context


class CommentCreationView(CreateView):
    model = Comment
    fields = ['body']
    template_name  = 'base/add_comment.html'

    def form_valid(self, form):
        obj = form.save(commit=False)
        product = Product.objects.get(slug=self.kwargs["slug"])
        obj.user = self.request.user
        obj.product = product
        obj.save()        
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('product-detail', kwargs={'slug': self.kwargs['slug']})


@login_required
def deleteComment(request, pk):
    comment = get_object_or_404(Comment, id=pk)
    if request.user != comment.user:
        messages.error(request, 'You are not allowed to delete')
        return redirect('home')
    if request.method == 'POST': 
        comment.delete() # usuniecie
        return redirect('product-detail', slug=comment.product.slug)
    context ={"comment":comment} 
    return render(request,'base/delete_comment.html', context)


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
    return redirect('order-summary')


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
            order_item.delete()
            
            messages.success(request, 'You removed the product from your cart')
            return redirect('order-summary')
        else:
            messages.success(request, 'There is no product to remove')
            return redirect('product-detail', slug=slug)
    else: 
        messages.success(request, 'User doesnt have order')
        return redirect('order-summary')
    

@login_required
def removeSingleItemFromCart(request, slug):
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
            order_item.quantity -= 1
            order_item.save()
            if order_item.quantity == 0:
                order_item.delete()
            messages.success(request, 'This item quantity was decreased by 1 ')
            return redirect('order-summary')
        else:
            messages.success(request, 'There is no product to remove')
            return redirect('product-detail', slug=slug)
    else: 
        messages.success(request, 'User doesnt have order')
        return redirect('order-summary')
    

class OrderSummaryView(View):

    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {'order':order}
            return render(self.request, 'base/order_summary.html', context)
        except ObjectDoesNotExist:
            messages.error(self.request, 'You do not have active orders')
            return redirect ('/')
        

class CheckoutView(View):
    
    def get(self, *args, **kwargs):
        form = CheckoutForm()
        order = Order.objects.get(user=self.request.user, ordered=False)
        context = {'form': form, 'order':order}
        return render(self.request,'base/checkout.html', context)

    def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST)
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            if form.is_valid():
                street_address = form.cleaned_data['street_address']
                apartment_address = form.cleaned_data['apartment_address']
                country = form.cleaned_data['country']
                zip = form.cleaned_data['zip']
                # TO DO, DODAC LOGIKE
                #same_shipping_address =form.cleaned_data['same_billing_address']
                #save_info = form.cleaned_data['save_info']
                payment_option = form.cleaned_data['payment_option']
                billing_address = BillingAddress(
                    user = self.request.user,
                    street_address = street_address,
                    apartment_address = apartment_address,
                    country = country,
                    zip = zip,
                            )
                billing_address.save()
                order.billing_address = billing_address
                order.save()
                # TODO : REDIRECT PAYMENT OPTION
                return redirect('checkout')
        except ObjectDoesNotExist:
            messages.error(self.request, 'You do not have active orders')
            return redirect ('/')
            return redirect('checkout')


class PaymentView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'base/payment.html')

    def post(self, request, *args, **kwargs):
        YOUR_DOMAIN = 'http://127.0.0.1:8000/'
        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    # Provide the exact Price ID (for example, pr_1234) of the product you want to sell
                    'price': 'price_1KUHiVFziaqMNqDNe8NUbrd4',
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url=YOUR_DOMAIN + '/home.html',
            cancel_url=YOUR_DOMAIN + '/inbox.html',
        )

        context = {
            'checkout_session':checkout_session.id,
            'stripe_public_key': settings.STRIPE_PUBLIC_KEY,
        }
        return redirect(checkout_session.url, code=303)