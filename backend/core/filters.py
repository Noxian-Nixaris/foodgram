from django_filters import FilterSet, ModelChoiceFilter, ModelMultipleChoiceFilter
from foodgram.models import Recipe, Tag


class IngredientFilter(ModelMultipleChoiceFilter):
    pass