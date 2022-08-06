from django.apps import AppConfig


class UsersConfig(AppConfig):
    """
    Announcing that we have app, named USERS.
    """
    default_auto_field = "django.db.models.BigAutoField"
    name = "users"
