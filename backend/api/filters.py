from django_filters import CharFilter, FilterSet

from foodgram.models import Recipe


class IngredientFilter(FilterSet):
    name = CharFilter(lookup_expr='istartswith')


class RecipeTagFilter(FilterSet):
    is_in_shopping_cart = CharFilter(
        field_name='is_in_shopping_cart', method='filter_is_in_shopping_cart'
    )
    is_favorited = CharFilter(
        field_name='is_favorited', method='filter_is_favorited'
    )
    author = CharFilter(field_name='author')
    tags = CharFilter(field_name='tags', method='filter_tags')

    def filter_tags(self, queryset, name, value):
        tags = dict(self.request.query_params).get('tags')
        return queryset.filter(tags__slug__in=tags).distinct()

    def filter_is_favorited(self, queryset, name, value):
        user = self.request.user
        return queryset.filter(favorite__user=user)

    def filter_is_in_shopping_cart(self, queryset, name, value):
        user = self.request.user
        return queryset.filter(shopping_cart__user=user)

    class Meta:
        model = Recipe
        fields = ['tags', 'is_in_shopping_cart', 'is_favorited', 'author']
