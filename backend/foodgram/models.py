from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models

User = get_user_model()


class Tag(models.Model):
    """
    This model is used to create tags.
    """
    name = models.CharField(
        max_length=250,
        verbose_name="Tag",
        help_text="Tags name")

    color = models.CharField(
        max_length=7,
        default="#ffffff",
        verbose_name="HEX colour",
        help_text="Tags colour")

    slug = models.SlugField(
        unique=True,
        verbose_name="Slug",
        help_text="Tags slug")

    class Meta:
        ordering = ["name"]
        verbose_name = "Tag"
        verbose_name_plural = "Tags"

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    """
    This model is used to create ingredients.
    """
    name = models.CharField(
        max_length=250,
        verbose_name="Ingredient",
        help_text="Input ingredients name"
    )

    measurement_unit = models.CharField(
        max_length=10,
        verbose_name="Measurement units",
        help_text="Input measurement units",
    )

    class Meta:
        ordering = ["name"]
        verbose_name = "Ingredient"
        verbose_name_plural = "Ingredients"
        constraints = [
            models.UniqueConstraint(fields=["name", "measurement_unit"],
                                    name="unique_ingredient")
        ]

    def __str__(self):
        return f"{self.name}, {self.measurement_unit}"


class Recipe(models.Model):
    """
    This model is used to create recipe
    """
    author = models.ForeignKey(
        User,
        verbose_name="Author",
        on_delete=models.CASCADE,
        related_name="recipes",
        help_text="This is the author of the recipe"
    )
    tags = models.ManyToManyField(
        Tag,
        through="TagsInRecipe",
        related_name="recipes",
        verbose_name="Tags",
        help_text="Choose recipes tags"
    )
    name = models.CharField(
        max_length=200,
        verbose_name="Name",
        help_text="Input recipes name"
    )
    text = models.TextField(
        default="",
        verbose_name="Description",
        help_text="How this thing should be cooked"
    )
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name="Cooking time",
        help_text="Input cooking time in minutes",
        validators=[MinValueValidator(1)],
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through="IngredientInRecipe",
        verbose_name="Ingredients",
        related_name="recipes",
        blank=True,
        help_text="Choose ingredients for your recipe"
    )
    pub_date = models.DateTimeField(
        auto_now_add=True, verbose_name="Publication time"
    )
    image = models.ImageField(
        "Image",
        upload_to="recipes/media/",
        blank=True,
        help_text="Upload image",
    )

    class Meta:
        ordering = ["-pub_date"]
        verbose_name = "Recipe"
        verbose_name_plural = "Recipes"

    def __str__(self):
        return self.name


class TagsInRecipe(models.Model):
    """
    This model is used to create several tags in recipe
    """
    tag = models.ForeignKey(
        Tag, verbose_name="Тag in recipe", on_delete=models.CASCADE
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = "Tags in recipe"
        verbose_name_plural = verbose_name


class IngredientInRecipe(models.Model):
    """
    This model is used to create several tags in recipe
    """
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        verbose_name="Ingredient in recipe",
        related_name="ingredients_amount",
    )
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE,
        verbose_name="Recipe",
        related_name="ingredients_amount",
    )
    amount = models.PositiveIntegerField(
        null=True, verbose_name="Amount value of ingredient"
    )

    class Meta:
        verbose_name = "Ingredients amount in recipe"
        verbose_name_plural = verbose_name
        constraints = [
            models.UniqueConstraint(fields=['ingredient', 'recipe'],
                                    name='unique_amount')
        ]


class Favorite(models.Model):
    """
    This model is used to favourite recipes
    """
    recipe = models.ForeignKey(
        Recipe,
        related_name="favorite",
        on_delete=models.CASCADE,
        verbose_name="Recipe",
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="User",
        related_name="favorite",
    )
    when_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-when_added"]
        verbose_name = "Favourited"
        verbose_name_plural = verbose_name
        constraints = [
            models.UniqueConstraint(fields=['user', 'recipe'],
                                    name='unique_favorite')
        ]

    def __str__(self):
        return f"{self.user} added {self.recipe}"


class ShoppingCart(models.Model):
    """
    This model is used to add recipe in Buying List
    """
    recipe = models.ForeignKey(
        Recipe,
        related_name="is_in_shopping_cart",
        on_delete=models.CASCADE,
        verbose_name="Recipe",
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="User",
        related_name="is_in_shopping_cart",
    )
    when_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Buying List"
        verbose_name_plural = verbose_name
        constraints = [
            models.UniqueConstraint(fields=['user', 'recipe'],
                                    name='unique_cart')
        ]

    def __str__(self):
        return f"{self.user} added {self.recipe}"
