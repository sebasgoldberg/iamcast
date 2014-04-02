#!/bin/bash
WD="$(pwd)"

git pull origin master

cd ../iampacks/agencia
git pull origin master

cd ../cross
git pull origin master

cd "$WD"
./manage.py migrate
./manage.py syncdb --all --noinput
./manage.py collectstatic --noinput
