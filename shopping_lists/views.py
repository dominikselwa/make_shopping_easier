from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import ObjectDoesNotExist
from django.db import OperationalError
from django.http import HttpResponseForbidden, Http404
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, ListView, DetailView, DeleteView

from shopping_lists.forms import SpaceModelForm, FridgeForm, ShoppingListForm
from shopping_lists.models import Space, Fridge, ShoppingList


class UserIsInSpacePkMixin(UserPassesTestMixin):
    def test_func(self):
        if self.kwargs.get('pk') is not None:
            try:
                return self.request.user in Space.objects.get(pk=self.kwargs['pk']).users.all()
            except ObjectDoesNotExist:
                raise Http404


class UserIsInSpaceIdMixin(UserPassesTestMixin):
    def test_func(self):
        if self.kwargs.get('space_id') is not None:
            try:
                return self.request.user in Space.objects.get(pk=self.kwargs['space_id']).users.all()
            except ObjectDoesNotExist:
                raise Http404



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


class SpaceCreateView(LoginRequiredMixin, CreateView):

    def get(self, request):
        form = SpaceModelForm()
        return render(request, 'shopping_lists/space.html', {'form': form})

    def post(self, request):
        form = SpaceModelForm(request.POST)
        if form.is_valid():
            space = form.save()
            space.users.add(request.user)
            return redirect('space_detail', pk=space.id)
        return render(request, 'shopping_lists/space.html', {'form': form})


class SpaceEditView(UserIsInSpacePkMixin, View):

    def get(self, request, pk):
        space = Space.objects.get(id=pk)
        form = SpaceModelForm(instance=space)
        return render(request, 'shopping_lists/space.html', {'form': form})

    def post(self, request, pk):
        space = Space.objects.get(id=pk)
        form = SpaceModelForm(request.POST, instance=space)
        if form.is_valid():
            space = form.save()
            space.users.add(request.user)
            return redirect('space_detail', pk=space.id)
        return render(request, 'shopping_lists/space.html', {'form': form})


class SpaceListView(LoginRequiredMixin, ListView):
    model = Space

    def get_queryset(self):
        return Space.objects.filter(users=self.request.user)


class SpaceDetailView(UserIsInSpacePkMixin, DetailView):
    model = Space


class SpaceDeleteView(UserIsInSpacePkMixin, DeleteView):
    model = Space
    success_url = reverse_lazy('space_list')
    template_name = 'delete_form.html'


class FridgeCreationView(UserIsInSpacePkMixin, CreateView):
    def get(self, request, pk):
        form = FridgeForm(space_id=pk)
        form.space = pk
        return render(request, 'shopping_lists/space.html', {'form': form})

    def post(self, request, pk):
        form = FridgeForm(request.POST, space_id=pk)
        if form.is_valid():
            fridge = Fridge.objects.create(**form.cleaned_data)
            return redirect('fridge_detail', space_id=pk, pk=fridge.id)
        return render(request, 'shopping_lists/space.html', {'form': form})


class FridgeEditView(UserIsInSpaceIdMixin, View):
    def get(self, request, pk, space_id):
        fridge = Fridge.objects.get(id=pk)
        form = FridgeForm(initial={'name': fridge.name})
        return render(request, 'shopping_lists/space.html', {'form': form})

    def post(self, request, pk, space_id):
        form = FridgeForm(request.POST, space_id=space_id, fridge_id=pk)
        if form.is_valid():
            fridge = Fridge.objects.get(id=pk)
            fridge.name = form.cleaned_data.get('name')
            fridge.save()
            return redirect('fridge_detail', space_id=space_id, pk=pk)
        return render(request, 'shopping_lists/space.html', {'form': form})


class FridgeListView(UserIsInSpacePkMixin, ListView):
    model = Fridge

    def get_queryset(self):
        return Fridge.objects.filter(space=Space.objects.get(pk=self.kwargs['pk']))


class FridgeDetailView(UserIsInSpaceIdMixin, DetailView):
    model = Fridge


class FridgeDeleteView(UserIsInSpaceIdMixin, DeleteView):
    model = Fridge
    success_url = reverse_lazy('space_list')
    template_name = 'delete_form.html'


class ShoppingListCreationView(UserIsInSpaceIdMixin, CreateView):
    def get(self, request, space_id, pk):
        form = ShoppingListForm(fridge_id=pk)
        form.space = space_id
        return render(request, 'shopping_lists/space.html', {'form': form})

    def post(self, request, space_id, pk):
        form = ShoppingListForm(request.POST, fridge_id=pk)
        if form.is_valid():
            shopping_list = ShoppingList.objects.create(**form.cleaned_data)
            return redirect('shopping_list_detail',
                            pk=shopping_list.pk,
                            fridge_id=pk,
                            space_id=space_id)
        return render(request, 'shopping_lists/space.html', {'form': form})


class ShoppingListEditView(UserIsInSpaceIdMixin, View):
    def get(self, request, pk, space_id, fridge_id):
        shopping_list = ShoppingList.objects.get(id=pk)
        form = ShoppingListForm(initial={'name': shopping_list.name})
        return render(request, 'shopping_lists/space.html', {'form': form})

    def post(self, request, pk, space_id, fridge_id):
        form = ShoppingListForm(request.POST, fridge_id=fridge_id, shopping_list_id=pk)
        if form.is_valid():
            shopping_list = ShoppingList.objects.get(id=pk)
            shopping_list.name = form.cleaned_data.get('name')
            shopping_list.save()
            return redirect('shopping_list_detail',
                            pk=pk,
                            fridge_id=fridge_id,
                            space_id=space_id)
        return render(request, 'shopping_lists/space.html', {'form': form})


class ShoppingListListView(UserIsInSpaceIdMixin, ListView):
    model = ShoppingList

    def get_queryset(self):
        return ShoppingList.objects.filter(space=Fridge.objects.get(pk=self.kwargs['fridge_id']))


class ShoppingListDetailView(UserIsInSpaceIdMixin, DetailView):
    model = ShoppingList


class ShoppingListDeleteView(UserIsInSpaceIdMixin, DeleteView):
    model = ShoppingList
    success_url = reverse_lazy('space_list')
    template_name = 'delete_form.html'
