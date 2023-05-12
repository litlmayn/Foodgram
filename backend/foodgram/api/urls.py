from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter

from users.views import UserViewSet
from recipes.views import RecipeViewSet, TagViewSet, IngredientViewSet, SubscriptionViewSet, FavoriteViewSet, ShoppingCartViewSet


app_name = 'api'

router_v1 = DefaultRouter()
router_v1.register(r'ingredients', IngredientViewSet, basename='ingredients')
router_v1.register(r'tags', TagViewSet, basename='tags')
router_v1.register(r'users/(?P<user_id>\d+)/subscribe', SubscriptionViewSet, basename='subscribe')
router_v1.register(r'users', UserViewSet, basename='users')
router_v1.register(r'recipes', RecipeViewSet, basename='recipes')
router_v1.register(r'recipes/(?P<recipe_id>\d+)/shopping_cart', ShoppingCartViewSet, basename='shopping_cart')
router_v1.register(r'recipes/(?P<recipe_id>\d+)/favorite', FavoriteViewSet, basename='favorite')

urlpatterns = [
    path('', include(router_v1.urls)),
    re_path(r'auth/', include('djoser.urls.authtoken')),
]
