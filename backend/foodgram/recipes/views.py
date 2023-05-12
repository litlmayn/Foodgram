from datetime import date

from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404

from api.serializer import (RecipeAddSerializer, IngredientSerializer,
                            TagSerializer, SubscriptionSerializer,
                            FavoriteSerializer, ShoppingCartSerializer,
                            RecipeListSerializer)
from .models import Recipe, Ingredient, Tag, Subscription, Favorite, ShoppingCart, IngredientInRecipe
from users.models import CustomUser


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


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeAddSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return RecipeListSerializer
        return RecipeAddSerializer

    @action(detail=False,
            methods=['get'],
            permission_classes=[IsAuthenticated])
    def download_shopping_cart(self, request):
        author = get_object_or_404(CustomUser, id=self.request.user.pk)
        if author.shopping_cart.exists():
            data = get_shopping_list_data(author)
            response = generate_shopping_list_response(data)
            filename = 'shopping_list.txt'
            response['Content-Disposition'] = (f'attachment; '
                                               f'filename={filename}')
            return response
        return Response({'message': 'Список покупок пуст'},
                        status=status.HTTP_404_NOT_FOUND)


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class SubscriptionViewSet(mixins.CreateModelMixin,
                          mixins.DestroyModelMixin,
                          viewsets.GenericViewSet):

    def create(self, request, **kwargs):
        following = get_object_or_404(CustomUser, pk=kwargs['user_id'])
        request.data['user'] = request.user.id
        request.data['following'] = following.id
        serializer = SubscriptionSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data,
                            status=status.HTTP_201_CREATED)

    def delete(self, request, *args, **kwargs):
        following = get_object_or_404(CustomUser, pk=kwargs['user_id'])
        Subscription.objects.filter(
            following=following, user=request.user).delete()
        return Response({'message': f'Вы успешно отписались от пользователя {following}!'},
                        status=status.HTTP_204_NO_CONTENT)


class FavoriteViewSet(mixins.CreateModelMixin,
                      mixins.DestroyModelMixin,
                      viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated]

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
        return Response({'message': 'Рецепт удалён из избранного!'},
                        status=status.HTTP_204_NO_CONTENT)


class ShoppingCartViewSet(mixins.CreateModelMixin,
                          mixins.DestroyModelMixin,
                          viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated]

    def create(self, request, **kwargs):
        recipe = get_object_or_404(CustomUser, pk=kwargs['recipe_id'])
        request.data['recipe'] = recipe.id
        request.data['user'] = request.user.id
        serializer = ShoppingCartSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data,
                            status=status.HTTP_201_CREATED)

    def delete(self, request, *args, **kwargs):
        recipe = get_object_or_404(Recipe, pk=kwargs['recipe_id'])
        get_object_or_404(ShoppingCart, user=request.user, recipe=recipe).delete()
        return Response({'message': 'Рецепт удалён из списка покупок!'},
                        status=status.HTTP_204_NO_CONTENT)
