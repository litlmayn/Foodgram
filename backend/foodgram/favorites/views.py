from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status, mixins
from rest_framework.response import Response

from .models import Favorite
from recipes.models import Recipe
from api.serializer import FavoriteSerializer


class FavoriteViewSet(mixins.CreateModelMixin,
                      mixins.DestroyModelMixin,
                      viewsets.GenericViewSet):

    def create(self, request, *args, **kwargs):
        recipe = get_object_or_404(Recipe, pk=kwargs['recipe_id'])
        request.data['recipe'] = recipe.id
        request.data['user'] = request.user.id
        serializer = FavoriteSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, *args, **kwargs):
        recipe = get_object_or_404(Recipe, pk=kwargs['recipe_id'])
        get_object_or_404(Favorite, user=request.user, recipe=recipe).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

