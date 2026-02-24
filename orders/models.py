from django.db import models
from products.models import Product
# Create your models here.
class PickUpPoints(models.Model):
    name = models.CharField(max_length = 1000)

    def __str__(self):
        return self.name

class Order(models.Model):
    count = models.IntegerField()
    article = models.ForeignKey(
        Product,
        on_delete = models.CASCADE,
        related_name = 'orders'
    )
    order_date = models.DateField()
    delivery_date = models.DateField()
    adress = models.ForeignKey(
        PickUpPoints,
        on_delete = models.CASCADE,
    )
    user = models.CharField(max_length = 100)
    def __str__(self):
        return f"{self.order_date} ,  Клиент{self.user}"