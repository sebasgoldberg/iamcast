#!/bin/bash
WD="$(pwd)"

cd ../iampacks/agencia
git pull origin master

cd ../cross
git pull origin master

cd "$WD"
./manage.py migrate
./manage.py syncdb --all
./manage.py collectstatic

mkdir -p uploads/tmp
./manage.py setpermissions


pip uninstall django
pip uninstall django-imagekit

pip install Django==1.6.2
pip install django-imagekit==3.2.0
