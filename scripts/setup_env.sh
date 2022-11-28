#!/usr/bin/env bash

conda update -q -n base -c defaults conda
conda env create -q -f config/"$1".yml
conda info -a  # Print post-creation properties

source ~/miniconda/etc/profile.d/conda.sh
conda activate "$1"

python manage.py migrate
python manage.py collectstatic --noinput
