from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.http import HttpResponseForbidden
from .models import Product
from .forms import ProductForm, ProductFilter
from utils import user_is_admin, user_is_manager, user_is_client, user_is_guest

class ProductListView(ListView):
    model = Product
    template_name = 'products/product_list.html'
    context_object_name = 'products'

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        
        is_admin = user_is_admin(user)
        is_manager = user_is_manager(user)
        can_filter = is_admin or is_manager
        
        self.filter_form = ProductFilter(self.request.GET)
        
        if can_filter and self.filter_form.is_valid():
            query = self.filter_form.cleaned_data.get('query')
            sort = self.filter_form.cleaned_data.get('sort')

            if query:
                queryset = queryset.filter(name__icontains=query)

            if sort:
                if sort == 'final_price':
                    queryset = queryset.order_by('price') 
                elif sort == '-final_price':
                    queryset = queryset.order_by('-price')
        
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
            'form': getattr(self, 'filter_form', ProductFilter(self.request.GET)),
        })
        return context

class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'products/product_form.html'
    success_url = reverse_lazy('product_list')

class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'products/product_form.html'
    success_url = reverse_lazy('product_list')

class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'products/product_confirm_delete.html'
    success_url = reverse_lazy('product_list')
