from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from djoser.conf import settings
from djoser.views import UserViewSet as DjoserUserViewSet
from rest_framework import mixins, status, viewsets
from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.serializers import (
    IngredientSerializer, RecipeSerializer, TagSerializer
)
from users_authentication.serializers import AvatarSerializer, UserSerializer
from foodgram.models import Ingredient, Recipe, Tag

User = get_user_model()


class UsersViewSet(DjoserUserViewSet):
    serializer_class = UserSerializer
    ordering = ('username', 'id')

    def get_queryset(self):
        user = self.request.user
        queryset = User.objects.all()
        if self.action == 'retrieve':
            queryset = queryset.filter(pk=user.pk)
        return queryset

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


class IngredientViewSet(BaseViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None
