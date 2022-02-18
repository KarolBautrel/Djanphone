from django.shortcuts import render, redirect, get_object_or_404
from .models import Store               
from .forms import StoreForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .filters import ProductFilter
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def stores(request):
    store = Store.objects.get(id=1)
    store2=Store.objects.get(id=2)
    context = {'store':store, 'store2':store2}
    return render(request, 'base/stores.html', context)


def storeInfo(request, pk):
    store = Store.objects.get(id=pk)
    products = store.products.all()
    productFilter = ProductFilter(request.GET, queryset=products)
    products = productFilter.qs
    paginator = Paginator(products, 4)
    page = request.GET.get('page')
    try:
        response = paginator.page(page)
    except PageNotAnInteger:
        response = paginator.page(1)
    except EmptyPage:
        response = paginator.page(paginator.num_pages)
    context = {'store':store, 'response':response, 'productFilter':productFilter}
    return render(request, 'base/store_info.html', context)


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



