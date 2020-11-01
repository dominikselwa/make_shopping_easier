# Generated by Django 3.1.2 on 2020-10-31 21:21

from django.db import migrations


def bool_to_choices(apps, schema_editor):
    Product = apps.get_model('shopping_lists', 'Product')
    for product in Product.objects.all():
        if product.is_in_shopping_list:
            product.place = 0
        else:
            product.place = 1
        product.save()


def choices_to_bool(apps, schema_editor):
    Product = apps.get_model('shopping_lists', 'Product')
    for product in Product.objects.all():
        if product.place == 0:
            product.is_in_shopping_list = True
        else:
            product.is_in_shopping_list = False
        product.save()


class Migration(migrations.Migration):

    dependencies = [
        ('shopping_lists', '0010_product_place'),
    ]

    operations = [
        migrations.RunPython(bool_to_choices, choices_to_bool),
    ]