from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from django.contrib import admin

from foodgram.models import Ingredient, Recipe, Tag


class IngredientAdmin(admin.ModelAdmin):
    model = Ingredient
    list_display = ('name', 'measurement_unit')
    list_editable = ('name', 'measurement_unit')
    search_fields = ('name')


class RecipeAdmin(admin.ModelAdmin):
    model = Recipe
    list_display = ('name', 'author', 'get_tag', 'score')
    list_editable = ('name', 'get_tag')
    list_filter = ('tag')
    search_fields = ('name', 'author')

    def get_tag(self, obj):
        return [tag.name for tag in obj.tag.all()]


class TagAdmin(admin.ModelAdmin):
    model = Tag
    list_display = ('name', 'slug')
    list_editable = ('name', 'slug')


class UserAdmin(BaseUserAdmin):
    model = User
    list_display = ('username', 'email', 'is staff', 'is_superuser')
    list_editable = ('is staff', 'is_superuser')
    list_filter = ('username', 'email')
