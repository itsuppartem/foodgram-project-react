from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from users.serializers import CustomUserSerializer
from . import models


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Tag
        fields = ["id", "name", "color", "slug"]


class IngredientInRecipeSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(
        queryset=models.Ingredient.objects.all(),
    )
    name = serializers.SlugRelatedField(
        source="ingredient", read_only=True, slug_field="name"
    )
    measurement_unit = serializers.SlugRelatedField(
        source="ingredient", read_only=True, slug_field="measurement_unit"
    )

    class Meta:
        model = models.IngredientInRecipe
        fields = ("id", "name", "measurement_unit", "amount")


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Ingredient
        fields = ["id", "name", "measurement_unit"]


class ShowRecipeSerializer(serializers.ModelSerializer):
    tags = TagSerializer(read_only=True, many=True)
    image = Base64ImageField()
    author = CustomUserSerializer(read_only=True)
    ingredients = IngredientInRecipeSerializer(
        source="ingredients_amount",
        many=True
    )
    is_favorited = serializers.SerializerMethodField("get_is_favorited")
    is_in_shopping_cart = serializers.SerializerMethodField(
        "get_is_in_shopping_cart"
    )

    class Meta:
        model = models.Recipe
        fields = [
            "id",
            "tags",
            "author",
            "ingredients",
            "is_favorited",
            "is_in_shopping_cart",
            "name",
            "image",
            "text",
            "cooking_time",
        ]

    def get_is_favorited(self, obj):
        request = self.context.get("request")
        if request is None or request.user.is_anonymous:
            return False
        user = request.user
        return models.Favorite.objects.filter(recipe=obj, user=user).exists()

    def get_is_in_shopping_cart(self, obj):
        request_user = self.context["request"].user
        if request_user.is_anonymous:
            return False
        return models.ShoppingCart.objects.filter(
            user=request_user,
            recipe=obj).exists()


class AddIngredientToRecipeSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(
        queryset=models.Ingredient.objects.all()
    )

    class Meta:
        model = models.IngredientInRecipe
        fields = ("id", "amount")


class CreateRecipeSerializer(serializers.ModelSerializer):
    image = Base64ImageField(max_length=None, use_url=True)
    author = CustomUserSerializer(read_only=True)
    ingredients = AddIngredientToRecipeSerializer(many=True)
    cooking_time = serializers.IntegerField()
    tags = serializers.SlugRelatedField(
        many=True, queryset=models.Tag.objects.all(), slug_field="id"
    )

    class Meta:
        model = models.Recipe
        fields = [
            "tags",
            "author",
            "ingredients",
            "name",
            "image",
            "text",
            "cooking_time",
        ]

    def validate_ingredients(self, data):
        ingredients = data['ingredients']
        ingredients_list = []
        for ingredient in ingredients:
            ingredient_id = ingredient['id']
            if ingredient_id in ingredients_list:
                raise serializers.ValidationError(
                    {"Ингредиент уже есть в списке"})
        return data

    def validate_cooking_time(self, data):
        if data <= 0:
            raise serializers.ValidationError("Введите число больше 0")
        return data

    def create_bulk(self, recipe, ingredients_data):
        models.IngredientInRecipe.objects.bulk_create(
            [models.IngredientInRecipe(
                ingredient=ingredient["id"],
                recipe=recipe,
                amount=ingredient['amount']
            ) for ingredient in ingredients_data])

    def create(self, validated_data):
        request = self.context.get('request')
        ingredients_data = validated_data.pop('ingredients')
        tags_data = validated_data.pop('tags')
        recipe = models.Recipe.objects.create(author=request.user,
                                              **validated_data)
        recipe.tags.set(tags_data)
        self.create_bulk(recipe, ingredients_data)
        return recipe

    def update(self, instance, validated_data):
        ingredients_data = validated_data.pop('ingredients')
        tags_data = validated_data.pop('tags')
        models.TagsInRecipe.objects.filter(recipe=instance).delete()
        models.IngredientInRecipe.objects.filter(recipe=instance).delete()
        self.create_bulk(instance, ingredients_data)
        instance.tags.set(tags_data)
        return super().update(instance, validated_data)


class FavoriteSerializer(serializers.ModelSerializer):
    recipe = serializers.PrimaryKeyRelatedField(
        queryset=models.Recipe.objects.all()
    )
    user = serializers.PrimaryKeyRelatedField(
        queryset=models.User.objects.all()
    )

    class Meta:
        model = models.Favorite
        fields = ["recipe", "user"]
        validators = [
            UniqueTogetherValidator(
                queryset=models.Favorite.objects.all(),
                fields=('user', 'recipe'),
                message='Рецепт уже добавлен в избранное'
            )
        ]


class ShoppingCartSerializer(FavoriteSerializer):
    class Meta:
        model = models.ShoppingCart
        fields = ["recipe", "user"]
