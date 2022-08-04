from djoser.serializers import UserCreateSerializer
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.validators import UniqueTogetherValidator

from foodgram.models import Recipe
from . import models


class CustomUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.User
        fields = ["id", "username", "email", "first_name", "last_name", ]


class CustomUserManipulateSerializer(UserCreateSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        fields = (
            "email",
            "id",
            "username",
            "first_name",
            "last_name",
            "password",
            "is_subscribed",
        )
        model = models.User

    def get_is_subscribed(self, obj):
        """Статус подписки на автора."""
        user_id = self.context.get('request').user.id
        return models.Follow.objects.filter(
            author=obj.id, user=user_id).exists()


class PasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(required=True)
    current_password = serializers.CharField(required=True)

    class Meta:
        model = models.User
        fields = "__all__"


class BaseRecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = (
            "id",
            "name",
            "image",
            "cooking_time",
        )


class TokenSerializer(serializers.ModelSerializer):
    token = serializers.CharField(source="key")

    class Meta:
        model = Token
        fields = ("token",)


class FollowerSerializer(serializers.ModelSerializer):
    def validate(self, data):
        user = data.get("user")
        author = data.get("author")
        if user == author:
            raise serializers.ValidationError("Невозможно подписаться на себя")
        return data

    class Meta:
        fields = ("user", "author")
        model = models.Follow
        validators = [
            UniqueTogetherValidator(
                queryset=models.Follow.objects.all(),
                fields=["user", "author"],
            )
        ]


class RepresentationFollowerSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source="author.id")
    email = serializers.ReadOnlyField(source="author.email")
    username = serializers.ReadOnlyField(source="author.username")
    first_name = serializers.ReadOnlyField(source="author.first_name")
    last_name = serializers.ReadOnlyField(source="author.last_name")
    is_subscribed = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = models.Follow
        fields = [
            "email",
            "id",
            "username",
            "first_name",
            "last_name",
            "is_subscribed",
            "recipes",
            "recipes_count",
        ]

    def get_is_subscribed(self, obj):
        """Статус подписки на автора."""
        user = self.context.get('request').user
        return models.Follow.objects.filter(
            author=obj.author, user=user).exists()

    def get_recipes(self, obj):
        request = self.context.get("request")
        limit = request.GET.get("recipes_limit")
        if limit is not None:
            queryset = Recipe.objects.filter(author=obj.author)[:int(limit)]
        else:
            queryset = obj.author.recipe_set.all()
        return BaseRecipeSerializer(queryset, many=True).data

    def get_recipes_count(self, obj):
        author = obj.author
        return Recipe.objects.filter(author=author).count()
