# Brewbook

# First time run

Start containers
1. `make up`

Create DB
1. `make web`
   1. `python manage.py makemigrations`
   1. `python manage.py migrate`
   1. `python manage.py createsuperuser`

Restore DB contents
1. `make bkup`
1. `make db`
   1. `f="$(ls -t /var/lib/postgresql/data/*.sql | head -1)"`
   1. `psql -U $POSTGRES_USER --set ON_ERROR_STOP=on -d $POSTGRES_DB --single-transaction < "$f"`


# Develop and test locally
1. Start development server
   * `make up`
1. Edit, test, repeat.
1. Stop dev server
   * `make down`


# Clean up local dev images and containers
1. `make clean`


# References
* [Django in a container](https://github.com/docker/awesome-compose/tree/master/official-documentation-samples/django/)
* [Django Tutorial](https://docs.djangoproject.com/en/5.1/intro/tutorial01/)
