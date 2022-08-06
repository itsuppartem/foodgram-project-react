from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    This model is used to create User
    """
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ("username", "first_name", "last_name")

    username = models.CharField(
        "Username",
        max_length=150,
        unique=True,
    )
    email = models.EmailField(
        "Email",
        max_length=254,
        unique=True,
    )
    first_name = models.CharField(
        "Name",
        max_length=150,
    )
    last_name = models.CharField(
        "Surname",
        max_length=150,
    )
    is_subscribed = models.BooleanField(
        default=False,
        verbose_name='Subsribed boolean',
        help_text='True for subscribe'
    )


class Follow(models.Model):
    """
    This model is used to create Subscription
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="follower")
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="following")

    class Meta:
        verbose_name = "Subscription"
        verbose_name_plural = "Subscriptions"
        constraints = [
            models.UniqueConstraint(fields=['user', 'author'],
                                    name='unique_follow')
        ]

    def __str__(self):
        return f'{self.author} {self.user}'
