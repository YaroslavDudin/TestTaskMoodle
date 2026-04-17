from django.urls import path
from .views import *

urlpatterns = [
    path('', order_list, name='order_list'),
    path('create/', order_create, name='order_create'),
    path('<int:pk>/update/', order_update, name='order_update'),
    path('<int:pk>/delete/', order_delete, name='order_delete'),
]
