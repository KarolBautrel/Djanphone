from django.shortcuts import render, redirect, get_object_or_404
from .models import (Product,
                    Comment,
                    Order,
                    OrderItem,
                    Address,
                    Coupon
                    )
from .forms import CheckoutShippingForm,CheckoutBillingForm, CouponForm                            
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
from django.conf import settings
from django.http import JsonResponse
import json


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
        comments = self.get_object().comment_set.all()
        context['comments'] = comments
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
    if order_qs.exists():
        order = order_qs[0]
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
    print(order_qs)
    print(order_qs)
    if order_qs.exists():
        order = order_qs[0]
        print(order)
        #check if the order item is in the order list
        if order.product.filter(product__slug = product.slug).exists():
            order_item = OrderItem.objects.filter(
                product=product,
                user = request.user, 
                ordered = False
            )[0]
            if order.shipping_address:
                order.shipping_address.delete()
            if order.billing_address:
                order.billing_address.delete()
            order_item.delete()
            if not order.product.all():
                order_qs.delete()
           
            messages.success(request, 'You removed the product from your cart')
            return redirect('order-summary')
        else:
            messages.error(request, 'There is no product to remove')
            return redirect('product-detail', slug=slug)
    else: 
        messages.info(request, 'User doesnt have order')
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
                if order.shipping_address:
                    order.shipping_address.delete()
                if order.billing_address:
                    order.billing_address.delete()
                order_item.delete()
                if not order.product.all():
                    order_qs.delete()
            return redirect('order-summary')
        else:
            messages.info(request, 'There is no product to remove')
            return redirect('product-detail', slug=slug)
    else: 
        messages.info(request, 'User doesnt have order')
        return redirect('order-summary')
    

class OrderSummaryView(View):

    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {'order':order}
            return render(self.request, 'base/order_summary.html', context)
        except ObjectDoesNotExist:
            messages.info(self.request, 'You do not have active orders')
            return redirect ('/')
        

class CheckoutShippingView(View):

    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered = False)
            form = CheckoutShippingForm()
            context = {
                'form': form,
                 'order':order,
                 'couponform':CouponForm(),
                 'DISPLAY_COUPON_FORM': True
                }
            return render(self.request,'base/checkout_shipping.html', context)
        except ObjectDoesNotExist:
            messages.info(self.request, 'You do not have active orders')
            return redirect('home')
        
    def post(self, *args, **kwargs):
        form = CheckoutShippingForm(self.request.POST)
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            if form.is_valid():
                street_address = form.cleaned_data['shipping_city']
                apartment_address = form.cleaned_data['shipping_address']
                country = form.cleaned_data['shipping_country']
                zip = form.cleaned_data['shipping_zip']
                # TO DO, DODAC LOGIKE
                same_billing_address =form.cleaned_data['same_billing_address']
                #save_info = form.cleaned_data['save_info']
                shipping_address_qs = Address.objects.filter(
                    user = self.request.user,
                    street_address = street_address,
                    apartment_address = apartment_address,
                    country = country,
                    zip = zip,
                    address_type = 'Shipping'
                            )
                if shipping_address_qs.exists():
                    order.shipping_address = shipping_address_qs[0]
                    print(order.shipping_address)
                    order.save()
                    if same_billing_address:
                        billing_address_qs = Address.objects.filter(
                                            user = self.request.user,
                                            street_address = street_address,
                                            apartment_address = apartment_address,
                                            country = country,
                                            zip = zip,
                                            address_type = 'Billing'
                                            )
                        if billing_address_qs.exists():
                            order.billing_address = billing_address_qs[0]
                            order.save()
                            return redirect('paypal' )
                    return redirect('billing')
                shipping_address = Address(
                                    user = self.request.user,
                                    street_address = street_address,
                                    apartment_address = apartment_address,
                                    country = country,
                                    zip = zip,
                                    address_type = 'Shipping'
                                    )
                print(shipping_address)
                shipping_address.save()
                order.shipping_address = shipping_address
                order.save()
                if same_billing_address:
                    billing_address = Address(
                                    user = self.request.user,
                                    street_address = street_address,
                                    apartment_address = apartment_address,
                                    country = country,
                                    zip = zip,
                                    address_type = 'Billing'
                                    )
                    billing_address.save()
                    order.billing_address = billing_address
                    order.save()
                    return redirect('paypal' )
                return redirect('billing')
            else:
                messages.info(self.request, 'Please fullfill everything')
                return redirect ('shipping')
        except ObjectDoesNotExist:
            messages.info(self.request, 'You do not have active orders')
            return redirect ('/')


