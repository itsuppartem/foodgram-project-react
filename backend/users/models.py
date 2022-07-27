from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ("username", "first_name", "last_name")

    username = models.CharField(
        "Имя пользователя",
        max_length=150,
        unique=True,
    )
    email = models.EmailField(
        "Электронная почта",
        max_length=254,
        unique=True,
    )
    first_name = models.CharField(
        "Имя",
        max_length=150,
    )
    last_name = models.CharField(
        "Фамилия",
        max_length=150,
    )


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="follower")
    following = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="following")

    class Meta:
        verbose_name = "Фоллоу"
        verbose_name_plural = "Фоллоус"
        constraints = [
            models.UniqueConstraint(fields=['user', 'following'],
                                    name='unique_follow')
        ]

    def __str__(self):
        return f'{self.following} {self.user}'
