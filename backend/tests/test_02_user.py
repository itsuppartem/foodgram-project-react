import pytest

from django.contrib.auth import get_user_model


User = get_user_model()


class TestUsersAuth:
    url_register = '/api/auth/users/'
    url_login = '/api/auth/token/login/'
    url_logout = '/api/auth/token/logout/'
    url_change_pass = '/api/users/set_password/'

    user_dict = dict(
        username='testuser3',
        password='123456Qqre123',
        email='test2@ya.ru',
        first_name='Test2',
        last_name='Test2',
    )


    @pytest.mark.django_db(transaction=True)
    def test_login(self, testuser, client):
        response = client.post(
            self.url_login,
            dict(email=testuser.email, password='123456Qqre123'),
        )

        assert response.status_code == 200, (
            f'Проверьте, что при POST запросе`{self.url_login}` '
            'возвращается статус 200'
        )

    @pytest.mark.django_db(transaction=True)
    def test_logout(self, client_auth):
        response = client_auth.post(self.url_logout)

        assert response.status_code != 403, (
            f'Проверьте, что при POST запросе`{self.url_logout}` '
            'не возвращается статус 403. Учетные данные не были предоставлены!'
        )
        assert response.status_code == 204, (
            f'Проверьте, что при POST запросе`{self.url_logout}` '
            'возвращается статус 204'
        )
