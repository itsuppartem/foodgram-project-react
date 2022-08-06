from django.conf.urls import include
from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import (FavoriteView, IngredientsView, RecipeView,
                    ShoppingCartView, TagView, download_shopping_cart)

#This block defines the URLs that will provide access to each view.

router = DefaultRouter()
router.register(r"tags", TagView, basename="tags")
router.register(r"ingredients", IngredientsView, basename="ingredients")
router.register(r"recipes", RecipeView, basename="recipes")

urlpatterns = [
    path(
        "recipes/download_shopping_cart/",
        download_shopping_cart,
        name="download",
    ),
    path(
        "recipes/<int:recipe_id>/favorite/",
        FavoriteView.as_view(),
        name="favorite",
    ),
    path(
        "recipes/<int:recipe_id>/shopping_cart/",
        ShoppingCartView.as_view(),
        name="shopping_cart",
    ),
    path("", include(router.urls)),
]
