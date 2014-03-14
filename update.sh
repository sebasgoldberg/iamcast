#!/bin/bash
sudo pip install django-modeltranslation==0.7.3

WD="$(pwd)"

cd ../iampacks/agencia
git pull origin master

cd ../cross
git pull origin master

cd "$WD"
./manage.py migrate
./manage.py syncdb --all
./manage.py collectstatic
./manage.py update_translation_fields
./manage.py loadperfil
