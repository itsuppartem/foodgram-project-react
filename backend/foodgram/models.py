from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models

User = get_user_model()


class Tag(models.Model):
    name = models.CharField(
        max_length=250,
        verbose_name="Название тега",
        help_text="Введите название тега")

    color = models.CharField(
        max_length=7,
        default="#ffffff",
        verbose_name="Цветовой HEX-код",
        help_text="Введите цвет тега.")

    slug = models.SlugField(
        unique=True,
        verbose_name="Slug",
        help_text="Введите slug тега")

    class Meta:
        ordering = ["name"]
        verbose_name = "Тег"
        verbose_name_plural = "Теги"

    def __str__(self):
        return self.name


class Ingredient(models.Model):

    name = models.CharField(
        max_length=250,
        verbose_name="Название ингредиента",
        help_text="Введите название ингредиента."
    )

    measurement_unit = models.CharField(
        max_length=10,
        verbose_name="Единицы измерения",
        help_text="Введите единицы измерения",
    )

    class Meta:
        ordering = ["name"]
        verbose_name = "Ингредиент"
        verbose_name_plural = "Ингредиенты"
        constraints = [
            models.UniqueConstraint(fields=["name", "measurement_unit"],
                                    name="unique_ingredient")
        ]

    def __str__(self):
        return f"{self.name}, {self.measurement_unit}"


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        verbose_name="Автор публикации",
        on_delete=models.CASCADE,
        related_name="recipes",
        help_text="Автор рецепта"
    )
    tags = models.ManyToManyField(
        Tag,
        through="TagsInRecipe",
        related_name="recipes",
        verbose_name="Теги",
        help_text="Выберите теги для рецепта"
    )
    name = models.CharField(
        max_length=200,
        verbose_name="Название",
        help_text="Введите название рецепта"
    )
    text = models.TextField(
        default="",
        verbose_name="Описание рецепта",
        help_text="Введите описание рецепта"
    )
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name="Время приготовления",
        help_text="Время приготовления в минутах",
        validators=[MinValueValidator(1)],
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through="IngredientInRecipe",
        verbose_name="Ингредиенты",
        related_name="recipes",
        blank=True,
        help_text="Выберите ингредиенты для рецепта"
    )
    pub_date = models.DateTimeField(
        auto_now_add=True, verbose_name="Время публикации"
    )
    image = models.ImageField(
        "Изображение",
        upload_to="recipes/media/",
        blank=True,
        help_text="Добавить фото",
    )

    class Meta:
        ordering = ["-pub_date"]
        verbose_name = "Рецепт"
        verbose_name_plural = "Рецепты"

    def __str__(self):
        return self.name


class TagsInRecipe(models.Model):

    tag = models.ForeignKey(
        Tag, verbose_name="Тег в рецепте", on_delete=models.CASCADE
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = "Теги в рецепте"
        verbose_name_plural = verbose_name


class IngredientInRecipe(models.Model):
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        verbose_name="Ингредиент в рецепте",
        related_name="ingredients_amount",
    )
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE,
        verbose_name="Рецепт",
        related_name="ingredients_amount",
    )
    amount = models.PositiveIntegerField(
        null=True, verbose_name="Количество ингредиента"
    )

    class Meta:
        verbose_name = "Количетсво ингредиента в рецепте"
        verbose_name_plural = verbose_name
        constraints = [
            models.UniqueConstraint(fields=['ingredient', 'recipe'],
                                    name='unique_amount')
        ]


class Favorite(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        related_name="favorite",
        on_delete=models.CASCADE,
        verbose_name="Рецепт",
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
        related_name="favorite",
    )
    when_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-when_added"]
        verbose_name = "Список покупок"
        verbose_name_plural = verbose_name
        constraints = [
            models.UniqueConstraint(fields=['user', 'recipe'],
                                    name='unique_favorite')
        ]

    def __str__(self):
        return f"{self.user} added {self.recipe}"


class ShoppingCart(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        related_name="is_in_shopping_cart",
        on_delete=models.CASCADE,
        verbose_name="Рецепт",
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
        related_name="is_in_shopping_cart",
    )
    when_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Список покупок"
        verbose_name_plural = verbose_name
        constraints = [
            models.UniqueConstraint(fields=['user', 'recipe'],
                                    name='unique_cart')
        ]

    def __str__(self):
        return f"{self.user} added {self.recipe}"
