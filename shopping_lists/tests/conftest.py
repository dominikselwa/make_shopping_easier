from random import randint, choice, shuffle

import pytest
from django.contrib.auth.models import User
from django.test import Client

from shopping_lists.models import Fridge, Category, Shop, Product


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

            for k in range(5):
                product = Product.objects.create(name=k * 100,
                                                 fridge=fridge,
                                                 category=choice(fridge.categories.all()),
                                                 )
                product.shops.set(fridge.shops.all()[:randint(1, 2)])

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
