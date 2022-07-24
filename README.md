# **Foodgram project**
[![Python](https://img.shields.io/badge/-Python-464646?style=flat-square&logo=Python)](https://www.python.org/)
[![Django](https://img.shields.io/badge/-Django-464646?style=flat-square&logo=Django)](https://www.djangoproject.com/)
[![Django REST Framework](https://img.shields.io/badge/-Django%20REST%20Framework-464646?style=flat-square&logo=Django%20REST%20Framework)](https://www.django-rest-framework.org/)
[![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-464646?style=flat-square&logo=PostgreSQL)](https://www.postgresql.org/)
[![Nginx](https://img.shields.io/badge/-NGINX-464646?style=flat-square&logo=NGINX)](https://nginx.org/ru/)
[![gunicorn](https://img.shields.io/badge/-gunicorn-464646?style=flat-square&logo=gunicorn)](https://gunicorn.org/)
[![docker](https://img.shields.io/badge/-Docker-464646?style=flat-square&logo=docker)](https://www.docker.com/)
### Фудграм

# Описание

**«Фудграм»** - это сайт, на котором пользователи могут _публиковать_ рецепты, добавлять чужие рецепты в _избранное_ и _подписываться_ на публикации других авторов. На сайте есть **«Список покупок»**, он позволяет пользователям создавать список продуктов, которые нужно купить для приготовления выбранных блюд.

# Запуск на локальной машине

- Создать .env  и поместить в backend\infra\
    DB_ENGINE=<django.db.backends.postgresql>
    DB_NAME=<имя базы данных postgres>
    DB_USER=<пользователь бд>
    DB_PASSWORD=<пароль>
    DB_HOST=<db>
    DB_PORT=<5432>
    SECRET_KEY=<секретный ключ проекта django>


- cd infra
- docker-compose up -d
- docker-compose exec backend python manage.py collectstatic --noinput
- docker-compose exec web python manage.py migrate
- docker-compose exec web python manage.py load_tags
- docker-compose exec web python manage.py load_ingredients
- docker-compose exec web python manage.py createsuperuser

# В проекте реализовано немножечко тестов

- Запуск по команде pytest