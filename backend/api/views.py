from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet as DjoserUserViewSet
from rest_framework import filters, mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from api.serializers import (
    IngredientSerializer,
    RecipeCreateSerializer,
    RecipeSerializer,
    ShoppingCart,
    ShortRecipeSerializer,
    SubscriptionSerializer,
    TagSerializer,
    UserSerializer
)
from foodgram.models import Favorite, Ingredient, Recipe, Tag
from users_authentication.models import UserSubscription
from users_authentication.serializers import AvatarSerializer


User = get_user_model()


class UsersViewSet(DjoserUserViewSet):
    serializer_class = UserSerializer
    ordering = ('username', 'id')

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
            if 'avatar' not in self.request.data:
                return Response(
                    status=status.HTTP_400_BAD_REQUEST
                )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif request.method == "DELETE":
            avatar = user.avatar
            avatar.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=False, methods=['get'],
        url_path='me', permission_classes=[IsAuthenticated],
        serializer_class=UserSerializer)
    def me(self, request, *args, **kwargs):
        pk = request.user.pk
        object = get_object_or_404(User, pk=pk)
        serializer = UserSerializer(object)
        return Response(serializer.data)

    @action(
        detail=False, methods=['get'],
        url_path='subscriptions', permission_classes=[IsAuthenticated],
    )
    def show_subscriptions(self, request, *args, **kwargs):
        user = request.user
        object = User.objects.filter(subscribed_to__user=user)
        serializer = SubscriptionSerializer(
            object, context={'request': request}, many=True
        )
        return Response(serializer.data)

    @action(
        detail=True, methods=['post', 'delete'],
        url_path='subscribe', permission_classes=[IsAuthenticated],
    )
    def subscribe(self, request, *args, **kwargs):
        user = request.user
        sub = get_object_or_404(User, pk=self.kwargs['id'])
        if request.method == "POST":
            serializer = SubscriptionSerializer(
                user, data=request.data, partial=True,
                context={'request': request})
            serializer.is_valid(raise_exception=True)
            UserSubscription.objects.create(user=user, subscribed=sub)
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif request.method == "DELETE":
            subscribe = UserSubscription.objects.filter(
                user=user, subscribed=sub
            )
            subscribe.delete()
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
    serializer_class = RecipeSerializer

    def get_serializer_class(self):
        if self.action in ['create', 'update']:
            return RecipeCreateSerializer
        return RecipeSerializer

    # @action(
    #     detail=False, methods=['get', 'post'],
    #     permission_classes=[IsAuthenticated],
    # )
    # def recipe(self, request, *args, **kwargs):
    #     recipe = Recipe.objects.all()
    #     if request.method == "GET":
    #         serializer = RecipeSerializer(
    #             recipe, context={'request': request}, many=True
    #         )
    #         return Response(serializer.data)
    #     elif request.method == "POST":
    #         serializer = RecipeCreateSerializer(
    #             recipe, data=request.data,
    #             partial=True,
    #             context={'request': request},
    #         )
    #         serializer.is_valid(raise_exception=True)
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        detail=True, methods=['get'],
        url_path='get-link', permission_classes=[IsAuthenticated],
    )
    def get_link(self, request, *args, **kwargs):
        pass

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
                context={'request': request},
                partial=True
            )
            serializer.is_valid(raise_exception=True)
            ShoppingCart.objects.create(user=user, recipe=recipe)
            return Response(serializer.data)
        elif request.method == "DELETE":
            favorite = get_object_or_404(
                ShoppingCart, user=user, recipe=recipe
            )
            favorite.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=True, methods=['post', 'delete'],
        url_path='favorite', permission_classes=[IsAuthenticated],
    )
    def get_favorite(self, request, *args, **kwargs):
        recipe = get_object_or_404(Recipe, pk=self.kwargs['pk'])
        user = request.user
        if request.method == "POST":
            serializer = ShortRecipeSerializer(
                recipe, data=request.data,
                context={'request': request},
            )
            serializer.is_valid(raise_exception=True)
            Favorite.objects.create(user=user, favorite=recipe)
            return Response(serializer.data)
        elif request.method == "DELETE":
            favorite = get_object_or_404(Favorite, user=user, favorite=recipe)
            favorite.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=False, methods=['get', 'post'],
        url_path='download_shopping_cart',
        permission_classes=[IsAuthenticated],
    )
    def download_shopping_cart(self, request, *args, **kwargs):
        pass


class IngredientViewSet(BaseViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    ordering = ('name',)
