from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet as DjoserUserViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from foodgram.pagination import CartCustomPagination
from .models import Follow, User
from .serializers import (CustomUserManipulateSerializer, CustomUserSerializer,
                          FollowerSerializer, RepresentationFollowerSerializer)


class CustomUserViewSet(DjoserUserViewSet):
    queryset = User.objects.all()
    serializer_class = CustomUserManipulateSerializer
    permission_classes = [
        AllowAny,
    ]
    pagination_class = CartCustomPagination

    @action(
        methods=["get"], detail=False, permission_classes=[IsAuthenticated]
    )
    def me(self, request, *args, **kwargs):
        user = get_object_or_404(User, pk=request.user.id)
        serializer = CustomUserSerializer(user)
        return Response(serializer.data)

    @action(
        methods=["delete", "post"],
        detail=True,
        permission_classes=[IsAuthenticated],
    )
    def subscribe(self, request, id):
        user = request.user
        author = get_object_or_404(User, id=id)
        follow = Follow.objects.filter(user=user, author=author)
        data = {"user": user.id, "author": author.id, }
        if request.method == "POST":
            serializer = FollowerSerializer(data=data, context=request)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        follow.delete()
        return Response("Удалено", status=status.HTTP_204_NO_CONTENT)

    @action(
        methods=["get"],
        detail=False,
        permission_classes=[IsAuthenticated],
    )
    def subscriptions(self, request):
        user = request.user
        queryset = user.follower.all()
        pages = self.paginate_queryset(queryset)
        serializer = RepresentationFollowerSerializer(
            pages, many=True, context={"request": request}
        )
        return self.get_paginated_response(serializer.data)
