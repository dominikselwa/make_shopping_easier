# Generated by Django 3.1.2 on 2020-10-14 18:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shopping_lists', '0002_auto_20201014_1558'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='shoppinglist',
            unique_together={('name', 'fridge')},
        ),
    ]