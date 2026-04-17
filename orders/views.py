from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Order
from .forms import OrderForm

def is_admin(user):
    return user.is_authenticated and (user.is_superuser or user.groups.filter(name__iexact='admin').exists())

def is_manager_or_admin(user):
    return user.is_authenticated and (
        user.is_superuser or 
        user.groups.filter(name__iexact='admin').exists() or 
        user.groups.filter(name__iexact='manager').exists()
    )

@user_passes_test(is_manager_or_admin, login_url='login')
def order_list(request):
    orders = Order.objects.all()
    user = request.user
    
    # Статусы для шаблона
    admin_status = is_admin(user)
    manager_status = user.is_authenticated and user.groups.filter(name__iexact='manager').exists()
    
    is_admin_val = admin_status
    is_manager_val = manager_status
    is_client = user.is_authenticated and user.groups.filter(name__iexact='client').exists()
    is_guest = not user.is_authenticated
    
    return render(request, 'orders/order_list.html', {
        'orders': orders,
        'user': user,
        'is_admin': is_admin_val,
        'is_manager': is_manager_val,
        'is_client': is_client,
        'is_guest': is_guest,
    })

@user_passes_test(is_admin, login_url='login')
def order_create(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('order_list')
    else:
        form = OrderForm()
    return render(request, 'orders/order_form.html', {'form': form, 'title': 'Создать заказ'})

@user_passes_test(is_admin, login_url='login')
def order_update(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('order_list')
    else:
        form = OrderForm(instance=order)
    return render(request, 'orders/order_form.html', {'form': form, 'title': 'Редактировать заказ'})

@user_passes_test(is_admin, login_url='login')
def order_delete(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if request.method == 'POST':
        order.delete()
        return redirect('order_list')
    return render(request, 'orders/order_confirm_delete.html', {'order': order})
