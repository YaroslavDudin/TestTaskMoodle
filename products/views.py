from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Product
from .forms import ProductFilter, ProductForm

def is_admin(user):
    return user.is_authenticated and (user.is_superuser or user.groups.filter(name__iexact='admin').exists())

def is_manager_or_admin(user):
    return user.is_authenticated and (
        user.is_superuser or 
        user.groups.filter(name__iexact='admin').exists() or 
        user.groups.filter(name__iexact='manager').exists()
    )

def product_list(request):
    products = Product.objects.all()
    user = request.user
    
    # Определяем статусы для шаблона
    admin_status = is_admin(user)
    manager_status = user.is_authenticated and user.groups.filter(name__iexact='manager').exists()
    
    is_admin_val = admin_status
    is_manager_val = manager_status
    is_client = user.is_authenticated and user.groups.filter(name__iexact='client').exists()
    is_guest = not user.is_authenticated

    form = ProductFilter(request.GET)  
    if form.is_valid():
        query = form.cleaned_data.get('query')
        if query:
            products = products.filter(name__icontains=query)
        
        sort = form.cleaned_data.get('sort')
        if sort:
            try:
                products = products.order_by(sort)
            except:
                pass

    return render(request, 'products/product_list.html', {
        'user': user,
        'is_admin': is_admin_val,
        'is_manager': is_manager_val,
        'is_client': is_client,
        'is_guest': is_guest,
        'products': products,
        'form': form
    })

@user_passes_test(is_admin, login_url='login')
def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm()
    return render(request, 'products/product_form.html', {'form': form, 'title': 'Добавить товар'})

@user_passes_test(is_admin, login_url='login')
def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm(instance=product)
    return render(request, 'products/product_form.html', {'form': form, 'title': 'Редактировать товар'})

@user_passes_test(is_admin, login_url='login')
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        return redirect('product_list')
    return render(request, 'products/product_confirm_delete.html', {'product': product})
