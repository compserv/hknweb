#!/usr/bin/env bash

DJANGO_WSGI_MODULE=hknweb.wsgi
DJANGO_DIR=~/hknweb/prod/current
SOCKFILE=/srv/apps/$(whoami)/dev.sock
NUM_WORKERS=4
PYTHONPATH=$DJANGO_DIR:$PYTHONPATH

source ~/miniconda/etc/profile.d/conda.sh
conda activate hknweb-dev

cd $DJANGO_DIR

exec gunicorn $DJANGO_WSGI_MODULE \
    -w $NUM_WORKERS \
    --log-level debug \
    --log-file - \
    -b unix:"$SOCKFILE"
