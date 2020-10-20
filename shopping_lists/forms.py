from django import forms
from django.core.exceptions import ValidationError
from django.forms import formset_factory

from shopping_lists.models import Fridge, Category, Shop, Product, Recipe, ProductInRecipe


class FridgeUniqueModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.fridge = Fridge.objects.get(pk=kwargs.pop('fridge_id'))
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get('name')
        if name is not None:
            if self.Meta.model.objects.filter(fridge=self.fridge, name=name).exclude(id=self.instance.id).count() > 0:
                raise ValidationError(self.instance.get_unique_error())
            self.instance.fridge = self.fridge
            return cleaned_data


class FridgeModelForm(forms.ModelForm):
    class Meta:
        model = Fridge
        fields = ('name',)
        labels = {
            'name': 'Nazwa lodówki:',
        }


class CategoryModelForm(FridgeUniqueModelForm):
    class Meta:
        model = Category
        fields = ('name',)
        labels = {
            'name': 'Nazwa kategorii:',
        }


class ShopModelForm(FridgeUniqueModelForm):
    class Meta:
        model = Shop
        fields = ('name',)
        labels = {
            'name': 'Nazwa sklepu:',
        }


class ProductModelForm(FridgeUniqueModelForm):
    class Meta:
        model = Product
        fields = ('name', 'quantity', 'unit', 'category', 'shops', 'is_in_shopping_list')
        labels = {
            'name': 'Nazwa produktu:',
            'quantity': 'Ilość/Liczba produktów, które mają być widoczne na liście zakupów:',
            'unit': 'Jednostka jakiej chcesz używać do tego produktu:',
            'category': 'Kategoria, do której ma być przyporządkowany produkt:',
            'shops': 'Sklepy w których będziesz kupować ten produkt:',
            'is_in_shopping_list': 'Chcesz go dodać do listy zakupów?',
        }
        widgets = {
            'shops': forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.filter(fridge=self.fridge)
        self.fields['shops'].queryset = Shop.objects.filter(fridge=self.fridge)
        self.fields['category'].required = False
        self.fields['unit'].required = False
        self.fields['quantity'].required = False
        self.fields['shops'].required = False
        self.fields['quantity'].widget.attrs['min'] = 0


class RecipeModelForm(FridgeUniqueModelForm):
    class Meta:
        model = Recipe
        fields = ('name',)
        labels = {
            'name': 'Nazwa przepisu:',
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        self.instance.owner = self.user
        return cleaned_data


class ProductInRecipeModelForm(forms.ModelForm):
    class Meta:
        model = ProductInRecipe
        fields = ('product', 'quantity_in_recipe')

    def __init__(self, *args, **kwargs):
        self.recipe = kwargs.pop('recipe', None)
        super().__init__(*args, **kwargs)
        if self.recipe is None:
            self.recipe = self.instance.recipe
        self.fields['product'].queryset = Product.objects.filter(fridge=self.recipe.fridge)
        self.fields['quantity_in_recipe'].required = False
        self.fields['quantity_in_recipe'].widget.attrs['min'] = 0

    def clean(self):
        cleaned_data = super().clean()
        if self.recipe is not None:
            self.instance.recipe = self.recipe
        return cleaned_data

# na przyszłość
# ProductInRecipeFormSet = formset_factory(ProductInRecipeModelForm)