class CheckoutBillingView(View):
    
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered = False)
            if order.shipping_address:
                form = CheckoutBillingForm()
                context = {
                    'form': form,
                    'order':order,
                    'couponform':CouponForm(),
                    'DISPLAY_COUPON_FORM': False
                    }
                return render(self.request,'base/checkout_billing.html', context)
            else:
                return redirect('shipping')
        except ObjectDoesNotExist:
            messages.info(self.request, 'You do not have active orders')
            return redirect('home')
        
    def post(self, *args, **kwargs):
        form = CheckoutBillingForm(self.request.POST)
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            if form.is_valid():
                street_address = form.cleaned_data['billing_city']
                apartment_address = form.cleaned_data['billing_address']
                country = form.cleaned_data['billing_country']
                zip = form.cleaned_data['billing_zip']
                # TO DO, DODAC LOGIKE
                #save_info = form.cleaned_data['save_info']
                billing_address_qs = Address.objects.filter(
                                    user = self.request.user,
                                    street_address = street_address,
                                    apartment_address = apartment_address,
                                    country = country,
                                    zip = zip,
                                    address_type = 'Billing'
                                    )
                if billing_address_qs.exists():
                    order.billing_address = billing_address_qs[0]
                    order.save()
                    return redirect('paypal' )
                billing_address = Address(
                                user = self.request.user,
                                street_address = street_address,
                                apartment_address = apartment_address,
                                country = country,
                                zip = zip,
                                address_type = 'Billing'
                                )
                billing_address.save()
                order.billing_address = billing_address
                order.save()
                return redirect('paypal' )
            else:
                messages.info(self.request, 'Please fullfill everything')
                return redirect('billing')
        except ObjectDoesNotExist:
            messages.info(self.request, 'You do not have active orders')
            return redirect ('/')
            

class PaymentPaypalView(View):

    def get(self, request, *args, **kwargs):
        order = Order.objects.get(user=self.request.user, ordered=False)
        if order.billing_address:
            context = { 
                'order':order,
                'DISPLAY_COUPON_FORM': False,
                }
            return render(request, 'base/paypal.html', context)
        else:
            messages.error(self.request, 'You did not add a billing address ')
            return redirect ('home')


class PaymentSuccessView(View):
    
    def post(self, request, *args, **kwargs):
        order = Order.objects.get(user=self.request.user, ordered = False)
        order_items = OrderItem.objects.filter(user=self.request.user, ordered = False)
        body = json.loads(request.body)
        for product in order_items:
            product.ordered = True
            product.save()
        order.ordered = True   
        order.save()
        return JsonResponse('Payment completed', safe=False)


def get_coupon(request, code):
    try:
        coupon = Coupon.objects.get(code=code)
        return coupon
    except ValueError:
        messages.error(request, "This coupon does not exists")
        return redirect('home')


class AddCouponView(View):
   def post(self, request, *args, **kwargs):
        form = CouponForm(request.POST)
        if form.is_valid():
            try:
                code = form.cleaned_data.get('code')
                order = Order.objects.get(user=request.user, ordered = False)
                order.coupon = get_coupon(request, code)
                order.save()
                messages.success(request, 'Coupon added')
                return redirect('shipping')
            except ObjectDoesNotExist:
                messages.info(request, 'Coupon does not exists')
                return redirect('shipping')
        else: 
            messages.info(request, 'Something went wrong')
            return redirect('shipping')

   