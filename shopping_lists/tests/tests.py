# Create your tests here.
from random import choice

import pytest
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse, reverse_lazy

from shopping_lists.models import Fridge, Category
from shopping_lists.tests.utils import login

URLS_WITHOUT_AUTH = (
    'index',
)

URLS_LOGIN_REQUIRED = (
    'main',
    'fridge_list',
    'fridge_create',
)

URLS_ACCESS_WITH_PK = (
    'fridge_detail',
    'fridge_update',
    'fridge_delete',
    'category_create',
)

URLS_ACCESS_WITH_FRIDGE_ID = (
    ('category_update', Category),
    ('category_delete', Category),
)


@pytest.mark.parametrize('url', URLS_WITHOUT_AUTH)
def test_index(client, url):
    response = client.get(reverse(url))
    assert response.status_code == 200


@pytest.mark.parametrize('url', URLS_LOGIN_REQUIRED)
@pytest.mark.django_db
def test_login_required(client, set_up, url):
    response = client.get(reverse_lazy(url), follow=True)
    assert response.redirect_chain[0][1] == 302  # [('/accounts/login/?next=/spaces/', 302)]
    assert response.request['PATH_INFO'] == reverse('login')


@pytest.mark.parametrize('url', URLS_ACCESS_WITH_PK)
@pytest.mark.django_db
def test_login_required_with_pk(client, set_up, url):
    fridge = Fridge.objects.first()
    response = client.get(reverse_lazy(url, kwargs={'pk': fridge.pk}), follow=True)
    assert response.redirect_chain[0][1] == 302  # [('/accounts/login/?next=/spaces/', 302)]
    assert response.request['PATH_INFO'] == reverse('login')


@pytest.mark.parametrize('url, model', URLS_ACCESS_WITH_FRIDGE_ID)
@pytest.mark.django_db
def test_login_required_with_fridge_id(client, set_up, url, model):
    fridge = Fridge.objects.first()
    model_instance = model.objects.filter(fridge=fridge).first()
    response = client.get(reverse_lazy(url, kwargs={'pk': model_instance.pk, 'fridge_id': fridge.id}), follow=True)
    assert response.redirect_chain[0][1] == 302
    assert response.request['PATH_INFO'] == reverse('login')


@pytest.mark.parametrize('url', URLS_ACCESS_WITH_PK)
@pytest.mark.django_db
def test_restrict_access_with_pk(client, set_up, user_without_fridge, url):
    client.login(username=user_without_fridge.username, password=user_without_fridge.password)
    fridge = Fridge.objects.first()
    response = client.get(reverse(url, kwargs={'pk': fridge.pk}))
    assert response.status_code == 403


@pytest.mark.parametrize('url, model', URLS_ACCESS_WITH_FRIDGE_ID)
@pytest.mark.django_db
def test_restrict_access_with_fridge_id(client, set_up, user_without_fridge, url, model):
    client.login(username=user_without_fridge.username, password=user_without_fridge.password)
    fridge = Fridge.objects.first()
    model_instance = model.objects.filter(fridge=fridge).first()
    response = client.get(reverse_lazy(url, kwargs={'pk': model_instance.pk, 'fridge_id': fridge.id}), follow=True)
    assert response.status_code == 403


@pytest.mark.django_db
def test_fridge_list(client, set_up):
    user = login(client, choice(set_up))
    response = client.get(reverse('fridge_list'))
    objects = response.context['object_list']

    for object in objects:
        assert object in user.fridges.all()
    assert len(objects) == user.fridges.all().count()


@pytest.mark.django_db
def test_fridge_create(client, set_up):
    user = login(client, choice(set_up))
    fridges_before_creation = user.fridges.all().count()
    name = 'new fridge babmbabambama'

    response = client.post(reverse('fridge_create'), {'name': name}, follow=True)

    fridge = Fridge.objects.get(users=user, name=name)
    assert response.request['PATH_INFO'] == reverse('fridge_detail', kwargs={'pk': fridge.pk})
    assert user.fridges.all().count() == fridges_before_creation + 1


@pytest.mark.django_db
def test_fridge_update(client, set_up):
    user = login(client, choice(set_up))
    fridge = user.fridges.first()
    name = 'new fridge bsakdasnbkaf'

    response = client.post(reverse('fridge_update', kwargs={'pk': fridge.pk}), {'name': name}, follow=True)

    assert response.request['PATH_INFO'] == reverse('fridge_detail', kwargs={'pk': fridge.pk})
    assert Fridge.objects.get(pk=fridge.pk).name == name


@pytest.mark.django_db
def test_fridge_detail(client, set_up):
    user = login(client, choice(set_up))
    fridge = user.fridges.first()

    response = client.get(reverse('fridge_detail', kwargs={'pk': fridge.pk}))

    assert fridge.id == response.context['object'].id


@pytest.mark.django_db
def test_fridge_delete(client, set_up):
    user = login(client, choice(set_up))
    fridges_before_delete = user.fridges.all().count()
    fridge = user.fridges.first()

    response = client.post(reverse('fridge_delete', kwargs={'pk': fridge.pk}), follow=True)

    assert response.request['PATH_INFO'] == reverse('fridge_list')
    assert user.fridges.all().count() == fridges_before_delete - 1
    with pytest.raises(ObjectDoesNotExist):
        Fridge.objects.get(users=user, name=fridge.name)


@pytest.mark.django_db
def test_category_create(client, set_up):
    user = login(client, choice(set_up))
    fridge = user.fridges.first()
    categories_before_create = fridge.categories.all().count()
    name = 'new category'

    response = client.post(reverse('category_create', kwargs={'pk': fridge.pk}), {'name': name}, follow=True)

    Category.objects.get(fridge=fridge, name=name)
    assert response.request['PATH_INFO'] == reverse('fridge_detail', kwargs={'pk': fridge.pk})
    assert fridge.categories.all().count() == categories_before_create + 1


@pytest.mark.django_db
def test_category_update(client, set_up):
    user = login(client, choice(set_up))
    fridge = user.fridges.first()
    category = fridge.categories.first()
    name = 'edited category'

    response = client.post(reverse('category_update', kwargs={'pk': category.pk, 'fridge_id': fridge.id}),
                           {'name': name},
                           follow=True)

    assert response.request['PATH_INFO'] == reverse('fridge_detail', kwargs={'pk': fridge.pk})
    assert Category.objects.get(pk=category.pk, fridge=fridge).name == name


@pytest.mark.django_db
def test_category_delete(client, set_up):
    user = login(client, choice(set_up))
    fridge = user.fridges.first()
    category = fridge.categories.first()
    categories_before_delete = fridge.categories.all().count()

    response = client.post(reverse('category_delete', kwargs={'pk': category.pk, 'fridge_id': fridge.id}), follow=True)

    assert response.request['PATH_INFO'] == reverse('fridge_detail', kwargs={'pk': fridge.pk})
    assert fridge.categories.all().count() == categories_before_delete - 1
    with pytest.raises(ObjectDoesNotExist):
        Category.objects.get(pk=category.pk, fridge=fridge)
