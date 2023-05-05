from rest_framework import viewsets

from api.serializer import RecipeSerializer
from .models import Recipe


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
