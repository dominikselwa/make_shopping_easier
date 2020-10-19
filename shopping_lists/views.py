from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, ListView, DetailView, DeleteView, UpdateView

from shopping_lists.forms import FridgeModelForm, CategoryModelForm, ShopModelForm, ProductModelForm, RecipeModelForm, \
    ProductInRecipeModelForm
from shopping_lists.mixins import UserHasAccessToFridgeMixin
from shopping_lists.models import Fridge, Category, Shop, Product, Recipe, ProductInRecipe


class IndexView(View):
    def get(self, request):
        return render(request, 'base.html')


class SingUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'


class MainView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'shopping_lists/main.html')


class FridgeListView(LoginRequiredMixin, ListView):
    model = Fridge

    def get_queryset(self):
        return self.request.user.fridges.all()


class FridgeCreateView(LoginRequiredMixin, CreateView):
    model = Fridge
    form_class = FridgeModelForm
    template_name = 'shopping_lists/space.html'

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
    template_name = 'shopping_lists/space.html'

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
    template_name = 'shopping_lists/space.html'

    def get_success_url(self):
        return reverse_lazy('fridge_detail', kwargs={'pk': self.kwargs['pk']})

    def get_form(self):
        return CategoryModelForm(fridge_id=self.kwargs['pk'],
                                 **self.get_form_kwargs())


class CategoryUpdateView(UserHasAccessToFridgeMixin, UpdateView):
    model = Category
    template_name = 'shopping_lists/space.html'

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
    template_name = 'shopping_lists/space.html'

    def get_success_url(self):
        return reverse_lazy('fridge_detail', kwargs={'pk': self.kwargs['pk']})

    def get_form(self):
        return ShopModelForm(fridge_id=self.kwargs['pk'],
                             **self.get_form_kwargs())


class ShopUpdateView(UserHasAccessToFridgeMixin, UpdateView):
    model = Shop
    template_name = 'shopping_lists/space.html'

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
    template_name = 'shopping_lists/product.html'

    def get_success_url(self):
        return reverse_lazy('fridge_detail', kwargs={'pk': self.kwargs['pk']})

    def get_form(self):
        return ProductModelForm(fridge_id=self.kwargs['pk'],
                                **self.get_form_kwargs())


class ProductUpdateView(UserHasAccessToFridgeMixin, UpdateView):
    model = Product
    template_name = 'shopping_lists/product.html'

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
    template_name = 'shopping_lists/space.html'

    def get_success_url(self):
        return reverse_lazy('recipe_detail', kwargs={'pk': self.object.id, 'fridge_id': self.kwargs['pk']})

    def get_form(self):
        return RecipeModelForm(fridge_id=self.kwargs['pk'],
                               user=self.request.user,
                               **self.get_form_kwargs())


class RecipeDetailView(UserHasAccessToFridgeMixin, DetailView):
    model = Recipe
    # template_name = 'shopping_lists/recipe.html'

    # def get_success_url(self):
    #     return reverse_lazy('recipe_detail', kwargs={'pk': self.kwargs['pk'], 'fridge_id': self.kwargs['fridge_id']})

    # def get_form(self):
    #     return ProductInRecipeModelForm(recipe=Recipe.objects.get(pk=self.kwargs['pk']),
    #                                     **self.get_form_kwargs())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'object': Recipe.objects.get(pk=self.kwargs['pk'])})
        return context


class RecipeUpdateView(UserHasAccessToFridgeMixin, UpdateView):
    model = Recipe
    template_name = 'shopping_lists/space.html'

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