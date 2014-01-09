#!/bin/bash

WD="$(dirname "$(readlink -f "$0")")"

cd "$WD/alternativa"

DB_USER="$(python -c "from ambiente import ambiente; print ambiente.db.user")"
if [ $? -ne 0 ]
then
  echo "No se ha podido obtener usuario de BD del ambiente"
  exit 1
fi

DB_NAME="$(python -c "from ambiente import ambiente; print ambiente.db.name")"
if [ $? -ne 0 ]
then
  echo "No se ha podido obtener nombre de BD del ambiente"
  exit 1
fi

DB_PASS="$(python -c "from ambiente import ambiente; print ambiente.db.password")"
if [ $? -ne 0 ]
then
  echo "No se ha podido obtener password de BD del ambiente"
  exit 1
fi

echo "Se procede a crear base de datos y usuario de base de datos (introduzca la contraseña del usuario root de mysql)."

(echo "create database $DB_NAME character set utf8;"
echo "create user '$DB_USER'@'localhost' identified by '$DB_PASS';"
echo "grant all on $DB_NAME.* to $DB_USER;"
) | mysql -u root -p

cd "$WD"

./manage.py install-agencia
