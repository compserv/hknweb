#!/usr/bin/env bash

conda env create -f config/"$1".yml

conda activate "$1"

conda info -a  # Print post-creation properties

python manage.py migrate
python manage.py collectstatic --noinput
