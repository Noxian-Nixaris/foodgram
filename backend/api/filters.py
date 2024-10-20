from django_filters.rest_framework import (
    BooleanFilter,
    CharFilter,
    FilterSet,
    ModelMultipleChoiceFilter
)

from foodgram.models import Recipe, Tag


class IngredientFilter(FilterSet):
    name = CharFilter(lookup_expr='istartswith')


class RecipeTagFilter(FilterSet):
    is_in_shopping_cart = BooleanFilter(
        field_name='shopping_cart',
        method='filter_is_in_shopping_cart'
    )
    is_favorited = BooleanFilter(
        field_name='favorite',
        method='filter_is_favorited'
    )
    tags = ModelMultipleChoiceFilter(
        field_name='tags__slug',
        to_field_name='slug',
        queryset=Tag.objects.all()
    )

    class Meta:
        model = Recipe
        fields = ['tags', 'is_in_shopping_cart', 'is_favorited', 'author']

    def filter_is_favorited(self, queryset, name, value):
        if value:
            user = self.request.user
            if user.is_authenticated:
                return queryset.filter(favorite__user=user)
        return queryset

    def filter_is_in_shopping_cart(self, queryset, name, value):
        if value:
            user = self.request.user
            if user.is_authenticated:
                return queryset.filter(shopping_cart__user=user)
        return queryset
