from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.urls import reverse


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

    def get_products_in_shopping_list(self):
        return self.products.filter(is_in_shopping_list=True)

    def get_products_in_fridge(self):
        return self.products.filter(is_in_shopping_list=False)

    def has_products_without_category(self):
        return self.products.filter(category=None).count() != 0

    def has_products_without_category_in_shopping_list(self):
        return self.get_products_in_shopping_list().filter(category=None).count() != 0

    def has_products_without_category_in_fridge(self):
        return self.get_products_in_fridge().filter(category=None).count() != 0

class Category(models.Model):
    name = models.CharField(max_length=32)
    fridge = models.ForeignKey(Fridge, on_delete=models.CASCADE, related_name='categories')

    class Meta:
        unique_together = ('name', 'fridge')

    def __str__(self):
        return self.name

    def get_unique_error(self):
        return 'Nie można dodać kolejnej kategorii o takiej nazwie'

    def get_create_url(self):
        return reverse('category_create', kwargs={'pk': self.fridge.pk})

    def has_products(self):
        return self.fridge.products.filter(category=self).count() != 0

    def has_products_in_shopping_list(self):
        return self.fridge.products.filter(category=self, is_in_shopping_list=True).count() != 0


class Shop(models.Model):
    name = models.CharField(max_length=32)
    fridge = models.ForeignKey(Fridge, on_delete=models.CASCADE, related_name='shops')

    class Meta:
        unique_together = ('name', 'fridge')

    def __str__(self):
        return self.name

    def get_unique_error(self):
        return 'Nie można dodać kolejnego sklepu o takiej nazwie'

    def get_create_url(self):
        return reverse('shop_create', kwargs={'pk': self.fridge.pk})

    def get_products(self):
        return Product.objects.filter(fridge=self.fridge, is_in_shopping_list=True).filter(
            models.Q(shops=self) | models.Q(shops=None))


class Product(models.Model):
    name = models.CharField(max_length=64)
    fridge = models.ForeignKey(Fridge, on_delete=models.CASCADE, related_name='products')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, related_name='products', null=True)
    avg_time_between_purchases = models.IntegerField(null=True, default=None)
    last_bought = models.DateTimeField(null=True, default=None)
    is_in_fridge = models.BooleanField(default=False)
    is_in_shopping_list = models.BooleanField(default=True)
    unit = models.CharField(max_length=16, default='')
    quantity = models.FloatField(null=True, default=None)
    shops = models.ManyToManyField(Shop, related_name='products')

    class Meta:
        unique_together = ('name', 'fridge')

    def __str__(self):
        quantity_str = ''
        if self.quantity is not None:
            if self.quantity.is_integer():
                quantity_str += f' {int(self.quantity)}'
            else:
                quantity_str += f' {self.quantity}'
        # return_str += f' {self.quantity}' if self.quantity is not None else ''
        quantity_str += f' {self.unit}'
        return f'{self.name}:{quantity_str}' if len(quantity_str) > 1 else self.name

    def get_unique_error(self):
        return 'Nie można dodać kolejnego produktu o takiej nazwie'

    def get_create_url(self):
        return reverse('product_create', kwargs={'pk': self.fridge.pk})

    def get_update_url(self):
        return reverse('product_update', kwargs={'pk': self.pk, 'fridge_id': self.fridge.id})

    def get_delete_url(self):
        return reverse('product_delete', kwargs={'pk': self.id, 'fridge_id': self.fridge.id})
