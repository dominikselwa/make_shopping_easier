from django.contrib.auth.models import User
from django.db import models


# Create your models here.

class Space(models.Model):
    name = models.CharField(max_length=32)
    users = models.ManyToManyField(User)


class Fridge(models.Model):
    name = models.CharField(max_length=32)
    space = models.ForeignKey(Space, on_delete=models.CASCADE, related_name='fridges')


class ShoppingList(models.Model):
    name = models.CharField(max_length=32)
    fridge = models.ForeignKey(Fridge, on_delete=models.CASCADE, related_name='shopping_lists')


class Category(models.Model):
    name = models.CharField(max_length=32)


class Product(models.Model):
    name = models.CharField(max_length=64)
    space = models.ForeignKey(Space, on_delete=models.CASCADE, related_name='products')
    shopping_list = models.ForeignKey(ShoppingList, on_delete=models.CASCADE, related_name='products')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    avg_time_between_purchases = models.IntegerField(null=True, default=None)
    last_bought = models.DateTimeField(null=True, default=None)
    is_in_fridge = models.BooleanField()
    is_in_shopping_list = models.BooleanField()
    unit = models.CharField(max_length=16, default='')
    quantity = models.FloatField(null=True, default=None)
