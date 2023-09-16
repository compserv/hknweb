#!/usr/bin/env bash

DJANGO_DIR=$1
PYTHONPATH=$DJANGO_DIR:$PYTHONPATH

cd $DJANGO_DIR

exec poetry run gunicorn hknweb.wsgi --daemon
