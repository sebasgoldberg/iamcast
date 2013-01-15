#!/bin/bash

echo "drop database agencia; create database agencia;" | mysql agencia -u agencia -pagencia1234  
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

echo 'Ingrese clave del superusuario de la aplicación'
python manage.py createsuperuser --username=cerebro --email=cerebro@cerebro.com

python manage.py migrar
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
