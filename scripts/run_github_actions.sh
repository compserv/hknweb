#!/usr/bin/env bash

eval "$(conda shell.bash hook)"
conda activate hknweb-dev

DJANGO_DIR=~/hknweb/github_actions/current
PYTHONPATH=$DJANGO_DIR:$PYTHONPATH

cd $DJANGO_DIR

exec gunicorn "$DJANGO_WSGI_MODULE" &
