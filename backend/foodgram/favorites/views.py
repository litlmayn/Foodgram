from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.response import Response

from .models import Favorite
from recipes.models import Recipe
from api.serializer import FavoriteSerializer


class FavoriteViewSet(viewsets.ModelViewSet):
    serializer_class = FavoriteSerializer

    def create(self, request, *args, **kwargs):
        recipe = get_object_or_404(Recipe, pk=kwargs['recipe_id'])
        request.data['recipe'] = recipe.id
        request.data['user'] = request.user
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valide():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
