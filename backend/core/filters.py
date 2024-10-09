from django_filters import FilterSet, CharFilter

from foodgram.models import Ingredient


class IngredientFilter(FilterSet):
    name = CharFilter(lookup_expr='istartswith')

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
