.DEFAULT_GOA:=help

help: ##Display this help
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m<target>\033[0m\n\nTargets:\n"} /^[a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 }' $(MAKEFILE_LIST)

start: ##Start all containers in background
	docker-compose up -d

start-build: ##Start all containers in background with building
	docker-compose up -d --build

stop: ##Stop all containers
	docker-compose down

test-backend:##Test backend
	docker-compose exec backend python manage.py test

black: ##Run black in backend
	docker-compose exec backend black .

black-check:##Check black in backend
	docker-compose exec backend black --check .

flake-check:
	docker-compose exec backend flake8 --config=.flake8