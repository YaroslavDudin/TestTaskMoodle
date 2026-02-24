from django.shortcuts import render
from .models import Order
# Create your views here.
def order_list(request):
    orders = Order.objects.all()
    user = request.user
    is_admin = user.is_authenticated and user.groups.filter(name = 'Admin').exists()
    is_manager = user.is_authenticated and user.groups.filter(name = 'Manager').exists()
    is_client = user.is_authenticated and user.groups.filter(name = 'Client').exists()
    is_guest = not user.is_authenticated
    return render(request , 'orders/order_list.html',{
        'orders' : orders,
        'user' : user,
        'is_admin' : is_admin,
        'is_manager' : is_manager,
        'is_client' : is_client,
        'is_guest' : is_guest,
        })