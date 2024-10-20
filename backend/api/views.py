import random

from django.conf import settings
from django.contrib.auth import get_user_model
from django_filters.rest_framework.backends import DjangoFilterBackend
from django.http import FileResponse, Http404
from django.shortcuts import get_object_or_404, redirect
from djoser.views import UserViewSet as DjoserUserViewSet
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import (
    IsAuthenticated
)
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from api.filters import IngredientFilter, RecipeTagFilter
from api.pagination import PageCastomPaginator
from api.permissions import IsAutorOrReadOnly
from api.serializers import (
    AvatarSerializer,
    FavoriteRecipeSerializer,
    IngredientSerializer,
    RecipeCreateSerializer,
    RecipeSerializer,
    ShoppingCart,
    ShortRecipeSerializer,
    ShortURLSerializer,
    SubscriptionSerializer,
    TagSerializer,
    UserSerializer
)
from core.constants import CHARACTERS, URL_LENGTH
from foodgram.models import (
    Favorite, Ingredient, Recipe, RecipeIngredient, ShortURL, Tag
)
from users_authentication.models import UserSubscription


User = get_user_model()


class UsersViewSet(DjoserUserViewSet):
    serializer_class = UserSerializer
    ordering = ('username', 'id')
    pagination_class = PageCastomPaginator

    def get_queryset(self):
        return User.objects.all()

    @action(
        detail=False, methods=['put', 'delete'],
        url_path='me/avatar', permission_classes=[IsAuthenticated])
    def update_avatar(self, request, *args, **kwargs):
        user = request.user
        if request.method == "PUT":
            serializer = AvatarSerializer(
                user, data=request.data, partial=True,
                context={'request': request}
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        avatar = user.avatar
        avatar.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=False, methods=['get'],
        url_path='me', permission_classes=[IsAuthenticated]
    )
    def me(self, request, *args, **kwargs):
        object = request.user
        serializer = UserSerializer(
            object, partial=True, context={'request': request})
        return Response(serializer.data)

    @action(
        detail=False, methods=['get'],
        url_path='subscriptions', permission_classes=[IsAuthenticated],
    )
    def show_subscriptions(self, request, *args, **kwargs):
        user = request.user
        objects = UserSubscription.objects.filter(user=user)
        queryset = [object.subscribed for object in objects]
        paginator = PageCastomPaginator()
        paginated_queryset = paginator.paginate_queryset(queryset, request)
        serializer = SubscriptionSerializer(
            paginated_queryset, context={'request': request}, many=True,
        )
        serializer = paginator.get_paginated_response(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        detail=True, methods=['post', 'delete'],
        url_path='subscribe', permission_classes=[IsAuthenticated],
    )
    def subscribe(self, request, *args, **kwargs):
        user = request.user
        sub = get_object_or_404(User, pk=self.kwargs['id'])
        if request.method == "POST":
            serializer = SubscriptionSerializer(
                sub, data=request.data, partial=True,
                context={'request': request, 'sub': sub}
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        elif request.method == "DELETE":
            try:
                obj = UserSubscription.objects.get(
                    user=user, subscribed=sub
                )
                obj.delete()
            except Exception:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            return Response(status=status.HTTP_204_NO_CONTENT)


class BaseViewSet(
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    GenericViewSet
):
    pass


class TagViewSet(BaseViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None


class RecipesViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    permission_classes = (IsAutorOrReadOnly,)
    serializer_class = RecipeSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeTagFilter
    filterset_fields = (
        'is_in_shopping_cart', 'is_favorited', 'tags', 'author'
    )

    def get_serializer_class(self):
        if self.action in ['create', 'partial_update']:
            return RecipeCreateSerializer
        return RecipeSerializer

    @action(
        detail=True, methods=['get'],
        url_path='get-link',
    )
    def get_link(self, request, *args, **kwargs):
        full_link = f'{settings.DOMAIN}recipes/{self.kwargs["pk"]}'
        link = ShortURL.objects.filter(full_link=full_link).first()
        if link is None:
            short_links = ShortURL.objects.all()
            while True:
                short_link = ''.join(random.choices(CHARACTERS, k=URL_LENGTH))
                if not short_links.filter(short_link=short_link):
                    break
            link = ShortURL.objects.create(
                short_link=short_link,
                full_link=full_link
            )
        serializer = ShortURLSerializer(link)
        return Response(serializer.data)

    @action(
        detail=True, methods=['post', 'delete'],
        url_path='shopping_cart', permission_classes=[IsAuthenticated],
    )
    def add_to_shopping_cart(self, request, *args, **kwargs):
        recipe = get_object_or_404(Recipe, pk=self.kwargs['pk'])
        user = request.user
        if request.method == "POST":
            serializer = ShortRecipeSerializer(
                recipe,
                data=request.data,
                context={'request': request, 'recipe': recipe},
                partial=True
            )
            serializer.is_valid(raise_exception=True)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        elif request.method == "DELETE":
            try:
                obj = ShoppingCart.objects.get(user=user, recipe=recipe)
                obj.delete()
            except Exception:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=True, methods=['post', 'delete'],
        url_path='favorite', permission_classes=[IsAuthenticated],
    )
    def get_favorite(self, request, *args, **kwargs):
        recipe = get_object_or_404(Recipe, pk=self.kwargs['pk'])
        user = request.user
        if request.method == "POST":
            serializer = FavoriteRecipeSerializer(
                recipe, data=request.data,
                context={'request': request, 'recipe': recipe},
            )
            serializer.is_valid(raise_exception=True)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        elif request.method == "DELETE":
            try:
                obj = Favorite.objects.get(user=user, favorite=recipe)
                obj.delete()
            except Exception:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=False, methods=['get'],
        url_path='download_shopping_cart',
        permission_classes=[IsAuthenticated],
    )
    def download_shopping_cart(self, request, *args, **kwargs):
        user = request.user.username
        cart = ShoppingCart.objects.filter(user=request.user)
        ingreds = {}
        for recipe in cart:
            query = RecipeIngredient.objects.filter(recipe=recipe.recipe)
            for recipe in query:
                ingr_name = recipe.ingredient.name
                ingr_amount = recipe.amount
                if ingr_name not in ingreds:
                    ingreds[ingr_name] = ingr_amount
                else:
                    ingreds[ingr_name] = ingreds[ingr_name] + ingr_amount
        cart = 'список' + '\n'
        for items in ingreds:
            cart += f'{items} {ingreds.get(items)}' + '\n'
        return FileResponse(
            cart, content_type='txt', filename=f'cart-{user}.txt'
        )


class IngredientViewSet(BaseViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None
    filter_backends = (DjangoFilterBackend,)
    filterset_class = IngredientFilter
    filterset_fields = ('name',)
    ordering = ('name',)


def redirection(request, short_link):
    try:
        full_link = get_object_or_404(
            ShortURL, short_link=short_link
        ).full_link
        return redirect(full_link)
    except Http404:
        return Response(status=status.HTTP_404_NOT_FOUND)
