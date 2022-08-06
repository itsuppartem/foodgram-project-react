from django.contrib import admin

from . import models

#Provides a quick, model-centric interface, that does not need to specify any fields or make custom parameters
admin.site.register(models.Tag)
admin.site.register(models.IngredientInRecipe)


class IngredientsInTable(admin.TabularInline):
    """
    Adds and shows realation between IngredientInRecipe model
    and Recipe model in Admin-zone
    """
    model = models.Recipe.ingredients.through


@admin.register(models.Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    """
    Adds and shows specifed fields of
    Favorite model in Admin-zone.
    Names of constants speak for themselves.
    """
    list_display = ("user", "recipe")


@admin.register(models.Recipe)
class RecipeAdmin(admin.ModelAdmin):
    """
    Adds and shows specifed fields of
    Recipe model in Admin-zone.
    fan_count is automatically calculated field.
    Names of constants speak for themselves.
    """
    inlines = [
        IngredientsInTable,
    ]
    list_display = ("name", "author", "fan_count")
    list_filter = ("author", "name", "tags",)
    search_fields = ("author", "name", "tags",)
    readonly_fields = ("fan_count",)

    def fan_count(self, obj):
        return models.Favorite.objects.filter(recipe=obj).count()


@admin.register(models.Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    """
    Adds and shows specifed fields of
    Ingredient model in Admin-zone.
    Names of constants speak for themselves.
    """
    list_display = ("name", "measurement_unit")
    search_fields = ("name",)
    list_filter = ("name",)
