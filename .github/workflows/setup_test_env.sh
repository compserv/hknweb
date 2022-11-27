#!/bin/bash

wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O miniconda.sh
bash miniconda.sh -b -p "$HOME"/miniconda

conda init bash
source ~/.bashrc

conda update -n base -c defaults conda
conda info -a
conda env create -f config/hknweb-dev.yml

conda activate hknweb-dev

python manage.py migrate
echo $SHELL
