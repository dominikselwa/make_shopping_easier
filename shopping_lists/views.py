from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, ListView, DetailView, DeleteView, UpdateView

from shopping_lists.forms import FridgeModelForm, CategoryModelForm
from shopping_lists.mixins import UserHasAccessToFridgeMixin
from shopping_lists.models import Fridge, Category


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



# class FridgeCreationView(LoginRequiredMixin, View):
#     def get(self, request):
#         form = FridgeModelForm()
#         return render(request, 'shopping_lists/space.html', {'form': form})
#
#     def post(self, request):
#         form = FridgeModelForm(request.POST)
#         if form.is_valid():
#             form.save(commit=False)
#             form.user = request.user
#             if form.is_valid():
#                 form.save()
#                 return redirect('fridge_detail', space_id=pk, pk=fridge.id)
#         return render(request, 'shopping_lists/space.html', {'form': form})


# class SpaceCreateView(LoginRequiredMixin, CreateView):
#
#     def get(self, request):
#         form = SpaceModelForm()
#         return render(request, 'shopping_lists/space.html', {'form': form})
#
#     def post(self, request):
#         form = SpaceModelForm(request.POST)
#         if form.is_valid():
#             space = form.save()
#             space.users.add(request.user)
#             return redirect('space_detail', pk=space.id)
#         return render(request, 'shopping_lists/space.html', {'form': form})
#
#
# class SpaceEditView(UserIsInSpaceMixin, View):
#
#     def get(self, request, pk):
#         space = Space.objects.get(id=pk)
#         form = SpaceModelForm(instance=space)
#         return render(request, 'shopping_lists/space.html', {'form': form})
#
#     def post(self, request, pk):
#         space = Space.objects.get(id=pk)
#         form = SpaceModelForm(request.POST, instance=space)
#         if form.is_valid():
#             space = form.save()
#             space.users.add(request.user)
#             return redirect('space_detail', pk=space.id)
#         return render(request, 'shopping_lists/space.html', {'form': form})
#
#
# class SpaceListView(LoginRequiredMixin, ListView):
#     model = Space
#
#     def get_queryset(self):
#         return Space.objects.filter(users=self.request.user)
#
#
# class SpaceDetailView(UserIsInSpaceMixin, DetailView):
#     model = Space
#
#
# class SpaceDeleteView(UserIsInSpaceMixin, DeleteView):
#     model = Space
#     success_url = reverse_lazy('space_list')
#     template_name = 'delete_form.html'
#
#
# class FridgeCreationView(UserIsInSpaceMixin, CreateView):
#     def get(self, request, pk):
#         form = FridgeForm(space_id=pk)
#         return render(request, 'shopping_lists/space.html', {'form': form})
#
#     def post(self, request, pk):
#         form = FridgeForm(request.POST, space_id=pk)
#         if form.is_valid():
#             fridge = Fridge.objects.create(**form.cleaned_data)
#             return redirect('fridge_detail', space_id=pk, pk=fridge.id)
#         return render(request, 'shopping_lists/space.html', {'form': form})
#
#
# class FridgeEditView(UserIsInSpaceMixin, View):
#     def get(self, request, pk, space_id):
#         fridge = Fridge.objects.get(id=pk)
#         form = FridgeForm(initial={'name': fridge.name})
#         return render(request, 'shopping_lists/space.html', {'form': form})
#
#     def post(self, request, pk, space_id):
#         form = FridgeForm(request.POST, space_id=space_id, fridge_id=pk)
#         if form.is_valid():
#             fridge = Fridge.objects.get(id=pk)
#             fridge.name = form.cleaned_data.get('name')
#             fridge.save()
#             return redirect('fridge_detail', space_id=space_id, pk=pk)
#         return render(request, 'shopping_lists/space.html', {'form': form})
#
#
# class FridgeListView(UserIsInSpaceMixin, ListView):
#     model = Fridge
#
#     def get_queryset(self):
#         return Fridge.objects.filter(space=Space.objects.get(pk=self.kwargs['pk']))
#
#
# class FridgeDetailView(UserIsInSpaceMixin, DetailView):
#     model = Fridge
#
#
# class FridgeDeleteView(UserIsInSpaceMixin, DeleteView):
#     model = Fridge
#     success_url = reverse_lazy('space_list')
#     template_name = 'delete_form.html'
#
#
# class ShoppingListCreationView(UserIsInSpaceMixin, CreateView):
#     def get(self, request, space_id, pk):
#         form = ShoppingListForm(fridge_id=pk)
#         return render(request, 'shopping_lists/space.html', {'form': form})
#
#     def post(self, request, space_id, pk):
#         form = ShoppingListForm(request.POST, fridge_id=pk)
#         if form.is_valid():
#             shopping_list = ShoppingList.objects.create(**form.cleaned_data)
#             return redirect('shopping_list_detail',
#                             pk=shopping_list.pk,
#                             fridge_id=pk,
#                             space_id=space_id)
#         return render(request, 'shopping_lists/space.html', {'form': form})
#
#
# class ShoppingListEditView(UserIsInSpaceMixin, View):
#     def get(self, request, pk, space_id, fridge_id):
#         shopping_list = ShoppingList.objects.get(id=pk)
#         form = ShoppingListForm(initial={'name': shopping_list.name})
#         return render(request, 'shopping_lists/space.html', {'form': form})
#
#     def post(self, request, pk, space_id, fridge_id):
#         form = ShoppingListForm(request.POST, fridge_id=fridge_id, shopping_list_id=pk)
#         if form.is_valid():
#             shopping_list = ShoppingList.objects.get(id=pk)
#             shopping_list.name = form.cleaned_data.get('name')
#             shopping_list.save()
#             return redirect('shopping_list_detail',
#                             pk=pk,
#                             fridge_id=fridge_id,
#                             space_id=space_id)
#         return render(request, 'shopping_lists/space.html', {'form': form})
#
#
# class ShoppingListListView(UserIsInSpaceMixin, ListView):
#     model = ShoppingList
#
#     def get_queryset(self):
#         return ShoppingList.objects.filter(space=Fridge.objects.get(pk=self.kwargs['fridge_id']))
#
#
# class ShoppingListDetailView(UserIsInSpaceMixin, DetailView):
#     model = ShoppingList
#
#
# class ShoppingListDeleteView(UserIsInSpaceMixin, DeleteView):
#     model = ShoppingList
#     success_url = reverse_lazy('space_list')
#     template_name = 'delete_form.html'
#
#
# class CategoryCreationView(UserIsInSpaceMixin, View):
#     def get(self, request, pk):
#         form = CategoryForm(space_id=pk)
#         return render(request, 'shopping_lists/space.html', {'form': form})
#
#     def post(self, request, pk):
#         form = CategoryForm(request.POST, space_id=pk)
#         if form.is_valid():
#             Category.objects.create(**form.cleaned_data)
#             return redirect('space_detail', pk=pk)
#         return render(request, 'shopping_lists/space.html', {'form': form})
#
#
# class CategoryEditView(UserIsInSpaceMixin, View):
#     def get(self, request, pk, space_id):
#         category = Category.objects.get(id=pk)
#         form = CategoryForm(initial={'name': category.name})
#         return render(request, 'shopping_lists/space.html', {'form': form})
#
#     def post(self, request, pk, space_id):
#         form = CategoryForm(request.POST, space_id=space_id, category_id=pk)
#         if form.is_valid():
#             category = Category.objects.get(id=pk)
#             category.name = form.cleaned_data.get('name')
#             category.save()
#             return redirect('space_detail', pk=space_id)
#         return render(request, 'shopping_lists/space.html', {'form': form})
#
#
# class CategoryDeleteView(UserIsInSpaceMixin, DeleteView):
#     model = Category
#     success_url = reverse_lazy('space_list')
#     template_name = 'delete_form.html'
