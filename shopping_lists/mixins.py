from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404

from shopping_lists.models import Space


class UserIsInSpaceMixin(UserPassesTestMixin):
    def test_func(self):
        space_id = None

        if self.kwargs.get('space_id') is not None:
            space_id = self.kwargs.get('space_id')
        elif self.kwargs.get('pk') is not None:
            space_id = self.kwargs.get('pk')

        if space_id is not None:
            try:
                return self.request.user in Space.objects.get(pk=space_id).users.all()
            except ObjectDoesNotExist:
                raise Http404