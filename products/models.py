from django.db import models
from django.core.validators import MaxValueValidator , MinValueValidator
# Create your models here.

class Category (models.Model):
    name = models.CharField(max_length = 100)

    def __str__(self):
        return self.name


class Manufacturer (models.Model):
    name = models.CharField(max_length = 100)

    def __str__(self):
        return self.name


class Supplier (models.Model):
    name = models.CharField(max_length = 100)

    def __str__(self):
        return self.name


class Product(models.Model):
    article = models.CharField(max_length = 100)
    name = models.CharField(max_length = 100)
    unit = models.CharField(max_length = 100)
    price = models.DecimalField(max_digits = 10 , decimal_places = 2)
    supplier = models.ForeignKey(
        Supplier,
        on_delete = models.PROTECT,
        related_name = 'products'
    )
    manufacturer = models.ForeignKey(
        Manufacturer,
        on_delete = models.PROTECT,
        related_name = 'products'
    )
    category = models.ForeignKey(
        Category,
        on_delete = models.PROTECT,
        related_name = 'products'
    )
    discount = models.PositiveIntegerField(default = 0, validators = [MinValueValidator(0),MaxValueValidator(99)])
    quanity = models.IntegerField()
    description = models.TextField(blank = True)
    image = models.ImageField(
        upload_to = 'products',
        blank = True,
        null = True,
    )

    def final_price(self):
        total = 0
        if self.discount > 0:
            total += self.price - (self.price * self.discount / 100)
            return total
        return self.price

    property(final_price)

    def __str__(self):
        return f"Имя товара  -  {self.name} , Имя производителя {self.manufacturer}"


