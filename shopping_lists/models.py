from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.urls import reverse
from django.utils.text import slugify


class Space(models.Model):
    name = models.CharField(max_length=32)
    users = models.ManyToManyField(User)

    def __str__(self):
        return self.name

    def get_detail_url(self):
        return reverse('space_detail', kwargs={'pk': self.id})

    def get_edit_url(self):
        return reverse('space_edit', kwargs={'pk': self.id})

    def get_delete_url(self):
        return reverse('space_delete', kwargs={'pk': self.id})

    def add_child_url(self):
        return reverse('fridge_new', kwargs={'pk': self.id})


class Fridge(models.Model):
    name = models.CharField(max_length=32)
    space = models.ForeignKey(Space, on_delete=models.CASCADE, related_name='fridges')

    class Meta:
        unique_together = ('name', 'space')

    def __str__(self):
        return self.name

    def get_detail_url(self):
        return reverse('fridge_detail', kwargs={'pk': self.id, 'space_id': self.space.id})

    def get_edit_url(self):
        return reverse('fridge_edit', kwargs={'pk': self.id, 'space_id': self.space.id})

    def get_delete_url(self):
        return reverse('fridge_delete', kwargs={'pk': self.id, 'space_id': self.space.id})

    def add_child_url(self):
        return reverse('shopping_list_new', kwargs={'pk': self.id, 'space_id': self.space.id})


class ShoppingList(models.Model):
    name = models.CharField(max_length=32)
    fridge = models.ForeignKey(Fridge, on_delete=models.CASCADE, related_name='shopping_lists')

    class Meta:
        unique_together = ('name', 'fridge')

    def __str__(self):
        return self.name

    def get_detail_url(self):
        return reverse('shopping_list_detail', kwargs={'pk': self.id,
                                                'space_id': self.fridge.space.id,
                                                'fridge_id': self.fridge.id})

    def get_edit_url(self):
        return reverse('shopping_list_edit', kwargs={'pk': self.id,
                                              'space_id': self.fridge.space.id,
                                              'fridge_id': self.fridge.id})

    def get_delete_url(self):
        return reverse('shopping_list_delete', kwargs={'pk': self.id,
                                                'space_id': self.fridge.space.id,
                                                'fridge_id': self.fridge.id})


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
