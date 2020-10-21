from random import choice
from secrets import token_urlsafe

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count
from django.http import Http404
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, ListView, DetailView, DeleteView, UpdateView

from shopping_lists.forms import FridgeModelForm, CategoryModelForm, ShopModelForm, ProductModelForm, RecipeModelForm, \
    ProductInRecipeModelForm
from shopping_lists.mixins import UserHasAccessToFridgeMixin
from shopping_lists.models import Fridge, Category, Shop, Product, Recipe, ProductInRecipe, Invitation


class IndexView(View):
    def get(self, request):
        return render(request, 'base.html')


class SingUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'


class MainView(LoginRequiredMixin, View):
    def get(self, request):
        if request.user.fridges.all().count() > 0:
            return redirect(reverse_lazy('fridge_detail', kwargs={'pk': request.user.fridges.all().
                                         annotate(num_products=Count('products')).
                                         order_by('-num_products').first().pk}))
        else:
            return redirect(reverse_lazy('fridge_create'))


class FridgeListView(LoginRequiredMixin, ListView):
    model = Fridge

    def get_queryset(self):
        return self.request.user.fridges.all()


class FridgeCreateView(LoginRequiredMixin, CreateView):
    model = Fridge
    form_class = FridgeModelForm

    def form_valid(self, form):
        self.object = form.save()
        self.object.users.add(self.request.user)
        self.object.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('fridge_detail', kwargs={'pk': self.object.pk})


class FridgeUpdateView(UserHasAccessToFridgeMixin, UpdateView):
    model = Fridge
    form_class = FridgeModelForm

    def get_success_url(self):
        return reverse_lazy('fridge_detail', kwargs={'pk': self.object.pk})


class FridgeDeleteView(UserHasAccessToFridgeMixin, DeleteView):
    model = Fridge
    template_name = 'delete_form.html'
    success_url = reverse_lazy('fridge_list')


class FridgeDetailView(UserHasAccessToFridgeMixin, DetailView):
    model = Fridge

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product_form = ProductModelForm(fridge_id=self.kwargs['pk'])
        category_form = CategoryModelForm(fridge_id=self.kwargs['pk'])
        shop_form = ShopModelForm(fridge_id=self.kwargs['pk'])
        recipe_form = RecipeModelForm(fridge_id=self.kwargs['pk'], user=self.request.user)

        context.update({'product_form': product_form,
                        'category_form': category_form,
                        'shop_form': shop_form,
                        'recipe_form': recipe_form,
                        'product_action': reverse_lazy('product_create', kwargs={'pk': self.kwargs['pk']}),
                        'category_action': reverse_lazy('category_create', kwargs={'pk': self.kwargs['pk']}),
                        'shop_action': reverse_lazy('shop_create', kwargs={'pk': self.kwargs['pk']}),
                        'recipe_action': reverse_lazy('recipe_create', kwargs={'pk': self.kwargs['pk']}),
                        })
        return context


class CategoryCreateView(UserHasAccessToFridgeMixin, CreateView):
    model = Category

    def get_success_url(self):
        return reverse_lazy('fridge_detail', kwargs={'pk': self.kwargs['pk']})

    def get_form(self):
        return CategoryModelForm(fridge_id=self.kwargs['pk'],
                                 **self.get_form_kwargs())


class CategoryUpdateView(UserHasAccessToFridgeMixin, UpdateView):
    model = Category

    def get_success_url(self):
        return reverse_lazy('fridge_detail', kwargs={'pk': self.kwargs['fridge_id']})

    def get_form(self):
        return CategoryModelForm(fridge_id=self.kwargs['fridge_id'],
                                 **self.get_form_kwargs())


class CategoryDeleteView(UserHasAccessToFridgeMixin, DeleteView):
    model = Category
    template_name = 'delete_form.html'

    def get_success_url(self):
        return reverse_lazy('fridge_detail', kwargs={'pk': self.kwargs['fridge_id']})


class ShopCreateView(UserHasAccessToFridgeMixin, CreateView):
    model = Shop

    def get_success_url(self):
        return reverse_lazy('fridge_detail', kwargs={'pk': self.kwargs['pk']})

    def get_form(self):
        return ShopModelForm(fridge_id=self.kwargs['pk'],
                             **self.get_form_kwargs())


class ShopUpdateView(UserHasAccessToFridgeMixin, UpdateView):
    model = Shop

    def get_success_url(self):
        return reverse_lazy('fridge_detail', kwargs={'pk': self.kwargs['fridge_id']})

    def get_form(self):
        return ShopModelForm(fridge_id=self.kwargs['fridge_id'],
                             **self.get_form_kwargs())


class ShopDeleteView(UserHasAccessToFridgeMixin, DeleteView):
    model = Shop
    template_name = 'delete_form.html'

    def get_success_url(self):
        return reverse_lazy('fridge_detail', kwargs={'pk': self.kwargs['fridge_id']})


class ProductCreateView(UserHasAccessToFridgeMixin, CreateView):
    model = Product

    def get_success_url(self):
        return reverse_lazy('fridge_detail', kwargs={'pk': self.kwargs['pk']})

    def get_form(self):
        return ProductModelForm(fridge_id=self.kwargs['pk'],
                                **self.get_form_kwargs())


class ProductUpdateView(UserHasAccessToFridgeMixin, UpdateView):
    model = Product

    def get_success_url(self):
        return reverse_lazy('fridge_detail', kwargs={'pk': self.kwargs['fridge_id']})

    def get_form(self):
        return ProductModelForm(fridge_id=self.kwargs['fridge_id'],
                                **self.get_form_kwargs())


