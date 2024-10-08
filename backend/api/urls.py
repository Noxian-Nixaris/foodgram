from django.urls import include, path
from rest_framework.routers import DefaultRouter
from api.views import (
    IngredientViewSet, RecipesViewSet, TagViewSet, UsersViewSet
)

router = DefaultRouter()
router.register('users', UsersViewSet, basename='users')
router.register('tags', TagViewSet, basename='tags'),
router.register('recipes', RecipesViewSet, basename='recipes')
router.register('ingredients', IngredientViewSet, basename='ingredients')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('djoser.urls.authtoken')),
]
