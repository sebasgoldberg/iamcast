#!/bin/bash
WD="$(pwd)"

cd ../iampacks/agencia
git pull origin master

cd ../cross
git pull origin master

cd "$WD"
./manage.py migrate
./manage.py syncdb --all --noinput
./manage.py collectstatic --noinput
