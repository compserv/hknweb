#!/usr/bin/env bash

conda env create -f config/"$1".yml

source ~/miniconda/etc/profile.d/conda.sh
conda activate "$1"

conda info -a  # Print post-creation properties

python manage.py migrate
python manage.py collectstatic --noinput
