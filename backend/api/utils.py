from datetime import date

from django.http import HttpResponse
from django.db.models import Sum

from recipes.models import IngredientInRecipe


def get_shopping_list_data(user):
    return IngredientInRecipe.objects.filter(
        recipe__shopping_cart__user=user
    ).values(
        'ingredients__name', 'ingredients__measurement_unit'
    ).annotate(
        amounts=Sum('amount', distinct=True)
    ).order_by('amounts')


def generate_shopping_list_response(data):
    today = date.today().strftime("%d-%m-%Y")
    shopping_list = f'Список покупок на: {today}\n\n'
    for ingredient in data:
        shopping_list += (
            f'{ingredient["ingredients__name"]} '
            f'({ingredient["ingredients__measurement_unit"]}) — '
            f'{ingredient["amounts"]}\n'
        )
    return HttpResponse(shopping_list,
                        content_type='text/plain; charset=utf-8')


def method_create(serializer, request, pk):
    request.data['recipe'] = pk
    request.data['user'] = request.user.id
    serializer = serializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return serializer.data
