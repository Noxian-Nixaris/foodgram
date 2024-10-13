from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from foodgram.models import (
    Favorite,
    Ingredient,
    Recipe,
    RecipeIngredient,
    RecipeTag,
    ShoppingCart,
    ShortURL,
    Tag
)
from users_authentication.models import User


class IngredientInlineAdmin(admin.TabularInline):
    model = RecipeIngredient
    extra = 0
    min_num = 1


class TagInlineAdmin(admin.TabularInline):
    model = RecipeTag
    extra = 0
    min_num = 1


class IngredientAdmin(admin.ModelAdmin):
    model = Ingredient
    list_display = ('id', 'name', 'measurement_unit')
    list_editable = ('measurement_unit',)
    search_fields = ('name',)


class RecipeAdmin(admin.ModelAdmin):
    model = Recipe
    list_display = ('id', 'name', 'author', 'get_tag', 'pub_date')
    readonly_fields = ('add_counter',)
    list_editable = ('name',)
    list_filter = ('tags',)
    search_fields = ('name', 'author')
    inlines = [IngredientInlineAdmin, TagInlineAdmin]

    def get_tag(self, obj):
        return [tag.name for tag in obj.tags.all()]

    def add_counter(self, obj):
        return Favorite.objects.filter(favorite=obj).count()


class FavoriteAdmin(admin.ModelAdmin):
    model = Favorite
    list_display = ('user', 'favorite')


class TagAdmin(admin.ModelAdmin):
    model = Tag
    list_display = ('id', 'name', 'slug')
    list_editable = ('name', 'slug')


class UserAdmin(BaseUserAdmin):
    model = User
    list_display = (
        'id', 'username', 'first_name', 'last_name',
        'email', 'avatar', 'is_staff', 'is_superuser'
    )
    list_editable = ('first_name', 'last_name', 'is_staff', 'is_superuser')
    search_fields = ('username', 'email')


class ShoppingCartAdmin(admin.ModelAdmin):
    model = ShoppingCart
    list_display = ('user', 'recipe')
    search_fields = ('name',)


class ShortURLAdmin(admin.ModelAdmin):
    model = ShortURL
    list_display = ('full_link', 'short_link')


admin.site.register(Favorite, FavoriteAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(ShoppingCart, ShoppingCartAdmin)
admin.site.register(ShortURL, ShortURLAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(User, UserAdmin)
