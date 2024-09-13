from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from users_authentication.models import User

from foodgram.models import Ingredient, Recipe, Tag


class IngredientAdmin(admin.ModelAdmin):
    model = Ingredient
    list_display = ('id', 'name', 'measurement_unit')
    list_editable = ('measurement_unit',)
    search_fields = ('name',)


class RecipeAdmin(admin.ModelAdmin):
    model = Recipe
    list_display = ('id', 'name', 'author', 'get_tag')
    list_editable = ('name',)
    list_filter = ('tag',)
    search_fields = ('name', 'author')

    def get_tag(self, obj):
        return [tag.name for tag in obj.tag.all()]


class TagAdmin(admin.ModelAdmin):
    model = Tag
    list_display = ('id', 'name', 'slug')
    list_editable = ('name', 'slug')


class UserAdmin(BaseUserAdmin):
    model = User
    list_display = (
        'id', 'username', 'first_name', 'last_name',
        'email', 'is_staff', 'is_superuser'
    )
    list_editable = ('first_name', 'last_name', 'is_staff', 'is_superuser')
    list_filter = ('username', 'email')


admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(User, UserAdmin)