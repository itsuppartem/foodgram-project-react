import pytest
import django
import os

from django.contrib.auth import get_user_model


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")

django.setup()

User = get_user_model()


@pytest.fixture()
def testuser():
    return User.objects.create_user(
        username='test_user',
        password='123456Qqre123',
        email='test13@ya.ru',
        first_name='Test13',
        last_name='Test13',
    )


@pytest.fixture()
def testuser2():
    return User.objects.create_user(
        username='test_user2',
        password='123456Qqre123',
        email='test14@ya.ru',
        first_name='Test14',
        last_name='Test14',
    )


@pytest.fixture()
def token(testuser):
    from rest_framework.authtoken.models import Token

    Token.objects.create(user=testuser)
    return Token.objects.get(user=testuser)


@pytest.fixture()
def client():
    from rest_framework.test import APIClient

    return APIClient()


@pytest.fixture()
def client_auth(token):
    from rest_framework.test import APIClient

    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
    return client


@pytest.fixture()
def first_user():
    return User.objects.filter(username='test_user').first()


@pytest.fixture()
def ingredients_list():
    from foodgram.models import Ingredient

    data = [
        {'id': 1, 'name': 'жижа', 'measurement_unit': 'л'},
        {'id': 2, 'name': 'пальцы', 'measurement_unit': 'кг'},
        {'id': 3, 'name': 'пудра', 'measurement_unit': 'гр'},
    ]
    for ingredient in data:
        id, name, measurement_unit = ingredient.values()
        Ingredient.objects.create(
            id=id, name=name, measurement_unit=measurement_unit,
        )
    return data


@pytest.fixture()
def tags_list():
    from foodgram.models import Tag

    data = [
        {'id': 1, 'name': 'Завтрак', 'slug': 'breakfast', 'color': '#E26C2D'},
        {'id': 2, 'name': 'Обед', 'slug': 'lunch', 'color': '#32CD32'},
        {'id': 3, 'name': 'Ужин', 'slug': 'dinner', 'color': '#000080'},
    ]
    for tag in data:
        id, name, slug, color = tag.values()
        Tag.objects.create(id=id, name=name, slug=slug, color=color)
    return data
