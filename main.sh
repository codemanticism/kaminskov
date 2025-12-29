#!/bin/sh
# Absolute path to this script, e.g. /home/user/bin/foo.sh
SCRIPT=$(readlink -f "$0")
# Absolute path this script is in, thus /home/user/bin
SCRIPT_PATH=$(dirname "$SCRIPT")

PYTHONHOME=/home/gabib/miniconda3
export PYTHONHOME
NUITKA_PYTHONPATH="/home/gabib/projects/kaminskov:/home/gabib/miniconda3/lib/python3.13:/home/gabib/miniconda3/lib/python3.13/lib-dynload:/home/gabib/miniconda3/lib/python3.13/site-packages:/home/gabib/miniconda3/lib/python3.13/site-packages/setuptools/_vendor"
export NUITKA_PYTHONPATH
PYTHONPATH="/home/gabib/projects/kaminskov:/home/gabib/miniconda3/lib/python3.13:/home/gabib/miniconda3/lib/python3.13/lib-dynload:/home/gabib/miniconda3/lib/python3.13/site-packages:/home/gabib/miniconda3/lib/python3.13/site-packages/setuptools/_vendor"
export PYTHONPATH

"$SCRIPT_PATH/main.bin" $@

