DIRNAME := $(shell basename $$(pwd))
HOME := $(shell echo $$HOME)

init:
	docker compose run web django-admin startproject $(DIRNAME) .

run:
	docker compose up

bash:
	docker container exec -it $(DIRNAME)-web-1 /bin/bash

stop:
	docker compose down

clean:
	docker compose down
	docker compose rm -f
	docker container prune -f
	docker images | awk '/$(DIRNAME)/ {print $$3}' | xargs -r docker rmi
	docker system prune -f
