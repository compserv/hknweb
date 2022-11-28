#!/usr/bin/env bash

wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O miniconda.sh
bash miniconda.sh -b -p "$HOME"/miniconda

conda info -a  # Print post-installation properties

conda update -n base -c defaults conda

conda init bash
