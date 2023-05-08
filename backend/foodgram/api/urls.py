from django.urls import path, include
from rest_framework.routers import DefaultRouter

from ingredients.views import IngredientViewSet
from tegs.views import TagViewSet
from users.views import UserViewSet
from recipes.views import RecipeViewSet
from subscriptions.views import SubscriptionViewSet
from favorites.views import FavoriteViewSet


app_name = 'api'

router_v1 = DefaultRouter()
router_v1.register(r'ingredients', IngredientViewSet, basename='ingredients')
router_v1.register(r'tags', TagViewSet, basename='tags')
router_v1.register(r'users/(?P<user_id>\d+)/subscribe', SubscriptionViewSet, basename='subscribe')
router_v1.register(r'users', UserViewSet, basename='users')
router_v1.register(r'recipes', RecipeViewSet, basename='recipes')
router_v1.register(r'recipes/(?P<recipe_id>\d+)/favorite', FavoriteViewSet, basename='favorite')

urlpatterns = [
    path('', include(router_v1.urls)),
]
