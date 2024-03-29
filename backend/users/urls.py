from django.conf.urls import include
from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import CustomUserViewSet

# This block defines the URLs that will provide access to each view.

router = DefaultRouter()
router.register("users", CustomUserViewSet)
urlpatterns = [
    path("auth/", include("djoser.urls.authtoken")),
    path("", include(router.urls)),

]
