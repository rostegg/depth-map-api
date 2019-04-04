#!/bin/bash
IS_VIRTUALENV_INSTALLED=$(dpkg-query -W -f='${Status}' virtualenv 2>/dev/null | grep -c "ok installed")

if [ "$IS_VIRTUALENV_INSTALLED" -eq "0" ]; then
    sudo apt install virtualenv
fi

virtualenv -p python3 flask-env 
source flask-env/bin/activate
pip install -r requirements.txt
python3 run.py