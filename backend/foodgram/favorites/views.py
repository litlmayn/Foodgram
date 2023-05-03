from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.response import Response

from .models import Favorite
from recipes.models import Recipe
from api.serializer import FavoriteSerializer


class FavoriteViewSet(viewsets.ModelViewSet):

    def create(self, request, *args, **kwargs):
        pk = kwargs['recipe_id']
        recipe = get_object_or_404(Recipe, pk=pk)
        favorite = Favorite.objects.create(user=request.user, recipe=recipe)
        serializer = FavoriteSerializer(favorite)
        return Response(serializer.data)
