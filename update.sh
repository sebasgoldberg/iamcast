#!/bin/bash
sudo pip install django-simple-captcha==0.4.1

WD="$(pwd)"

cd ../iampacks/agencia
git pull origin master

cd ../cross
git pull origin master

cd "$WD"
./manage.py migrate
./manage.py syncdb --all
./manage.py collectstatic

