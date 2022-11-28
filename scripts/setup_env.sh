#!/usr/bin/env bash

conda update -q -n base -c defaults conda
conda env create -q -f config/"$1".yml
conda info -a  # Print post-creation properties

conda init bash
source ~/.bashrc

conda activate "$1"

python manage.py migrate
python manage.py collectstatic --noinput
