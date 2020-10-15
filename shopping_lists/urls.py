"""make_shopping_easier URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path

from shopping_lists import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('accounts/signup/', views.SingUpView.as_view(), name='signup'),
    path('main/', views.MainView.as_view(), name='main'),

    path('spaces/', views.SpaceListView.as_view(), name='space_list'),
    path('spaces/new/', views.SpaceCreateView.as_view(), name='space_new'),
    path('spaces/<int:pk>/', views.SpaceDetailView.as_view(), name='space_detail'),
    path('spaces/<int:pk>/edit/', views.SpaceEditView.as_view(), name='space_edit'),
    path('spaces/<int:pk>/delete/', views.SpaceDeleteView.as_view(), name='space_delete'),

    path('spaces/<int:pk>/fridges/', views.FridgeListView.as_view(), name='fridge_list'),
    path('spaces/<int:pk>/fridges/new/', views.FridgeCreationView.as_view(), name='fridge_new'),
    path('spaces/<int:space_id>/fridges/<int:pk>/', views.FridgeDetailView.as_view(), name='fridge_detail'),
    path('spaces/<int:space_id>/fridges/<int:pk>/edit/', views.FridgeEditView.as_view(), name='fridge_edit'),
    path('spaces/<int:space_id>/fridges/<int:pk>/delete/', views.FridgeDeleteView.as_view(), name='fridge_delete'),

    path('spaces/<int:space_id>/fridges/<int:pk>/lists/', views.ShoppingListListView.as_view(), name='shopping_list_list'),
    path('spaces/<int:space_id>/fridges/<int:pk>/lists/new/', views.ShoppingListCreationView.as_view(), name='shopping_list_new'),
    path('spaces/<int:space_id>/fridges/<int:fridge_id>/lists/<int:pk>/', views.ShoppingListDetailView.as_view(), name='shopping_list_detail'),
    path('spaces/<int:space_id>/fridges/<int:fridge_id>/lists/<int:pk>/edit/', views.ShoppingListEditView.as_view(), name='shopping_list_edit'),
    path('spaces/<int:space_id>/fridges/<int:fridge_id>/lists/<int:pk>/delete/', views.ShoppingListDeleteView.as_view(), name='shopping_list_delete'),
]
