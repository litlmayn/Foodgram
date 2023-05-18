from django.db.models import Sum
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet as DjoserUserViewSet
from rest_framework import status, viewsets, permissions
from rest_framework.decorators import action
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response

from api.utils import (generate_shopping_list_response,
                       method_create)
from api.filters import RecipeFilter, IngredientSearchFilter
from api.serializer import (FavoriteSerializer, IngredientSerializer,
                            RecipeAddSerializer, RecipeListSerializer,
                            ShoppingCartSerializer, SubscriptionSerializer,
                            TagSerializer, UserSerializer, SubscribeSerializer)
from api.permissions import IsCurrentUserOrAdminOrReadOnly
from users.models import CustomUser
from recipes.models import (Favorite, Ingredient, IngredientInRecipe, Recipe,
                            ShoppingCart, Tag, Subscription)


class UserViewSet(DjoserUserViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsCurrentUserOrAdminOrReadOnly]

    @action(methods=['post'],
            permission_classes=[IsAuthenticated],
            detail=True)
    def subscribe(self, request, **kwargs):
        following = get_object_or_404(CustomUser, pk=kwargs['id'])
        request.data['user'] = request.user.id
        request.data['following'] = following.id
        serializer = SubscriptionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data,
                        status=status.HTTP_201_CREATED)

    @subscribe.mapping.delete
    def delete_subscribe(self, request, **kwargs):
        get_object_or_404(
            Subscription,
            following=get_object_or_404(CustomUser, pk=kwargs['id']),
            user=request.user).delete()
        return Response({'message':
                        'Вы успешно отписались от пользователя!'},
                        status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, permission_classes=[IsAuthenticated])
    def subscriptions(self, request):
        follows = CustomUser.objects.filter(following__user=self.request.user)
        pages = self.paginate_queryset(follows)
        serializer = SubscribeSerializer(
            pages,
            many=True,
            context={'request': request}
        )
        return self.get_paginated_response(serializer.data)


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeAddSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter

    def get_serializer_class(self):
        if self.action in permissions.SAFE_METHODS:
            return RecipeListSerializer
        return RecipeAddSerializer

    @action(detail=False,
            methods=['get'],
            permission_classes=[IsAuthenticated])
    def download_shopping_cart(self, request):
        user = self.request.user.id
        if user.shopping_cart.exists():
            data = IngredientInRecipe.objects.filter(
                        recipe__shopping_cart__user=user
                    ).values(
                        'ingredients__name', 'ingredients__measurement_unit'
                    ).annotate(
                        amounts=Sum('amount')
                    ).order_by('ingredients__name')
            response = generate_shopping_list_response(data)
            return response
        return Response({'message': 'Список покупок пуст'},
                        status=status.HTTP_404_NOT_FOUND)

    @action(methods=['post'],
            permission_classes=[IsAuthenticated],
            detail=True)
    def favorite(self, request, pk):
        return Response(method_create(FavoriteSerializer, request, pk),
                        status=status.HTTP_201_CREATED)

    @favorite.mapping.delete
    def delete_favorite(self, request, pk):
        get_object_or_404(Favorite, user=request.user.id, recipe=pk).delete()
        return (Response({'message': 'Рецепт удалён'},
                status=status.HTTP_204_NO_CONTENT)
                )

    @action(methods=['post'],
            permission_classes=[IsAuthenticated],
            detail=True)
    def shopping_cart(self, request, pk):
        return Response(method_create(ShoppingCartSerializer, request, pk),
                        status=status.HTTP_201_CREATED)

    @shopping_cart.mapping.delete
    def delete_shopping_cart(self, request, pk):
        get_object_or_404(
            ShoppingCart, user=request.user.id, recipe=pk).delete()
        return (Response({'message': 'Рецепт удалён'},
                status=status.HTTP_204_NO_CONTENT)
                )


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None
    filter_backends = (IngredientSearchFilter,)
    search_fields = ('^name',)


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None
