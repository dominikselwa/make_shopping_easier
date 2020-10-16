# Create your tests here.
from random import choice

import pytest
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse, reverse_lazy

from shopping_lists.models import Space, Fridge, ShoppingList
from shopping_lists.tests.utils import login


def test_index(client):
    response = client.get(reverse('index'))
    assert response.status_code == 200


@pytest.mark.parametrize('url', (
        'main',
        'space_list',
        'space_new',
        'space_detail',
        'space_edit',
        'space_delete',
        'fridge_list',
        'fridge_new',
        'fridge_detail',
        'fridge_edit',
        'fridge_delete',
        'shopping_list_list',
        'shopping_list_new',
        'shopping_list_detail',
        'shopping_list_edit',
        'shopping_list_delete',
))
@pytest.mark.django_db
def test_login_required(client, url):
    response = client.get(reverse('space_list'), follow=True)
    assert response.redirect_chain[0][1] == 302  # [('/accounts/login/?next=/spaces/', 302)]
    assert response.request['PATH_INFO'] == reverse('login')


@pytest.mark.parametrize('url', (
        'space_detail',
        'space_edit',
        'space_delete',
        # 'fridge_list',
        'fridge_new',
))
@pytest.mark.django_db
def test_restrict_access_space(client, set_up, user_without_space, url):
    username, password = user_without_space
    client.login(username=username, password=password)
    space = Space.objects.first()
    response = client.get(reverse(url, kwargs={'pk': space.pk}))
    assert response.status_code == 403


@pytest.mark.parametrize('url', (
        'fridge_detail',
        'fridge_edit',
        'fridge_delete',
        'shopping_list_list',
        'shopping_list_new',
))
@pytest.mark.django_db
def test_restrict_access_fridge(client, set_up, user_without_space, url):
    username, password = user_without_space
    client.login(username=username, password=password)
    fridge = Fridge.objects.first()
    space = fridge.space
    response = client.get(reverse_lazy(url, kwargs={'pk': fridge.pk, 'space_id': space.pk}))
    assert response.status_code == 403


@pytest.mark.parametrize('url', (
        'shopping_list_detail',
        'shopping_list_edit',
        'shopping_list_delete',
))
@pytest.mark.django_db
def test_restrict_access_fridge(client, set_up, user_without_space, url):
    username, password = user_without_space
    client.login(username=username, password=password)
    shopping_list = ShoppingList.objects.first()
    fridge = shopping_list.fridge
    space = fridge.space
    response = client.get(reverse_lazy(url, kwargs={'fridge_id': fridge.pk,
                                                    'space_id': space.pk,
                                                    'pk': shopping_list.pk}))
    assert response.status_code == 403


@pytest.mark.django_db
def test_space_list(client, set_up):
    user = login(client, choice(set_up))
    response = client.get(reverse('space_list'))
    assert response.status_code == 200

    objects = response.context['object_list']
    spaces = user.space_set.all()
    for object in objects:
        assert object in spaces
    assert spaces.count() == len(objects)


@pytest.mark.django_db
def test_space_new(client, set_up):
    user = login(client, choice(set_up))
    spaces_before_creation = user.space_set.all().count()
    name = 'space'

    response = client.post(reverse('space_new'), {'name': name}, follow=True)

    space = Space.objects.get(users=user, name=name)
    assert response.request['PATH_INFO'] == reverse('space_detail', kwargs={'pk': space.pk})
    assert user.space_set.all().count() == spaces_before_creation + 1


@pytest.mark.django_db
def test_space_edit(client, set_up):
    user = login(client, choice(set_up))
    space = user.space_set.first()
    new_name = 'new space name walalalala'

    response = client.post(reverse('space_edit', kwargs={'pk': space.pk}), {'name': new_name}, follow=True)

    assert response.request['PATH_INFO'] == reverse('space_detail', kwargs={'pk': space.pk})
    space = Space.objects.get(pk=space.pk)
    assert space.name == new_name


@pytest.mark.django_db
def test_space_detail(client, set_up):
    user = login(client, choice(set_up))
    space = user.space_set.first()

    response = client.get(reverse('space_detail', kwargs={'pk': space.pk}), follow=True)

    response_space = response.context['object']
    assert space == response_space


@pytest.mark.django_db
def test_space_delete(client, set_up):
    user = login(client, choice(set_up))
    spaces_before_creation = user.space_set.all().count()
    space = user.space_set.first()

    response = client.post(reverse('space_delete', kwargs={'pk': space.pk}), follow=True)

    assert response.request['PATH_INFO'] == reverse('space_list')
    assert spaces_before_creation - 1 == user.space_set.all().count()
    with pytest.raises(ObjectDoesNotExist):
        Space.objects.get(pk=space.pk)


# @pytest.mark.django_db
# def test_fridge_list(client, set_up):
#     user = login(client, choice(set_up))
#     space = user.space_set.first()
#
#     response = client.get(reverse('fridge_list', kwargs={'pk': space.pk}))
#
#     objects = response.context['object_list']
#
#     for object in objects:
#         assert object in space.fridges.all()
#     assert len(objects) == space.fridges.all().count()

@pytest.mark.django_db
def test_fridge_new(client, set_up):
    user = login(client, choice(set_up))
    space = user.space_set.first()
    fridges_before_creation = space.fridges.all().count()
    name = 'new fridge babmbabambama'

    response = client.post(reverse('fridge_new', kwargs={'pk': space.pk}), {'name': name}, follow=True)

    fridge = Fridge.objects.get(space=space, name=name)
    assert response.request['PATH_INFO'] == reverse('fridge_detail', kwargs={'space_id': space.pk, 'pk': fridge.pk})
    assert space.fridges.all().count() == fridges_before_creation + 1