class ProductDeleteView(UserHasAccessToFridgeMixin, DeleteView):
    model = Product
    template_name = 'delete_form.html'

    def get_success_url(self):
        return reverse_lazy('fridge_detail', kwargs={'pk': self.kwargs['fridge_id']})


class ProductsToFridge(UserHasAccessToFridgeMixin, View):
    def post(self, request, pk):
        product_ids = request.POST.getlist('product')
        if product_ids:
            products = Product.objects.filter(id__in=product_ids)
            for product in products:
                product.is_in_shopping_list = False
                product.save()
        return redirect(reverse_lazy('fridge_detail', kwargs={'pk': pk}))


class ProductsToShoppingList(UserHasAccessToFridgeMixin, View):
    def post(self, request, pk):
        product_ids = request.POST.getlist('product')
        if product_ids:
            products = Product.objects.filter(id__in=product_ids)
            for product in products:
                product.is_in_shopping_list = True
                product.save()
        return redirect(reverse_lazy('fridge_detail', kwargs={'pk': pk}))


class RecipeCreateView(UserHasAccessToFridgeMixin, CreateView):
    model = Recipe

    def get_success_url(self):
        return reverse_lazy('recipe_detail', kwargs={'pk': self.object.id, 'fridge_id': self.kwargs['pk']})

    def get_form(self):
        return RecipeModelForm(fridge_id=self.kwargs['pk'],
                               user=self.request.user,
                               **self.get_form_kwargs())


class RecipeDetailView(UserHasAccessToFridgeMixin, DetailView):
    model = Recipe

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'form': ProductInRecipeModelForm(recipe=self.object),
                        'action': reverse_lazy('product_in_recipe_create',
                                               kwargs={'pk': self.kwargs['pk'], 'fridge_id': self.kwargs['fridge_id']}
                                               )})
        return context


class RecipeUpdateView(UserHasAccessToFridgeMixin, UpdateView):
    model = Recipe

    def get_success_url(self):
        return reverse_lazy('recipe_detail', kwargs={'pk': self.object.id, 'fridge_id': self.object.fridge.id})

    def get_form(self):
        return RecipeModelForm(fridge_id=self.kwargs['fridge_id'],
                               user=self.request.user,
                               **self.get_form_kwargs())


class RecipeDeleteView(UserHasAccessToFridgeMixin, DeleteView):
    model = Recipe
    template_name = 'delete_form.html'

    def get_success_url(self):
        return reverse_lazy('fridge_detail', kwargs={'pk': self.kwargs['fridge_id']})


class UserRecipeListView(LoginRequiredMixin, ListView):
    model = Recipe

    def get_queryset(self):
        return self.request.user.recipes.all()


class ProductInRecipeCreateView(UserHasAccessToFridgeMixin, CreateView):
    model = ProductInRecipe

    def get_success_url(self):
        return reverse_lazy('recipe_detail', kwargs={'pk': self.kwargs['pk'],
                                                     'fridge_id': self.kwargs['fridge_id']})

    def get_form(self):
        return ProductInRecipeModelForm(recipe=Recipe.objects.get(pk=self.kwargs['pk']),
                                        **self.get_form_kwargs())


class ProductInRecipeUpdateView(UserHasAccessToFridgeMixin, UpdateView):
    model = ProductInRecipe

    def get_success_url(self):
        return reverse_lazy('recipe_detail', kwargs={'pk': self.object.recipe.pk,
                                                     'fridge_id': self.kwargs['fridge_id']})

    def get_form(self):
        return ProductInRecipeModelForm(**self.get_form_kwargs())


class ProductInRecipeDeleteView(UserHasAccessToFridgeMixin, DeleteView):
    model = ProductInRecipe
    template_name = 'delete_form.html'

    def get_success_url(self):
        return reverse_lazy('recipe_detail', kwargs={'pk': self.object.recipe.pk,
                                                     'fridge_id': self.kwargs['fridge_id']})


class AddRecipeToShoppingListView(UserHasAccessToFridgeMixin, View):
    def get(self, request, fridge_id, pk):
        recipe = Recipe.objects.get(pk=pk)
        for product_in_recipe in recipe.productinrecipe_set.all():
            product = product_in_recipe.product
            if product.is_in_shopping_list:
                if product_in_recipe.quantity_in_recipe is not None:
                    if product.quantity is None:
                        product.quantity = product_in_recipe.quantity_in_recipe
                    else:
                        product.quantity += product_in_recipe.quantity_in_recipe
            else:
                product.is_in_shopping_list = True
                if product_in_recipe.quantity_in_recipe is not None:
                    product.quantity = product_in_recipe.quantity_in_recipe

            product.save()

        return redirect(reverse_lazy('fridge_detail', kwargs={'pk': fridge_id}))


class InvitationCreateView(UserHasAccessToFridgeMixin, View):
    def get(self, request, pk):
        fridge = Fridge.objects.get(pk=pk)

        unique_slug = token_urlsafe(32)
        while Invitation.objects.filter(slug=unique_slug).count() != 0:
            unique_slug = token_urlsafe(32)

        invitation = Invitation.objects.create(slug=unique_slug, fridge=fridge)

        return redirect(reverse_lazy('invitation_show', kwargs={'fridge_id': pk, 'pk': invitation.pk}))


class InvitationShowView(UserHasAccessToFridgeMixin, DetailView):
    model = Invitation


class InvitationAcceptView(LoginRequiredMixin, View):
    def get(self, request, slug):
        try:
            invitation = Invitation.objects.get(slug=slug)
        except ObjectDoesNotExist:
            raise Http404
        fridge = invitation.fridge

        fridge.users.add(request.user)
        invitation.delete()

        return redirect(reverse_lazy('fridge_detail', kwargs={'pk': invitation.fridge.pk}))
