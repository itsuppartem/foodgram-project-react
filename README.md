# **Foodgram aka «Grocery Assistant»**
[![Python](https://img.shields.io/badge/-Python-464646?style=flat-square&logo=Python)](https://www.python.org/)
[![Django](https://img.shields.io/badge/-Django-464646?style=flat-square&logo=Django)](https://www.djangoproject.com/)
[![Django REST Framework](https://img.shields.io/badge/-Django%20REST%20Framework-464646?style=flat-square&logo=Django%20REST%20Framework)](https://www.django-rest-framework.org/)
[![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-464646?style=flat-square&logo=PostgreSQL)](https://www.postgresql.org/)
[![Nginx](https://img.shields.io/badge/-NGINX-464646?style=flat-square&logo=NGINX)](https://nginx.org/ru/)
[![gunicorn](https://img.shields.io/badge/-gunicorn-464646?style=flat-square&logo=gunicorn)](https://gunicorn.org/)
[![docker](https://img.shields.io/badge/-Docker-464646?style=flat-square&logo=docker)](https://www.docker.com/)
[![GitHub%20Actions](https://img.shields.io/badge/-GitHub%20Actions-464646?style=flat-square&logo=GitHub%20actions)](https://github.com/features/actions)
[![Yandex.Cloud](https://img.shields.io/badge/-Yandex.Cloud-464646?style=flat-square&logo=Yandex.Cloud)](https://cloud.yandex.ru/)
### 
![example workflow](https://github.com/itsuppartem/foodgram-project-react/actions/workflows/foodgram_workflow.yml/badge.svg)


**«Foodgram»** - is django-based online service, with API(Django REST framework). 
Things that are avialable:

Full user authentication.
CRUD new recipe.
Filter by tags.
Choose from a bunch of ingredients.
Add to favourites.
Favourites page.
Follow another authors.
Add to shopping list.
Download shopping list.

# You can do test-clicking right now
*_______________________________________________
Home page http://51.250.98.29/signin
Admin zone http://51.250.98.29/admin/
API http://51.250.98.29/api/
API Redoc http://51.250.98.29/api/docs/

## Preparations for project launch
### Clone repository to your machine:
```
git clone https://github.com/itsuppartem/foodgram-project-react
```
## If you are using remote VM (ubuntu):
* Log in to your machine

* Install docker:
```
sudo apt install docker.io 
```
* install docker-compose:
```
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```
* Edit infra/default.conf in stirng "server_name" type your IP
* Copy docker-compose.yml and default.conf from infra directory to your remote VM:
```
scp docker-compose.yml <username>@<host>:/home/<username>/docker-compose.yml
scp default.conf <username>@<host>:/home/<username>/default.conf
```

* Create .env file, fullfill with conten below or just copy ".env example" and rename it:
    ```
    DB_ENGINE=django.db.backends.postgresql -Choose db engine
    DB_NAME=postgres -Db name
    POSTGRES_USER=postgres -Db connection login
    POSTGRES_PASSWORD=postgres -Db connection password
    DB_HOST=db -Name of the container
    DB_PORT=5432 -Port for db connection
    SECRET_KEY=example_key -django prject secret key
    ```
* If you want Workflow to work, add constants shown below to your Secrets GitHub:
    ```
    DB_ENGINE=<Choose db engine>
    DB_NAME=<Db name>
    POSTGRES_USER=<Db connection login>
    POSTGRES_PASSWORD=<Db connection password>
    DB_HOST=<Name of the container>
    DB_PORT=<Port for db connection>

    
    DOCKER_PASSWORD=<Docker pass>
    DOCKER_USERNAME=<Docker username>
    
    SECRET_KEY=<django prject secret key>

    USER=<remote VM user login>
    HOST=<IP>
    PASSPHRASE=<passphrase for ssh key>
    SSH_KEY=<Your SHH key (Command: cat ~/.ssh/id_rsa)>

    TELEGRAM_TO=<Telegram user ID>
    TELEGRAM_TOKEN=<Telegram bot token>
    ```
    Workflow consists of three steps:
     - PEP8 check
     - Build and push Backend and Frontend images to DockerHub.
     - Deploy on remote VM.
     - Greetings in telegram from bot if workflow succed.  
  
* Use build command of docker-compose:
```
sudo docker-compose up -d --build
```
* After succesful building use following commands:
    - Collect static files:
    ```
    sudo docker-compose exec backend python manage.py collectstatic --noinput
    ```
    - Apply migrations:
    ```
    sudo docker-compose exec backend python manage.py migrate --noinput
    ```
    - Load ingredients to db (no need if you dont want to):  
    ```
    sudo docker-compose exec backend python manage.py load_ingredients
    ```
    - Load tags to db (no need if you dont want to): 
    ```
    sudo docker-compose exec backend python manage.py load_tags
    ```
    - Create superuser:
    ```
    sudo docker-compose exec backend python manage.py createsuperuser
    ```
    - Enjoy your project

### Backend by:
Guliaev Artem / Гуляев Артем <br />
[Github](https://github.com/itsuppartem) <br />
[Email me](mailto:itsuppartem@yandex.ru)

### Frontend by:
https://github.com/yandex-praktikum/foodgram-project-react