from django import forms
from django.core.exceptions import ValidationError

from shopping_lists.models import Space, Fridge


class SpaceModelForm(forms.ModelForm):
    class Meta:
        model = Space
        fields = ('name',)
        labels = {
            'name': 'Nazwa przestrzeni',
        }


class FridgeForm(forms.Form):
    name = forms.CharField(max_length=32, label='Nazwa lodówki')

    def __init__(self, *args, **kwargs):
        self.space_id = kwargs.pop('space_id', None)
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get('name')
        if name is not None:
            space = Space.objects.get(pk=self.space_id)
            if space.fridges.filter(name=name).count() > 0:
                raise ValidationError('Nie można dodać kolejnej lodówki o takiej nazwie')
            cleaned_data['space'] = space
            return cleaned_data

class ShoppingListForm(forms.Form):
    name = forms.CharField(max_length=32, label='Nazwa listy zakupów')

    def __init__(self, *args, **kwargs):
        self.fridge_id = kwargs.pop('fridge_id', None)
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get('name')
        if name is not None:
            fridge = Fridge.objects.get(pk=self.fridge_id)
            if fridge.shopping_lists.filter(name=name).count() > 0:
                raise ValidationError('Nie można dodać kolejnej listy zakupów o takiej nazwie')
            cleaned_data['fridge'] = fridge
            return cleaned_data