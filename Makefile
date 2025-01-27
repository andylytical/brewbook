DIRNAME := $(shell basename $$(pwd))
HOME := $(shell echo $$HOME)

help:
	echo "Synopsis: make [init up down web db clean bkup reset]"

init:
	docker compose run web django-admin startproject $(DIRNAME) .

up down:
	docker compose $@

web db:
	docker container exec -it $(DIRNAME)-$@-1 /bin/bash

clean:
	docker compose down
	docker compose rm -f
	docker container prune -f
	docker images | awk '/$(DIRNAME)/ {print $$3}' | xargs -r docker rmi
	docker system prune -a -f
	bash $@.sh

bkup:
	bash $@.sh

reset: bkup clean
