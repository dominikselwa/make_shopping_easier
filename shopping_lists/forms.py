from django import forms

from shopping_lists.models import Space


class SpaceModelForm(forms.ModelForm):
    class Meta:
        model = Space
        fields = ('name',)
        labels = {
            'name': 'Nazwa przestrzeni',
        }


