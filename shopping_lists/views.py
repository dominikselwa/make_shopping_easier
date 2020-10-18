from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render

# Create your views here.
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, ListView, DetailView, DeleteView, UpdateView

from shopping_lists.forms import FridgeModelForm, CategoryModelForm, ShopModelForm, ProductModelForm
from shopping_lists.mixins import UserHasAccessToFridgeMixin
from shopping_lists.models import Fridge, Category, Shop, Product


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
