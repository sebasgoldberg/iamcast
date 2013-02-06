#!/bin/bash

# Busca una expresión regular en ciertos archivos y donde encuentra abre el archivo utilizando el vim en la línea donde encontró la expresión regular

if [ $# -ne 2 ]
then
  echo "$0 <regexp_to_find> <regexp_file_name>"
  exit 1
fi

APERTURA_DE_ARCHIVOS=$(grep -n "$1" $(find . -name "$2") | cut -f '1-2'  -d : )

for linea in $APERTURA_DE_ARCHIVOS 
do
  arch=$(echo "$linea" | cut -f 1 -d ':')
  linea=$(echo "$linea" | cut -f 2 -d ':')
  vim "$arch" +"$linea"
done

exit 0
