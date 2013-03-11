#Instalacion del modulo python para SQL Server
[ $# -gt 0 ] && forzar_instalacion_pymssql=$1

#Se verifica si hay alguna version instalada
instalar_pymssql='X'

if [ "$forzar_instalacion_pymssql" = "" ]
then
  python -c "import pymssql" > /dev/null 2>&1
  if [ $? -eq 0 ]
  then
    # En caso de haber alguna version instalada se verifica si sirve
    pymssql_version=$(python -c "import pymssql; print pymssql.__version__" | cut -f 1 -d '.')
    if [ $pymssql_version -ge 2 ]
    then
      instalar_pymssql=''
    fi
  fi
fi

if [ "$instalar_pymssql" = "X" ]
then
  # El paquete a continuación es necesario para interactuar con base de datos Microsoft SQL Server
  apt-get remove python-pymssql #Se quita en caso de existir una instalación (la version instalada por apt-get no funciona correctamente)
  apt-get install python-dev #Necesatio para poder instalar pymssql

  mkdir pymssql
  cd pymssql/
  hg clone https://code.google.com/p/pymssql/
  if [ $? -ne 0 ]
  then
    echo "No se ha encontrado el paquete para la instalación de pymssql. Por favor ingrese a la siguiente página http://code.google.com/p/pymssql/ y modifique url, nombre de archivo y nombre de carpeta en este script, el contexto es donde se está mostrando este mensaje."
    exit 0
  fi
  cd pymssql/
  sudo python setup.py build
  sudo python setup.py install
  cd ../..
  rm -rf pymssql
fi
