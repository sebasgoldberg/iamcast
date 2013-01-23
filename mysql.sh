#!/bin/bash
python -c "import alternativa.settings"
if [ $? -ne 0 ]
then
  echo "ERROR: Este script debe ejecutarse desde la ruta del proyecto."
  exit 1
fi

pass="$(python -c 'from alternativa.ambiente import ambiente; print ambiente.db.password')"

mysql agencia -u agencia -p"$pass"
