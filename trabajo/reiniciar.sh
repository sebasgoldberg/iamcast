#!/bin/bash

echo "drop table trabajo_itemportfolio; drop table trabajo_postulacion; drop table trabajo_rol; drop table trabajo_trabajo;" | mysql agencia -u agencia -p"$(python -c 'from alternativa.ambiente import ambiente; print ambiente.db.password')"
if [ $? -ne 0 ]
then
  exit 1
fi

cd /home/cerebro/django-projects/alternativa
if [ $? -ne 0 ]
then
  exit 1
fi

python manage.py syncdb 
if [ $? -ne 0 ]
then
  exit 1
fi

exit 0
