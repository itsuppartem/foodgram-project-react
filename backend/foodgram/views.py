from django.contrib.auth import get_user_model
from django.db.models import F, Sum
from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.views import APIView

from . import models, serializers
from .filters import IngredientFilter, RecipeFilter
from .pagination import CartCustomPagination
from .permissions import IsOwnerOrReadOnly
from .utils import custom_delete, custom_post

User = get_user_model()


class IngredientsView(viewsets.ModelViewSet):
    """
    Handler function for the processing of the Ingredient objects through
    GET request
    """
    queryset = models.Ingredient.objects.all()
    serializer_class = serializers.IngredientSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, ]
    filter_class = IngredientFilter
    search_fields = ("^name",)
    pagination_class = None


class TagView(viewsets.ModelViewSet):
    """
    Handler function for the processing of the Tag objects through
    GET request
    """
    queryset = models.Tag.objects.all()
    serializer_class = serializers.TagSerializer
    permissions = (AllowAny,)
    pagination_class = None


class RecipeView(viewsets.ModelViewSet):
    """
    Handler function for the processing of the Recipe objects through
    the further requests: GET, POST, PATCH, DEL.
    """
    queryset = models.Recipe.objects.all()
    serializer_class = serializers.CreateRecipeSerializer
    permissions = (IsOwnerOrReadOnly,)
    filterset_class = RecipeFilter
    pagination_class = CartCustomPagination

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
    """
    Handler function for the processing GET, POST, DEL requests for
    Favourite objects.
    """
    permission_classes = [
        IsAuthenticatedOrReadOnly,
    ]
    pagination_class = CartCustomPagination
    filter_backends = (DjangoFilterBackend,)

    def get_queryset(self):
        user = self.request.user
        return models.Favorite.objects.filter(user=user)

    def post(self, request, recipe_id):
        return custom_post(self, request,
                           recipe_id, serializers.FavoriteSerializer, "recipe")

    def delete(self, request, recipe_id):
        return custom_delete(self, request, recipe_id, models.Favorite)


class ShoppingCartView(APIView):
    """
    Handler function for the processing GET, POST, DEL requests for
    Buying list objects.
    """
    permission_classes = [IsAuthenticatedOrReadOnly, ]
    serializer_class = serializers.ShoppingCartSerializer
    filterset_class = RecipeFilter
    pagination_class = CartCustomPagination
    queryset = models.ShoppingCart.objects.all()

    def post(self, request, recipe_id):
        return custom_post(self, request, recipe_id,
                           serializers.ShoppingCartSerializer, "recipe")

    def delete(self, request, recipe_id):
        return custom_delete(self, request, recipe_id, models.ShoppingCart)


# Action for downloading a buying list, processing GET request
@api_view(["GET"])
@permission_classes([IsAuthenticatedOrReadOnly])
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
