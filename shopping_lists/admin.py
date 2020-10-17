from django.contrib import admin

# Register your models here.
from shopping_lists import models

admin.site.register(models.Fridge)
admin.site.register(models.Category)
admin.site.register(models.Shop)
admin.site.register(models.Product)
