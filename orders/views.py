from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.http import HttpResponseForbidden
from .models import Order
from .forms import OrderForm
from utils import user_is_admin, user_is_manager, user_is_client, user_is_guest

class OrderListView(ListView):
    model = Order
    template_name = 'orders/order_list.html'
    context_object_name = 'orders'

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        
        is_admin = user_is_admin(user)
        is_manager = user_is_manager(user)
        can_filter = is_admin or is_manager
        
        query = self.request.GET.get('q')
        sort = self.request.GET.get('sort')

        if can_filter and query:
            queryset = queryset.filter(user__icontains=query)

        if can_filter and sort:
            if sort == 'price_asc':
                queryset = queryset.order_by('article__price')
            elif sort == 'price_desc':
                queryset = queryset.order_by('-article__price')
        
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        is_admin = user_is_admin(user)
        is_manager = user_is_manager(user)
        is_client = user_is_client(user)
        is_guest = user_is_guest(user)
        can_filter = is_admin or is_manager
        
        context.update({
            'is_admin': is_admin,
            'is_manager': is_manager,
            'is_client': is_client,
            'is_guest': is_guest,
            'can_filter': can_filter,
            'query': self.request.GET.get('q'),
            'sort': self.request.GET.get('sort'),
        })
        return context

class OrderCreateView(CreateView):
    model = Order
    form_class = OrderForm
    template_name = 'orders/order_form.html'
    success_url = reverse_lazy('order_list')
    extra_context = {'title': 'Создать заказ'}

class OrderUpdateView(UpdateView):
    model = Order
    form_class = OrderForm
    template_name = 'orders/order_form.html'
    success_url = reverse_lazy('order_list')
    extra_context = {'title': 'Редактировать заказ'}

class OrderDeleteView(DeleteView):
    model = Order
    template_name = 'orders/order_confirm_delete.html'
    success_url = reverse_lazy('order_list')
