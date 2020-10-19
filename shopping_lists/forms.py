from django import forms
from django.core.exceptions import ValidationError

from shopping_lists.models import Fridge, Category, Shop, Product


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


    # def __init__(self, *args, **kwargs):
    #     self.fridge = Fridge.objects.get(pk=kwargs.pop('fridge_id'))
    #     super().__init__(*args, **kwargs)
    #
    # def clean(self):
    #     cleaned_data = super().clean()
    #     name = cleaned_data.get('name')
    #     if name is not None:
    #         if self.fridge.categories.filter(name=name).exclude(id=self.instance.id).count() > 0:
    #             raise ValidationError(self.instance.get_unique_error())
    #         self.instance.fridge = self.fridge
    #         return cleaned_data

# class CategoryModelForm(forms.ModelForm):
#     def __init__(self, *args, **kwargs):
#         self.object_id = kwargs.pop('object_id', None)
#         self.fridge_id = kwargs.pop('fridge_id', None)
#         super().__init__(*args, **kwargs)
#
#
#     def clean(self):
#         cleaned_data = super().clean()
#         name = cleaned_data.get('name')
#         if name is not None:
#             fridge = Fridge.objects.get(pk=self.fridge_id)
#             print(fridge)
#             if fridge.categories.filter(name=name).exclude(id=self.object_id).count() > 0:
#                 raise ValidationError('Nie można dodać kolejnej kategorii o takiej nazwie')
#             self.instance.fridge = fridge
#             return cleaned_data

# class FormWithExtraKwargs(forms.)

#
# class SpaceModelForm(forms.ModelForm):
#     class Meta:
#         model = Space
#         fields = ('name',)
#         labels = {
#             'name': 'Nazwa przestrzeni',
#         }
#
#
# class FridgeForm(forms.Form):
#     name = forms.CharField(max_length=32, label='Nazwa lodówki')
#
#     def __init__(self, *args, **kwargs):
#         self.space_id = kwargs.pop('space_id', None)
#         self.fridge_id = kwargs.pop('fridge_id', None)
#         super().__init__(*args, **kwargs)
#
#     def clean(self):
#         cleaned_data = super().clean()
#         name = cleaned_data.get('name')
#         if name is not None:
#             space = Space.objects.get(pk=self.space_id)
#             if space.fridges.filter(name=name).exclude(id=self.fridge_id).count() > 0:
#                 raise ValidationError('Nie można dodać kolejnej lodówki o takiej nazwie')
#             cleaned_data['space'] = space
#             return cleaned_data
#
# class ShoppingListForm(forms.Form):
#     name = forms.CharField(max_length=32, label='Nazwa listy zakupów')
#
#     def __init__(self, *args, **kwargs):
#         self.fridge_id = kwargs.pop('fridge_id', None)
#         self.shopping_list_id = kwargs.pop('shopping_list_id', None)
#         super().__init__(*args, **kwargs)
#
#     def clean(self):
#         cleaned_data = super().clean()
#         name = cleaned_data.get('name')
#         if name is not None:
#             fridge = Fridge.objects.get(pk=self.fridge_id)
#             if fridge.shopping_lists.filter(name=name).exclude(id=self.shopping_list_id).count() > 0:
#                 raise ValidationError('Nie można dodać kolejnej listy zakupów o takiej nazwie')
#             cleaned_data['fridge'] = fridge
#             return cleaned_data
#
#
# class CategoryForm(forms.Form):
#     name = forms.CharField(max_length=32, label='Nazwa kategorii')
#
#     def __init__(self, *args, **kwargs):
#         self.space_id = kwargs.pop('space_id', None)
#         self.category_id = kwargs.pop('category_id', None)
#         super().__init__(*args, **kwargs)
#
#     def clean(self):
#         cleaned_data = super().clean()
#         name = cleaned_data.get('name')
#         if name is not None:
#             space = Space.objects.get(pk=self.space_id)
#             if space.categories.filter(name=name).exclude(id=self.category_id).count() > 0:
#                 raise ValidationError('Nie można dodać kolejnej kategorii o takiej nazwie')
#             cleaned_data['space'] = space
#             return cleaned_data
