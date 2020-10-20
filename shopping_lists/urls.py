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

    path('fridges/', views.FridgeListView.as_view(), name='fridge_list'),
    path('fridges/create/', views.FridgeCreateView.as_view(), name='fridge_create'),
    path('fridges/<int:pk>/', views.FridgeDetailView.as_view(), name='fridge_detail'),
    path('fridges/<int:pk>/update/', views.FridgeUpdateView.as_view(), name='fridge_update'),
    path('fridges/<int:pk>/delete/', views.FridgeDeleteView.as_view(), name='fridge_delete'),

    path('fridges/<int:pk>/category/create/', views.CategoryCreateView.as_view(), name='category_create'),
    path('fridges/<int:fridge_id>/category/<int:pk>/update/', views.CategoryUpdateView.as_view(),
         name='category_update'),
    path('fridges/<int:fridge_id>/category/<int:pk>/delete/', views.CategoryDeleteView.as_view(),
         name='category_delete'),

    path('fridges/<int:pk>/shop/create/', views.ShopCreateView.as_view(), name='shop_create'),
    path('fridges/<int:fridge_id>/shop/<int:pk>/update/', views.ShopUpdateView.as_view(), name='shop_update'),
    path('fridges/<int:fridge_id>/shop/<int:pk>/delete/', views.ShopDeleteView.as_view(), name='shop_delete'),

    path('fridges/<int:pk>/product/create/', views.ProductCreateView.as_view(), name='product_create'),
    path('fridges/<int:fridge_id>/product/<int:pk>/update/', views.ProductUpdateView.as_view(), name='product_update'),
    path('fridges/<int:fridge_id>/product/<int:pk>/delete/', views.ProductDeleteView.as_view(), name='product_delete'),

    path('fridges/<int:pk>/products-to-fridge/', views.ProductsToFridge.as_view(), name='products_to_fridge'),
    path('fridges/<int:pk>/products-to-shopping-list/', views.ProductsToShoppingList.as_view(),
         name='products_to_shopping_list'),

    path('fridges/<int:pk>/recipe/create/', views.RecipeCreateView.as_view(), name='recipe_create'),
    path('fridges/<int:fridge_id>/recipe/<int:pk>/', views.RecipeDetailView.as_view(), name='recipe_detail'),
    path('fridges/<int:fridge_id>/recipe/<int:pk>/update/', views.RecipeUpdateView.as_view(), name='recipe_update'),
    path('fridges/<int:fridge_id>/recipe/<int:pk>/delete/', views.RecipeDeleteView.as_view(), name='recipe_delete'),
    path('fridges/<int:fridge_id>/recipe/<int:pk>/add-to-shopping-list/', views.AddRecipeToShoppingListView.as_view(),
         name='add_recipe_to_shopping_list'),

    path('my-recipes/', views.UserRecipeListView.as_view(), name='recipe_list'),

    path('fridges/<int:fridge_id>/recipe/<int:pk>/product-in-recipe/create/',
         views.ProductInRecipeCreateView.as_view(), name='product_in_recipe_create'),
    path('fridges/<int:fridge_id>/product-in-recipe/<int:pk>/update/', views.ProductInRecipeUpdateView.as_view(),
         name='product_in_recipe_update'),
    path('fridges/<int:fridge_id>/product-in-recipe/<int:pk>/delete/', views.ProductInRecipeDeleteView.as_view(),
         name='product_in_recipe_delete'),

    path('fridges/<int:pk>/invitation/create/', views.InvitationCreateView.as_view(), name='invitation_create'),
    path('invitation/<slug:slug>/', views.InvitationAcceptView.as_view(), name='invitation_accept'),
    path('fridges/<int:fridge_id>/invitation/<int:pk>/', views.InvitationShowView.as_view(), name='invitation_show'),

]
