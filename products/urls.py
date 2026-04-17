from django.urls import path
from .views import *

urlpatterns = [
    path('', product_list, name='product_list'),
    path('create/', product_create, name='product_create'),
    path('<int:pk>/update/', product_update, name='product_update'),
    path('<int:pk>/delete/', product_delete, name='product_delete'),
]
