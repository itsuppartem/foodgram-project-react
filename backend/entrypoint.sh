python3 manage.py makemigrations users

python3 manage.py makemigrations recipes

python3 manage.py migrate --no-input

python3 manage.py collectstatic --no-input

gunicorn backend.foodgram.wsgi:application --bind 0.0.0.0:8000