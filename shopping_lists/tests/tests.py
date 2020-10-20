# Create your tests here.
from random import choice, random

import pytest
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse, reverse_lazy

from shopping_lists.models import Fridge, Category, Shop, Product, Recipe, ProductInRecipe
from shopping_lists.tests.utils import login

URLS_WITHOUT_AUTH = (
    'index',
)

URLS_LOGIN_REQUIRED = (
    'main',
    'fridge_list',
    'fridge_create',
    'recipe_list',
)

URLS_ACCESS_WITH_PK = (
    'fridge_detail',
    'fridge_update',
    'fridge_delete',
    'category_create',
    'shop_create',
    'product_create',
    'products_to_fridge',
    'products_to_shopping_list',
    'recipe_create',
)

URLS_ACCESS_WITH_FRIDGE_ID = (
    ('category_update', Fridge),
    ('category_delete', Fridge),
    ('shop_update', Fridge),
    ('shop_delete', Fridge),
    ('product_update', Fridge),
    ('product_delete', Fridge),
    ('recipe_detail', Fridge),
    ('recipe_update', Fridge),
    ('recipe_delete', Fridge),
    ('product_in_recipe_create', Fridge),
    ('product_in_recipe_update', Recipe),
    ('product_in_recipe_delete', Recipe),
    ('add_recipe_to_shopping_list', Fridge),
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
    assert response.redirect_chain[0][1] == 302
    assert response.request['PATH_INFO'] == reverse('login')


@pytest.mark.parametrize('url, parent_model', URLS_ACCESS_WITH_FRIDGE_ID)
@pytest.mark.django_db
def test_login_required_with_fridge_id(client, set_up, url, parent_model):
    parent_model_instance = parent_model.objects.first()
    fridge_id = parent_model_instance.id if parent_model == Fridge else parent_model_instance.fridge.id
    response = client.get(reverse_lazy(url, kwargs={'pk': 1, 'fridge_id': fridge_id}), follow=True)
    assert response.redirect_chain[0][1] == 302
    assert response.request['PATH_INFO'] == reverse('login')


@pytest.mark.parametrize('url', URLS_ACCESS_WITH_PK)
@pytest.mark.django_db
def test_restrict_access_with_pk(client, set_up, user_without_fridge, url):
    client.login(username=user_without_fridge.username, password=user_without_fridge.password)
    fridge = Fridge.objects.first()
    response = client.get(reverse(url, kwargs={'pk': fridge.pk}))
    assert response.status_code == 403


@pytest.mark.parametrize('url, parent_model', URLS_ACCESS_WITH_FRIDGE_ID)
@pytest.mark.django_db
def test_restrict_access_with_fridge_id(client, set_up, user_without_fridge, url, parent_model):
    client.login(username=user_without_fridge.username, password=user_without_fridge.password)
    parent_model_instance = parent_model.objects.first()
    fridge_id = parent_model_instance.id if parent_model == Fridge else parent_model_instance.fridge.id
    response = client.get(reverse_lazy(url, kwargs={'pk': 1, 'fridge_id': fridge_id}), follow=True)
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


@pytest.mark.django_db
def test_shop_create(client, set_up):
    user = login(client, choice(set_up))
    fridge = user.fridges.first()
    shops_before_create = fridge.shops.all().count()
    name = 'new shop'

    response = client.post(reverse('shop_create', kwargs={'pk': fridge.pk}), {'name': name}, follow=True)

    Shop.objects.get(fridge=fridge, name=name)
    assert response.request['PATH_INFO'] == reverse('fridge_detail', kwargs={'pk': fridge.pk})
    assert fridge.shops.all().count() == shops_before_create + 1


@pytest.mark.django_db
def test_shop_update(client, set_up):
    user = login(client, choice(set_up))
    fridge = user.fridges.first()
    shop = fridge.shops.first()
    name = 'edited shop'

    response = client.post(reverse('shop_update', kwargs={'pk': shop.pk, 'fridge_id': fridge.id}),
                           {'name': name},
                           follow=True)

    assert response.request['PATH_INFO'] == reverse('fridge_detail', kwargs={'pk': fridge.pk})
    assert Shop.objects.get(pk=shop.pk, fridge=fridge).name == name


@pytest.mark.django_db
def test_shop_delete(client, set_up):
    user = login(client, choice(set_up))
    fridge = user.fridges.first()
    shop = fridge.shops.first()
    shops_before_delete = fridge.shops.all().count()

    response = client.post(reverse('shop_delete', kwargs={'pk': shop.pk, 'fridge_id': fridge.id}), follow=True)

    assert response.request['PATH_INFO'] == reverse('fridge_detail', kwargs={'pk': fridge.pk})
    assert fridge.shops.all().count() == shops_before_delete - 1
    with pytest.raises(ObjectDoesNotExist):
        Shop.objects.get(pk=shop.pk, fridge=fridge)


@pytest.mark.django_db
def test_product_create_min_fields(client, set_up):
    user = login(client, choice(set_up))
    fridge = user.fridges.first()
    products_before_create = fridge.products.all().count()
    name = 'new product'

    response = client.post(reverse('product_create', kwargs={'pk': fridge.pk}), {'name': name}, follow=True)

    Product.objects.get(fridge=fridge, name=name)
    assert response.request['PATH_INFO'] == reverse('fridge_detail', kwargs={'pk': fridge.pk})
    assert fridge.products.all().count() == products_before_create + 1


@pytest.mark.django_db
def test_product_create_all_fields(client, set_up):
    user = login(client, choice(set_up))
    fridge = user.fridges.first()
    products_before_create = fridge.products.all().count()
    shops = fridge.shops.all()
    data = {
        'name': 'new product',
        'quantity': 5,
        'unit': 'new unit',
        'category': fridge.categories.first().pk,
        'shops': [shop.pk for shop in shops],
        'is_in_shopping_list': False,
    }

    response = client.post(reverse('product_create', kwargs={'pk': fridge.pk}), data, follow=True)

    data.pop('shops')
    product = Product.objects.get(**data)
    for shop in shops:
        assert shop in product.shops.all()
    assert len(shops) == product.shops.all().count()
    assert response.request['PATH_INFO'] == reverse('fridge_detail', kwargs={'pk': fridge.pk})
    assert fridge.products.all().count() == products_before_create + 1


@pytest.mark.django_db
def test_product_update(client, set_up):
    user = login(client, choice(set_up))
    fridge = user.fridges.first()
    product = fridge.products.first()
    name = 'edited product'

    response = client.post(reverse('product_update', kwargs={'pk': product.pk, 'fridge_id': fridge.id}),
                           {'name': name},
                           follow=True)

    assert response.request['PATH_INFO'] == reverse('fridge_detail', kwargs={'pk': fridge.pk})
    assert Product.objects.get(pk=product.pk, fridge=fridge).name == name


@pytest.mark.django_db
def test_product_update_all_fields(client, set_up):
    user = login(client, choice(set_up))
    fridge = user.fridges.first()
    product = fridge.products.first()
    shops = fridge.shops.all()
    data = {
        'name': 'edited product',
        'quantity': 8,
        'unit': 'edited unit',
        'category': fridge.categories.first().pk,
        'shops': [shop.pk for shop in shops],
        'is_in_shopping_list': False,
    }

    response = client.post(reverse('product_update', kwargs={'pk': product.pk, 'fridge_id': fridge.id}),
                           data,
                           follow=True)

    data.pop('shops')
    product = Product.objects.get(pk=product.pk, **data)
    for shop in shops:
        assert shop in product.shops.all()
    assert len(shops) == product.shops.all().count()
    assert response.request['PATH_INFO'] == reverse('fridge_detail', kwargs={'pk': fridge.pk})


@pytest.mark.django_db
def test_product_delete(client, set_up):
    user = login(client, choice(set_up))
    fridge = user.fridges.first()
    product = fridge.products.first()
    products_before_delete = fridge.products.all().count()

    response = client.post(reverse('product_delete', kwargs={'pk': product.pk, 'fridge_id': fridge.id}), follow=True)

    assert response.request['PATH_INFO'] == reverse('fridge_detail', kwargs={'pk': fridge.pk})
    assert fridge.products.all().count() == products_before_delete - 1
    with pytest.raises(ObjectDoesNotExist):
        Product.objects.get(pk=product.pk, fridge=fridge)


@pytest.mark.django_db
def test_products_to_fridge(client, set_up):
    user = login(client, choice(set_up))
    fridge = user.fridges.first()
    products = fridge.products.filter(is_in_shopping_list=True)
    products_in_shopping_list_before = products.count()

    response = client.post(reverse('products_to_fridge', kwargs={'pk': fridge.pk}),
                           {'product': [product.id for product in products]},
                           follow=True)

    assert response.request['PATH_INFO'] == reverse('fridge_detail', kwargs={'pk': fridge.pk})
    assert fridge.products.filter(is_in_shopping_list=True).count() == 0 != products_in_shopping_list_before


@pytest.mark.django_db
def test_products_to_shopping_fridge(client, set_up):
    user = login(client, choice(set_up))
    fridge = user.fridges.first()
    products = fridge.products.filter(is_in_shopping_list=False)
    products_in_shopping_list_before = products.count()

    response = client.post(reverse('products_to_shopping_list', kwargs={'pk': fridge.pk}),
                           {'product': [product.id for product in products]},
                           follow=True)

    assert response.request['PATH_INFO'] == reverse('fridge_detail', kwargs={'pk': fridge.pk})
    assert fridge.products.filter(is_in_shopping_list=False).count() == 0 != products_in_shopping_list_before


@pytest.mark.django_db
def test_recipe_list(client, set_up):
    user = login(client, choice(set_up))
    response = client.get(reverse('recipe_list'))
    objects = response.context['object_list']

    for object in objects:
        assert object in user.recipes.all()
    assert len(objects) == user.recipes.all().count()


@pytest.mark.django_db
def test_recipe_detail(client, set_up):
    user = login(client, choice(set_up))
    recipe = user.recipes.first()

    response = client.get(reverse('recipe_detail', kwargs={'pk': recipe.pk, 'fridge_id': recipe.fridge.id}))

    assert recipe.id == response.context['object'].id


@pytest.mark.django_db
def test_recipe_create(client, set_up):
    user = login(client, choice(set_up))
    fridge = user.fridges.first()
    recipes_before_create = fridge.recipes.all().count()
    name = 'new recipe'

    response = client.post(reverse('recipe_create', kwargs={'pk': fridge.pk}), {'name': name}, follow=True)

    recipe = Recipe.objects.get(fridge=fridge, name=name, owner=user)
    assert response.request['PATH_INFO'] == reverse('recipe_detail',
                                                    kwargs={'pk': recipe.pk, 'fridge_id': recipe.fridge.id})
    assert fridge.recipes.all().count() == recipes_before_create + 1


@pytest.mark.django_db
def test_recipe_update(client, set_up):
    user = login(client, choice(set_up))
    recipe = user.recipes.first()
    fridge = recipe.fridge
    name = 'edited recipe'

    response = client.post(reverse('recipe_update', kwargs={'pk': recipe.pk, 'fridge_id': fridge.id}),
                           {'name': name},
                           follow=True)

    assert response.request['PATH_INFO'] == reverse('recipe_detail',
                                                    kwargs={'pk': recipe.pk, 'fridge_id': recipe.fridge.id})
    assert Recipe.objects.get(pk=recipe.pk, fridge=recipe.fridge, owner=user).name == name


@pytest.mark.django_db
def test_recipe_delete(client, set_up):
    user = login(client, choice(set_up))
    recipe = user.recipes.first()
    recipes_before_delete = user.recipes.all().count()

    response = client.post(reverse('recipe_delete',
                                   kwargs={'pk': recipe.pk, 'fridge_id': recipe.fridge.id}), follow=True)

    assert response.request['PATH_INFO'] == reverse('fridge_detail', kwargs={'pk': recipe.fridge.pk})
    assert user.recipes.all().count() == recipes_before_delete - 1
    with pytest.raises(ObjectDoesNotExist):
        Recipe.objects.get(pk=recipe.pk, fridge=recipe.fridge)


@pytest.mark.django_db
def test_product_in_recipe_create_max(client, set_up):
    user = login(client, choice(set_up))
    recipe = user.recipes.first()
    product_in_recipes_before_create = recipe.productinrecipe_set.all().count()
    product = choice(recipe.fridge.products.all())
    quantity = 20

    response = client.post(reverse('product_in_recipe_create',
                                   kwargs={'pk': recipe.pk, 'fridge_id': recipe.fridge.pk}),
                           {'product': product.id, 'quantity_in_recipe': quantity},
                           follow=True)

    assert response.request['PATH_INFO'] == reverse('recipe_detail',
                                                    kwargs={'pk': recipe.pk,
                                                            'fridge_id': recipe.fridge.id})
    assert recipe.productinrecipe_set.all().count() == product_in_recipes_before_create + 1


@pytest.mark.django_db
def test_product_in_recipe_create_min(client, set_up):
    user = login(client, choice(set_up))
    recipe = user.recipes.first()
    product_in_recipes_before_create = recipe.productinrecipe_set.all().count()
    product = choice(recipe.fridge.products.all())

    response = client.post(reverse('product_in_recipe_create',
                                   kwargs={'pk': recipe.pk, 'fridge_id': recipe.fridge.pk}),
                           {'product': product.id},
                           follow=True)

    assert response.request['PATH_INFO'] == reverse('recipe_detail',
                                                    kwargs={'pk': recipe.pk,
                                                            'fridge_id': recipe.fridge.id})
    assert recipe.productinrecipe_set.all().count() == product_in_recipes_before_create + 1


@pytest.mark.django_db
def test_product_in_recipe_update_max(client, set_up):
    user = login(client, choice(set_up))
    recipe = user.recipes.first()
    product_in_recipe = recipe.productinrecipe_set.first()
    product = choice(recipe.fridge.products.all())
    quantity = 20

    response = client.post(reverse('product_in_recipe_update',
                                   kwargs={'pk': product_in_recipe.pk, 'fridge_id': recipe.fridge.pk}),
                           {'product': product.id, 'quantity_in_recipe': quantity},
                           follow=True)

    assert response.request['PATH_INFO'] == reverse('recipe_detail',
                                                    kwargs={'pk': recipe.pk,
                                                            'fridge_id': recipe.fridge.id})
    ProductInRecipe.objects.get(pk=product_in_recipe.pk, recipe=recipe, product=product, quantity_in_recipe=quantity)


@pytest.mark.django_db
def test_product_in_recipe_update_min(client, set_up):
    user = login(client, choice(set_up))
    recipe = user.recipes.first()
    product_in_recipe = recipe.productinrecipe_set.first()
    product = choice(recipe.fridge.products.all())

    response = client.post(reverse('product_in_recipe_update',
                                   kwargs={'pk': product_in_recipe.pk, 'fridge_id': recipe.fridge.pk}),
                           {'product': product.id},
                           follow=True)

    assert response.request['PATH_INFO'] == reverse('recipe_detail',
                                                    kwargs={'pk': recipe.pk,
                                                            'fridge_id': recipe.fridge.id})
    ProductInRecipe.objects.get(pk=product_in_recipe.pk,
                                recipe=recipe,
                                product=product,
                                quantity_in_recipe=product_in_recipe.quantity_in_recipe)


@pytest.mark.django_db
def test_product_in_recipe_delete(client, set_up):
    user = login(client, choice(set_up))
    recipe = user.recipes.first()
    product_in_recipes_before_delete = recipe.productinrecipe_set.all().count()
    product_in_recipe = recipe.productinrecipe_set.first()

    response = client.post(reverse('product_in_recipe_delete',
                                   kwargs={'pk': product_in_recipe.pk, 'fridge_id': recipe.fridge.pk}),
                           follow=True)

    assert response.request['PATH_INFO'] == reverse('recipe_detail',
                                                    kwargs={'pk': recipe.pk,
                                                            'fridge_id': recipe.fridge.id})
    assert recipe.productinrecipe_set.all().count() == product_in_recipes_before_delete - 1
    with pytest.raises(ObjectDoesNotExist):
        ProductInRecipe.objects.get(pk=product_in_recipe.pk)


@pytest.mark.parametrize(
    'is_in_shopping_list, product_quantity_before_adding, quantity_in_recipe, resulting_product_quantity',
    ((True, None, None, None),
     (True, 3, None, 3),
     (True, None, 4, 4),
     (True, 3, 4, 7),
     (False, None, None, None),
     (False, 3, None, 3),
     (False, None, 4, 4),
     (False, 3, 4, 4),
     ))
@pytest.mark.django_db
def test_add_recipe_to_shopping_list(client, set_up, is_in_shopping_list, product_quantity_before_adding,
                                     quantity_in_recipe, resulting_product_quantity):
    user = login(client, choice(set_up))
    recipe = user.recipes.first()
    product_in_recipe = recipe.productinrecipe_set.first()
    product = product_in_recipe.product

    recipe.productinrecipe_set.exclude(pk=product_in_recipe.pk).delete()

    product.is_in_shopping_list = is_in_shopping_list
    product.quantity = product_quantity_before_adding
    product.save()

    product_in_recipe.quantity_in_recipe = quantity_in_recipe
    product_in_recipe.save()

    response = client.get(reverse('add_recipe_to_shopping_list',
                                  kwargs={'pk': recipe.pk, 'fridge_id': recipe.fridge.id}),
                          follow=True)

    assert response.request['PATH_INFO'] == reverse('fridge_detail',
                                                    kwargs={'pk': recipe.fridge.id})
    assert Product.objects.get(pk=product.pk).quantity == resulting_product_quantity
