from django_filters import FilterSet, ModelMultipleChoiceFilter

from foodgram.models import Ingredient, Recipe, Tag


class IngredientFilter(FilterSet):

    class Meta:
        model = Ingredient
        fields = ('name',)

    @property
    def qs(self):
        params = self.request.query_params
        queryset = Ingredient.objects.all()
        if 'name' in params:
            params = dict(params).get('name')[0]
            queryset = queryset.filter(name__istartswith=params)
        return queryset


class RecipeTagFilter(FilterSet):

    tags = ModelMultipleChoiceFilter(
        field_name='tags__slug',
        to_field_name='slug',
        queryset=Tag.objects.all()
    )

    @property
    def qs(self):
        params = self.request.query_params
        queryset = Recipe.objects.all()
        user = self.request.user
        if 'is_in_shopping_cart' in params:
            queryset = queryset.filter(is_in_shopping_cart=user)
        elif 'is_favorited' in params:
            queryset = queryset.filter(is_favorited=user)
        return queryset
