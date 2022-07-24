from django.contrib import admin

from . import models

admin.site.register(models.Tag)
admin.site.register(models.IngredientInRecipe)


class IngredientsInTable(admin.TabularInline):
    model = models.Recipe.ingredients.through


@admin.register(models.Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ("user", "recipe")


@admin.register(models.Recipe)
class RecipeAdmin(admin.ModelAdmin):
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
    list_display = ("name", "measurement_unit")
    search_fields = ("name",)
    list_filter = ("name",)
