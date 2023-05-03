from rest_framework import viewsets

from ingredients.models import Ingredient
from api.serializer import IngredientSerializer


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
