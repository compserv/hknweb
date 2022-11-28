#!/bin/bash

conda info -a
conda env create -f config/"$1".yml

conda activate "$1"

python manage.py migrate
python manage.py collectstatic --noinput
