# Dev stage

# Build docker image on base settings
build:
	docker-compose build

# Run app on dev settings with migrations and creating premium group
setup:
	docker-compose build
	docker-compose up -d
	docker-compose exec django python manage.py makemigrations
	docker-compose exec django python manage.py migrate
	docker-compose exec django python manage.py collectstatic


# Set up containers on dev settings then test and if tests pass stop and remove all containers.
test:
	docker-compose build
	docker-compose up -d
	docker-compose exec django python manage.py makemigrations
	docker-compose exec django python manage.py migrate
	docker-compose exec django coverage run --source='.' manage.py test && flake8
	docker-compose exec django coverage report -m
	docker-compose down -v

# Remove running containers
remove:
	docker-compose down -v
