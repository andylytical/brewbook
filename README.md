# Brewbook

# First time run
1. `export PROJECT_NAME=brewbook`
1. `git clone https://github.com/andylytical/django-dev-container.git "${PROJECT_NAME}"`
1. `cd "${PROJECT_NAME}"`
1. make init
1. `sudo chown -R $USER:$USER src/"${PROJECT_NAME}"/`
1. `sed -i -e '1 i import os' src/"${PROJECT_NAME}"/settings.py`
1. Set database connection params
   1. `vim src/"${PROJECT_NAME}"/settings.py`
      ```
      DATABASES = {
         'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.environ.get('POSTGRES_NAME'),
            'USER': os.environ.get('POSTGRES_USER'),
            'PASSWORD': os.environ.get('POSTGRES_PASSWORD'),
            'HOST': 'db',
            'PORT': 5432,
         }
      }
      ```
1. Start the server and make sure you can connect and it provides a response
   1. `make run`
   1. http://localhost:8000
      You should see the Django development screen with a rocket.

# Develop and test locally
1. Start development server
   * `make run`
1. Edit, test, repeat.
1. Stop dev server
   * `make stop`

# Clean up local dev images and containers
1. `make clean`

# References
* [Django in a container](https://github.com/docker/awesome-compose/tree/master/official-documentation-samples/django/)
* [Django Tutorial](https://docs.djangoproject.com/en/5.1/intro/tutorial01/)
