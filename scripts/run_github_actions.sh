#!/usr/bin/env bash

eval "$(conda shell.bash hook)"
conda activate hknweb-dev

DJANGO_DIR=~/hknweb/github_actions/current
PYTHONPATH=$DJANGO_DIR:$PYTHONPATH

SOCKFILE=/srv/apps/$(whoami)/dev.sock
NUM_WORKERS=1

cd $DJANGO_DIR

exec gunicorn "$DJANGO_WSGI_MODULE" \
    -w $NUM_WORKERS \
    --log-level debug \
    --log-file - \
    -b unix:"$SOCKFILE"
