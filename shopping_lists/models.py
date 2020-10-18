from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.urls import reverse


# class Space(models.Model):
#     name = models.CharField(max_length=32)
#     users = models.ManyToManyField(User)
#
#     def __str__(self):
#         return self.name
#
#     def get_detail_url(self):
#         return reverse('space_detail', kwargs={'pk': self.id})
#
#     def get_edit_url(self):
#         return reverse('space_edit', kwargs={'pk': self.id})
#
#     def get_delete_url(self):
#         return reverse('space_delete', kwargs={'pk': self.id})
#
#     def add_child_url(self):
#         return reverse('fridge_new', kwargs={'pk': self.id})


class Fridge(models.Model):
    name = models.CharField(max_length=32)
    users = models.ManyToManyField(User, related_name='fridges')

    def __str__(self):
        return self.name

    @staticmethod
    def get_create_url():
        return reverse('fridge_create')

    def get_detail_url(self):
        return reverse('fridge_detail', kwargs={'pk': self.id})

    def get_update_url(self):
        return reverse('fridge_update', kwargs={'pk': self.pk})

    def get_delete_url(self):
        return reverse('fridge_delete', kwargs={'pk': self.id})

    # def add_child_url(self):
    #     return reverse('shopping_list_new', kwargs={'pk': self.id, 'space_id': self.space.id})


class Category(models.Model):
    name = models.CharField(max_length=32)
    fridge = models.ForeignKey(Fridge, on_delete=models.CASCADE, related_name='categories')

    class Meta:
        unique_together = ('name', 'fridge')

    def __str__(self):
        return self.name

    def get_unique_error(self):
        return 'Nie można dodać kolejnej kategorii o takiej nazwie'


class Shop(models.Model):
    name = models.CharField(max_length=32)
    fridge = models.ForeignKey(Fridge, on_delete=models.CASCADE, related_name='shops')

    class Meta:
        unique_together = ('name', 'fridge')

    def __str__(self):
        return self.name

    def get_unique_error(self):
        return 'Nie można dodać kolejnego sklepu o takiej nazwie'


class Product(models.Model):
    name = models.CharField(max_length=64)
    fridge = models.ForeignKey(Fridge, on_delete=models.CASCADE, related_name='products')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, related_name='products', null=True)
    avg_time_between_purchases = models.IntegerField(null=True, default=None)
    last_bought = models.DateTimeField(null=True, default=None)
    is_in_fridge = models.BooleanField()
    is_in_shopping_list = models.BooleanField()
    unit = models.CharField(max_length=16, default='')
    quantity = models.FloatField(null=True, default=None)
    shops = models.ManyToManyField(Shop, related_name='products')

    class Meta:
        unique_together = ('name', 'fridge')

    def __str__(self):
        return self.name

    def get_unique_error(self):
        return 'Nie można dodać kolejnego produktu o takiej nazwie'