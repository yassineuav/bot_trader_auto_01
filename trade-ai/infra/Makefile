.PHONY: up down migrate createsuperuser

up:
docker-compose up --build

down:
docker-compose down

migrate:
docker-compose run --rm backend python manage.py migrate

createsuperuser:
docker-compose run --rm backend python manage.py createsuperuser
