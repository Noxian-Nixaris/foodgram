from django_filters import FilterSet

from foodgram.models import Ingredient, Recipe


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

    @property
    def qs(self):
        params = self.request.query_params
        queryset = Recipe.objects.all()
        user = self.request.user
        if 'is_in_shopping_cart' in params:
            queryset = queryset.filter(is_in_shopping_cart=user)
        if 'is_favorited' in params:
            queryset = queryset.filter(is_favorited=user)
        if 'author' in params:
            author = params.get('author')
            print(author)
            queryset = queryset.filter(author=author)
        if 'tags' in params:
            tags = (dict(params).get('tags'))
            queryset = queryset.filter(tags__slug__in=tags).distinct()
        return queryset
