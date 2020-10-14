from shopping_lists.models import Fridge, Space


def user_data(request):
    if request.user.is_authenticated:
        spaces = Space.objects.filter(users=request.user)
        fridges = Fridge.objects.filter(space__in=spaces)
        return {'spaces': spaces, 'fridges': fridges}
