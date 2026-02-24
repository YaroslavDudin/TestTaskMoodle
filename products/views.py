from django.shortcuts import render
from django.http import HttpResponse
from .models import Product
from .forms import ProductFilter
# Create your views here.

def product_list(request):
    products = Product.objects.all()
    user = request.user
    is_admin = user.is_authenticated and user.groups.filter(name = 'Admin').exists()
    is_manager = user.is_authenticated and user.groups.filter(name = 'Manager').exists()
    is_client = user.is_authenticated and user.groups.filter(name = 'Client').exists()
    is_guest = not user.is_authenticated

    form = ProductFilter(request.GET)  
    
    
    if form.is_valid():
        query = form.cleaned_data.get('query')
        if query:
            products = products.filter(name__icontains=query)
        
        sort = form.cleaned_data.get('sort')
        if sort:
            products = products.order_by(sort)
        

    return render(request , 'products/product_list.html', {
        'user' : user,
        'is_admin' : is_admin,
        'is_manager' : is_manager,
        'is_client' : is_client,
        'is_guest' : is_guest,
        'products' : products,
        'form' : form
        })