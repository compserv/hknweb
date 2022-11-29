hknweb
======

Welcome! This is the *in-progress website redesign* for the [IEEE-Eta Kappa Nu (HKN)](https://hkn.ieee.org/) [University of California, Berkeley Mu Chapter](https://dev-hkn.eecs.berkeley.edu/), built with [Django](https://www.djangoproject.com/), [Django REST framework](https://www.django-rest-framework.org/), and [Vue.js](https://vuejs.org/).

## Setup
We use any `sh` shell e.g. `bash`, `zsh`, etc.

If `conda` is not already available, install [conda](https://docs.conda.io/projects/conda/en/stable/user-guide/install/index.html). If you're installing `conda` for the first time, we recommend `Miniconda` over `Anaconda`. 

```sh
# Once `conda` is installed
$ conda env create -f config/hknweb-dev.yml         # Create dev environment
$ conda activate hknweb-dev                         # Activate dev environment
$ python manage.py migrate                          # Initialize database
$ python manage.py init_permissions                 # Provision database with default permissions
```

## Development
All commands we use are native to Django [link to available Django commands](https://docs.djangoproject.com/en/4.1/django-admin/#available-commands). If you haven't worked with Django before, checkout the [Django tutorial](https://docs.djangoproject.com/en/4.1/intro/).

A few frequently used commands:
```sh
$ python manage.py makemigrations       # Create migrations files
$ python manage.py migrate              # Apply migrations files to database
$ python manage.py createsuperuser      # Create an admin super user to login as 
$ python manage.py runserver            # Run development server
$ coverage run                          # Run tests
$ coverage report                       # Report test coverage
```
