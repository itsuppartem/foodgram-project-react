import pytest


class TestTags:
    url_tags = '/api/tags/'
    url_tag_1 = '/api/tags/1/'
    url_tag_2 = '/api/tags/2/'
    url_tag_3 = '/api/tags/3/'

    @pytest.mark.django_db(transaction=True)
    def test_tag_list(self, client, tags_list):
        response = client.get(self.url_tags)

        tag_id = [obj['id'] for obj in response.data]
        name = [obj['name'] for obj in response.data]
        slug = [obj['slug'] for obj in response.data]
        color = [obj['color'] for obj in response.data]

        assert tag_id == [1, 2, 3], (
            f'Проверьте, что при GET запросе на `{self.url_tags}` '
            'корректно создаются ID тэгов'
        )
        assert name == ['Завтрак', 'Обед', 'Ужин'], (
            f'Проверьте, что при GET запросе на `{self.url_tags}` '
            'корректно создаются имена тэгов'
        )
        assert slug == ['breakfast', 'lunch', 'dinner'], (
            f'Проверьте, что при GET запросе на `{self.url_tags}` '
            'корректно создается slug тэгов'
        )
        assert color == ['#E26C2D', '#32CD32', '#000080'], (
            f'Проверьте, что при GET запросе на `{self.url_tags}` '
            'корректно создаются цвета тэгов'
        )

        assert response.status_code == 200, (
            f'Проверьте, что при GET запросе`{self.url_tags}` '
            'возвращается статус 200'
        )

    @pytest.mark.django_db(transaction=True)
    def test_get_tag(self, client, tags_list):
        response_tag_1 = client.get(self.url_tag_1)
        data_1 = response_tag_1.data

        assert data_1['id'] == 1, (
            f'Проверьте, что при GET запросе на `{self.url_tag_1}` '
            'корректно возвращается id тэга'
        )

        assert data_1['name'] == 'Завтрак', (
            f'Проверьте, что при GET запросе на `{self.url_tag_1}` '
            'корректно возвращается имя тэга'
        )

        assert data_1['slug'] == 'breakfast', (
            f'Проверьте, что при GET запросе на `{self.url_tag_1}` '
            'корректно возвращается slug тэга'
        )

        assert data_1['color'] == '#E26C2D', (
            f'Проверьте, что при GET запросе на `{self.url_tag_1}` '
            'корректно возвращается цвет тэга'
        )

        assert response_tag_1.status_code != 404, (
            f'Проверьте, что при GET запросе`{self.url_tag_1}` '
            'не возвращается статус 404. Страница не найдена!'
        )

        assert response_tag_1.status_code == 200, (
            f'Проверьте, что при GET запросе`{self.url_tag_1}` '
            'возвращается статус 200'
        )

        response_tag_2 = client.get(self.url_tag_2)
        data_2 = response_tag_2.data

        assert data_2['id'] == 2, (
            f'Проверьте, что при GET запросе на `{self.url_tag_2}` '
            'корректно возвращается id тэга'
        )

        assert data_2['name'] == 'Обед', (
            f'Проверьте, что при GET запросе на `{self.url_tag_2}` '
            'корректно возвращается имя тэга'
        )

        assert data_2['slug'] == 'lunch', (
            f'Проверьте, что при GET запросе на `{self.url_tag_2}` '
            'корректно возвращается slug тэга'
        )

        assert data_2['color'] == '#32CD32', (
            f'Проверьте, что при GET запросе на `{self.url_tag_2}` '
            'корректно возвращается цвет тэга'
        )

        assert response_tag_2.status_code != 404, (
            f'Проверьте, что при GET запросе`{self.url_tag_2}` '
            'не возвращается статус 404. Страница не найдена!'
        )

        assert response_tag_2.status_code == 200, (
            f'Проверьте, что при GET запросе`{self.url_tag_2}` '
            'возвращается статус 200'
        )

        response_tag_3 = client.get(self.url_tag_3)
        data_3 = response_tag_3.data

        assert data_3['id'] == 3, (
            f'Проверьте, что при GET запросе на `{self.url_tag_3}` '
            'корректно возвращается id тэга'
        )

        assert data_3['name'] == 'Ужин', (
            f'Проверьте, что при GET запросе на `{self.url_tag_3}` '
            'корректно возвращается имя тэга'
        )

        assert data_3['slug'] == 'dinner', (
            f'Проверьте, что при GET запросе на `{self.url_tag_3}` '
            'корректно возвращается slug тэга'
        )

        assert data_3['color'] == '#000080', (
            f'Проверьте, что при GET запросе на `{self.url_tag_3}` '
            'корректно возвращается цвет тэга'
        )

        assert response_tag_3.status_code != 404, (
            f'Проверьте, что при GET запросе`{self.url_tag_3}` '
            'не возвращается статус 404. Страница не найдена!'
        )

        assert response_tag_3.status_code == 200, (
            f'Проверьте, что при GET запросе`{self.url_tag_3}` '
            'возвращается статус 200'
        )
