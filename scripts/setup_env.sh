#!/usr/bin/env bash

conda update -q -n base -c defaults conda
conda env create -q -f config/"$1".yml
conda info -a  # Print post-creation properties

eval "$(conda shell.bash hook)"

conda activate "$1"

python manage.py migrate


case $1 in
    "hknweb-prod")
        python manage.py collectstatic --noinput
    ;;

    "hknweb-dev")
    ;;

    *)
        echo "Unrecognized hknweb mode $1"
        exit 1
    ;;
esac
