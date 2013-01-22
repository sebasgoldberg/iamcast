#!/bin/bash
python -c "import alternativa.settings"
if [ $? -ne 0 ]
then
  echo "ERROR: Este script debe ejecutarse desde la ruta del proyecto."
  exit 1
fi

echo "drop table trabajo_itemportfolio; drop table trabajo_postulacion; drop table trabajo_rol; drop table trabajo_trabajo;" | mysql agencia -u agencia -p"$(python -c 'from alternativa.ambiente import ambiente; print ambiente.db.password')"
if [ $? -ne 0 ]
then
  exit 1
fi

mkdir -p uploads/trabajo/portfolio
mkdir -p uploads/cache/trabajo/portfolio
mkdir -p uploads/trabajo/trabajo
mkdir -p uploads/cache/trabajo/trabajo
chmod 777 -R uploads

python manage.py syncdb 
if [ $? -ne 0 ]
then
  exit 1
fi

PRODUCTIVO=$(python -c "from alternativa.ambiente import ambiente; print ambiente.productivo")

if [ $? -ne 0 ]
then
  exit 1
fi

if [ "$PRODUCTIVO" = "False" ]
then
  python manage.py loaddata trabajo/fixtures/test-data
fi

exit 0
