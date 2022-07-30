from django.contrib.auth import get_user_model
from django.db.models import F, Sum
from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.views import APIView

from . import models, serializers
from .filters import IngredientFilter, RecipeFilter
from .permissions import IsOwnerOrReadOnly
from .utils import custom_delete, custom_post

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

    def post(self, request, recipe_id):
        return custom_post(self, request,
                           recipe_id, serializers.FavoriteSerializer, "recipe")

    def delete(self, request, recipe_id):
        return custom_delete(self, request, recipe_id, models.Favorite)


class ShoppingCartViewSet(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly, ]
    pagination_class = None
    serializer_class = serializers.ShoppingCartSerializer
    filterset_class = RecipeFilter

    def post(self, request, recipe_id):
        return custom_post(self, request, recipe_id,
                           serializers.ShoppingCartSerializer, "recipe")

    def delete(self, request, recipe_id):
        return custom_delete(self, request, recipe_id, models.ShoppingCart)


@api_view(["GET"])
@permission_classes([IsAuthenticatedOrReadOnly])
def download_shopping_cart(request):
    user = request.user
    ingredients = models.IngredientInRecipe.objects.filter(
        recipe__in=(user.is_in_shopping_cart.values('recipe_id'))).values(
            ingredients=F('ingredient__name'),
            measure=F('ingredient__measurement_unit')).annotate(
                amount_sum=Sum('amount'))
    content = ([f'{item["ingredients"]} ({item["measure"]})'
               f'- {item["amount_sum"]}\n'
                for item in ingredients])
    response = HttpResponse(content, content_type='text/plain')
    response['Content-Disposition'] = (
        f'attachment; filename={"shopping_list.txt"}'
    )
    return response
