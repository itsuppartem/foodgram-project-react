from django.contrib import admin

from . import models

admin.site.register(models.Follow)


class FollowAdmin(admin.ModelAdmin):
    list_display = ("user", "author")
    autocomplete_fields = ("author", "user")
    search_fields = ("user", "author",)


@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
    fields = ("username", "first_name", "last_name", "email")
    search_fields = ("username",)
    list_filter = ("username", "email")
    empty_value_display = "-пусто-"
    list_display = ("id", "username", "email", "first_name", "last_name")
