from rest_framework import viewsets

from ingredients.models import Ingredient
from api.serializer import IngredientSerializer


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    pagination_class = None
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
