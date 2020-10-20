# Generated by Django 3.1.2 on 2020-10-20 21:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shopping_lists', '0007_auto_20201019_2219'),
    ]

    operations = [
        migrations.CreateModel(
            name='Invitation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(unique=True)),
                ('is_used', models.IntegerField(default=False)),
                ('fridge', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shopping_lists.fridge')),
            ],
        ),
    ]