DOCKER_COMPOSE = docker-compose
DOCKER = docker
IMAGE_NAME = adventure_app
SERVICE_NAME = web

build:
	$(DOCKER) build -t $(IMAGE_NAME) .

up:
	$(DOCKER_COMPOSE) up --build -d

down:
	$(DOCKER_COMPOSE) down

clean:
	$(DOCKER_COMPOSE) down --volumes --rmi all --remove-orphans

rebuild: down build up
