# django-api-recipes
Udemy course for Django REST API

# Docker notes
Test build from Dockerfile 

    ```docker build .```
    
Test build from docker-compose 

    ```docker-compose build```
    
Run a command in the docker container from command line. ex: python manage.py runserver

    ```docker-compose run app sh -c "python mange.py runserver"```
    

# Django-extensions
Produce a tab-separated list of (url_pattern, view_function, name) tuples
    ```python manage.py show_urls```

