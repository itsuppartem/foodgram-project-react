from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response

from .models import Recipe

# This is a repetitive code snippets that are used in
# ShoppingCartView and FavoriteView


def custom_post(self, request, id, custom_serializer, field):
    user = request.user
    data = {"user": user.id, field: id}
    serializer = custom_serializer(data=data, context={"request": request})
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)


def custom_delete(self, request, id, model):
    user = request.user
    recipe = get_object_or_404(Recipe, id=id)
    deleting_obj = model.objects.all().filter(user=user, recipe=recipe)
    deleting_obj.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
