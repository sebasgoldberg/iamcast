#!/bin/bash
WD="$(pwd)"

cd ../iampacks/agencia
git pull origin master

cd ../cross
git pull origin master

cd "$WD"
./manage.py migrate
./manage.py syncdb --all
echo "Tareas pendientes:"
echo "- Agregar permiso de envío de mail a agenciados, a grupo de agenciadores."

