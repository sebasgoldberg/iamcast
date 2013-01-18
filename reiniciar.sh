#!/bin/bash

cantidad=5

[ $# -gt 0 ] && cantidad="$1"

echo "drop database agencia; create database agencia;" | mysql agencia -u agencia -p"$(python -c 'from alternativa.ambiente import ambiente; print ambiente.db.password')"
if [ $? -ne 0 ]
then
  exit 1
fi

cd /home/cerebro/django-projects/alternativa
if [ $? -ne 0 ]
then
  exit 1
fi

echo -e 'no\n' | python manage.py syncdb 
if [ $? -ne 0 ]
then
  exit 1
fi

python manage.py migrar "--cantidad=${cantidad}"
if [ $? -ne 0 ]
then
  exit 1
fi

python manage.py migrar-fotos
if [ $? -ne 0 ]
then
  exit 1
fi

exit 0
