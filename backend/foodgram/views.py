from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from rest_framework import viewsets, status
from rest_framework.permissions import (AllowAny,
                                        IsAuthenticatedOrReadOnly,)
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.decorators import api_view, action
from rest_framework.views import APIView

from . import models, serializers
from .filters import IngredientFilter, RecipeFilter
from .permissions import IsOwnerOrReadOnly

User = get_user_model()


class IngredientsView(viewsets.ModelViewSet):
    queryset = models.Ingredient.objects.all()
    serializer_class = serializers.IngredientSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, ]
    filter_class = IngredientFilter
    search_fields = ("^name",)
    pagination_class = None


class TagView(viewsets.ModelViewSet):
    queryset = models.Tag.objects.all()
    serializer_class = serializers.TagSerializer
    permissions = (AllowAny,)
    pagination_class = None


class RecipeView(viewsets.ModelViewSet):
    queryset = models.Recipe.objects.all()
    serializer_class = serializers.CreateRecipeSerializer
    permissions = (IsOwnerOrReadOnly,)
    filterset_class = RecipeFilter
    pagination_class = PageNumberPagination

    def get_serializer_class(self):
        if self.request.method == "POST":
            return serializers.CreateRecipeSerializer
        if self.request.method == "PATCH":
            return serializers.CreateRecipeSerializer
        return serializers.ShowRecipeSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context


class FavoriteView(APIView):
    permission_classes = [
        IsAuthenticatedOrReadOnly,
    ]
    pagination_class = None
    filter_backends = (DjangoFilterBackend,)

    def get_queryset(self):
        user = self.request.user
        return models.Favorite.objects.filter(user=user)

    @action(methods=["post", ], detail=True,)
    def post(self, request, recipe_id):
        user = request.user
        data = {"user": user.id, "recipe": recipe_id, }
        if models.Favorite.objects.filter(
            user=user, recipe__id=recipe_id
        ).exists():
            return Response(
                {"Ошибка": "Уже в избранном"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        serializer = serializers.FavoriteSerializer(
            data=data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(methods=["DELETE", ], detail=True,)
    def delete(self, request, recipe_id):
        user = request.user
        recipe = get_object_or_404(models.Recipe, id=recipe_id)
        if not models.Favorite.objects.filter(
            user=user, recipe=recipe
        ).exists():
            return Response(status=status.HTTP_400_BAD_REQUEST)
        models.Favorite.objects.get(user=user, recipe=recipe).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ShoppingCartViewSet(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly, ]
    pagination_class = None
    serializer_class = serializers.ShoppingCartSerializer
    filterset_class = RecipeFilter

    @action(methods=["post", ], detail=False,)
    def post(self, request, recipe_id):
        user = request.user
        data = {"user": user.id, "recipe": recipe_id, }
        recipe = get_object_or_404(models.Recipe, id=recipe_id)
        if models.ShoppingCart.objects.filter(
            user=user, recipe=recipe
        ).exists():
            return Response(
                {"Ошибка": "Уже в корзине"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        serializer = serializers.ShoppingCartSerializer(
            data=data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(method=["delete", ], detail=False,)
    def delete(self, request, recipe_id):
        user = request.user
        recipe = get_object_or_404(models.Recipe, id=recipe_id)
        if not models.ShoppingCart.objects.filter(
            user=user, recipe=recipe
        ).exists():
            return Response(status=status.HTTP_400_BAD_REQUEST)
        models.ShoppingCart.objects.get(user=user, recipe=recipe).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["GET"])
def download_shopping_cart(request):
    shopping_cart = models.ShoppingCart.objects.filter(user=request.user)
    buying_list = {}
    for record in shopping_cart:
        recipe = record.recipe
        ingredients = models.IngredientInRecipe.objects.filter(recipe=recipe)
        for ingredient in ingredients:
            amount = ingredient.amount
            name = ingredient.ingredient.name
            measurement_unit = ingredient.ingredient.measurement_unit
            if name not in buying_list:
                buying_list[name] = {
                    "measurement_unit": measurement_unit,
                    "amount": amount,
                }
            else:
                buying_list[name]["amount"] = (
                    buying_list[name]["amount"] + amount
                )
    wishlist = []
    for name, data in buying_list.items():
        wishlist.append(
            f"{name} - {data['amount']} ({data['measurement_unit']})\n")
    pdfmetrics.registerFont(TTFont("RunicRegular", "data/RunicRegular.ttf",
                                   "UTF-8"))
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = ('attachment; '
                                       'filename="shopping_list.pdf"')
    page = canvas.Canvas(response)
    page.setFont('RunicRegular', size=32)
    page.drawString(200, 800, 'Список покупок')
    page.setFont('RunicRegular', size=18)
    height = 760
    for i, (name, data) in enumerate(buying_list.items(), 1):
        page.drawString(55, height, (f'{i}. {name} - {data["amount"]} '
                                     f'{data["measurement_unit"]}'))
        height -= 30
    page.showPage()
    page.save()
    return response
