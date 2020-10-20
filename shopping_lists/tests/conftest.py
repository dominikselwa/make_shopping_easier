from random import randint, choice, shuffle, random
from secrets import token_urlsafe

import pytest
from django.contrib.auth.models import User
from django.test import Client

from shopping_lists.models import Fridge, Category, Shop, Product, Recipe, ProductInRecipe, Invitation


@pytest.fixture
def client():
    return Client()


@pytest.fixture
def set_up():
    users = []
    for i in range(3):
        u = User.objects.create(username=f'User{i}')
        users.append(u)

    for user in users:
        for i in range(2):
            fridge = Fridge.objects.create(name=str(i))
            fridge.users.add(user)

            for j in range(2):
                Category.objects.create(name=j, fridge=fridge)
                Shop.objects.create(name=j * 10 + 1, fridge=fridge)
                Recipe.objects.create(name=f'recipe {(j + 1) * 10 + 2}', fridge=fridge, owner=user)

                unique_slug = token_urlsafe(32)
                while Invitation.objects.filter(slug=unique_slug).count() != 0:
                    unique_slug = token_urlsafe(32)

                Invitation.objects.create(slug=unique_slug, fridge=fridge)

            for k in range(5):
                product = Product.objects.create(name=k * 100,
                                                 fridge=fridge,
                                                 category=choice(fridge.categories.all()),
                                                 is_in_shopping_list=k % 2 == 0,
                                                 )
                product.shops.set(fridge.shops.all()[:randint(1, 2)])

            for recipe in fridge.recipes.all():
                for _ in range(3):
                    product = choice(fridge.products.all())
                    quantity = choice((random(), None))
                    ProductInRecipe.objects.create(product=product, quantity_in_recipe=quantity, recipe=recipe)

    return users


@pytest.fixture
def user_without_fridge():
    class FakeUser:
        password = 'password'
        username = 'username'

    user = User.objects.create(username=FakeUser.username)
    user.set_password(FakeUser.password)
    user.save()
    return FakeUser
