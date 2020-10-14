from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, ListView, DetailView, DeleteView

from shopping_lists.forms import SpaceModelForm
from shopping_lists.models import Space


class UserIsInSpacePkMixin(UserPassesTestMixin):
    def test_func(self):
        if self.kwargs.get('pk') is not None:
            return self.request.user in Space.objects.get(pk=self.kwargs['pk']).users.all()


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


class SpaceListView(ListView):
    model = Space

    def get_queryset(self):
        print(Space.objects.filter(users=self.request.user))
        return Space.objects.filter(users=self.request.user)


class SpaceDetailView(UserIsInSpacePkMixin, DetailView):
    model = Space


class SpaceDeleteView(UserIsInSpacePkMixin, DeleteView):
    model = Space
    success_url = reverse_lazy('space_list')
