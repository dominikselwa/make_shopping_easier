from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404

from shopping_lists.models import Fridge


class UserHasAccessToFridgeMixin(UserPassesTestMixin):
    def test_func(self):
        fridge_id = None

        if self.kwargs.get('fridge_id') is not None:
            fridge_id = self.kwargs.get('fridge_id')
        elif self.kwargs.get('pk') is not None:
            fridge_id = self.kwargs.get('pk')

        if fridge_id is not None:
            try:
                return self.request.user in Fridge.objects.get(pk=fridge_id).users.all()
            except ObjectDoesNotExist:
                raise Http404
