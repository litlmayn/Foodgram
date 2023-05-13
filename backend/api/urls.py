from django.urls import include, path, re_path
from recipes.views import (FavoriteViewSet, IngredientViewSet, RecipeViewSet,
                             ShoppingCartViewSet, SubscriptionViewSet,
                             TagViewSet)
from rest_framework.routers import DefaultRouter
from users.views import UserViewSet

app_name = 'api'

router_v1 = DefaultRouter()
router_v1.register(r'ingredients', IngredientViewSet, basename='ingredients')
router_v1.register(r'tags', TagViewSet, basename='tags')
router_v1.register(r'users/(?P<user_id>\d+)/subscribe',
                   SubscriptionViewSet, basename='subscribe')
router_v1.register(r'users', UserViewSet, basename='users')
router_v1.register(r'recipes', RecipeViewSet, basename='recipes')
router_v1.register(r'recipes/(?P<recipe_id>\d+)/shopping_cart',
                   ShoppingCartViewSet, basename='shopping_cart')
router_v1.register(r'recipes/(?P<recipe_id>\d+)/favorite',
                   FavoriteViewSet, basename='favorite')

urlpatterns = [
    path('', include(router_v1.urls)),
    re_path(r'auth/', include('djoser.urls.authtoken')),
]
