hknweb
======

Welcome! This is the repository for the in-progress redesign for the HKN
website, built with Django.

## Setup

hknweb uses Django 2.0, which requires Python 3.4+. However, the latest
version (Python 3.6) is recommended.

Development requires [`pipenv`](https://docs.pipenv.org):

```sh
$ pip install pipenv
```

as well as a working copy of MySQL (or MariaDB).

To install the Python dev environment (Python dependencies, a virtualenv), run
```sh
$ make venv
```

To run the Django development server (which runs a web server locally), run
```sh
$ make serve
```

which will make the web site available at `http://localhost:3000`.
