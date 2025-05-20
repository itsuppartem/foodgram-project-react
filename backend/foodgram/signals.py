from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError

from .models import Recipe, IngredientInRecipe

@receiver(pre_save, sender=Recipe)
def validate_recipe(sender, instance, **kwargs):
    if instance.cooking_time < 1:
        raise ValidationError('Время приготовления должно быть больше 0')
    if not instance.ingredients.exists():
        raise ValidationError('Рецепт должен содержать хотя бы один ингредиент')
    if not instance.tags.exists():
        raise ValidationError('Рецепт должен содержать хотя бы один тег')

@receiver(pre_save, sender=IngredientInRecipe)
def validate_ingredient_amount(sender, instance, **kwargs):
    if instance.amount is not None and instance.amount < 1:
        raise ValidationError('Количество ингредиента должно быть больше 0') 