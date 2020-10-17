# from shopping_lists.models import Fridge, Space, ShoppingList
#
#
# # def user_data(request):
# #     if request.user.is_authenticated:
# #         spaces = Space.objects.filter(users=request.user)
# #         fridges = Fridge.objects.filter(space__in=spaces)
# #         shopping_lists = ShoppingList.objects.filter(fridge__in=fridges)
# #         return {'spaces': spaces, 'fridges': fridges, 'shopping_lists': shopping_lists}
# #     return {'spaces': None, 'fridges': None, 'shopping_lists': None}