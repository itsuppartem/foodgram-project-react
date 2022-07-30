from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .models import Follow
from .serializers import (CustomUserSerializer, FollowerSerializer,
                          PasswordSerializer, RepresentationFollowerSerializer)

User = get_user_model()


class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [
        AllowAny,
    ]
    pagination_class = None

    @action(
        methods=["get"], detail=False, permission_classes=[IsAuthenticated]
    )
    def me(self, request, *args, **kwargs):
        user = get_object_or_404(User, pk=request.user.id)
        serializer = CustomUserSerializer(user)
        return Response(serializer.data)

    def perform_create(self, serializer):
        if "password" in self.request.data:
            password = make_password(self.request.data["password"])
            serializer.save(password=password)
        else:
            serializer.save()

    def perform_update(self, serializer):
        if "password" in self.request.data:
            password = make_password(self.request.data["password"])
            serializer.save(password=password)
        else:
            serializer.save()

    @action(["post"], detail=False)
    def set_password(self, request, *args, **kwargs):
        user = self.request.user
        serializer = PasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user.save()
        return Response({"status": "пароль установлен"})

    @action(
        methods=["delete", "post"],
        detail=True,
        permission_classes=[IsAuthenticated],
    )
    def subscribe(self, request, pk=None):
        user = request.user
        following = get_object_or_404(User, pk=pk)
        follow = Follow.objects.filter(user=user, following=following)
        data = {"user": user.id, "following": following.id, }
        if request.method == "POST":
            serializer = FollowerSerializer(data=data, context=request)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        elif request.method == "DELETE":
            follow.delete()
            return Response("Удалено", status=status.HTTP_204_NO_CONTENT)
        else:
            return None

    @action(
        methods=["get"],
        detail=False,
        permission_classes=[IsAuthenticated],
    )
    def subscriptions(self, request):
        user_obj = User.objects.filter(following__user=request.user)
        paginator = PageNumberPagination()
        paginator.page_size = 6
        result_page = paginator.paginate_queryset(user_obj, request)
        serializer = RepresentationFollowerSerializer(
            result_page, many=True, context={'current_user': request.user})
        return paginator.get_paginated_response(serializer.data)
