if [ $# -eq 0 ]
then
  MAIN_APP='alternativa'
  echo "Se asigna por default la aplicación principal $MAIN_APP"
else
  MAIN_APP="$1"
fi

cd "$MAIN_APP/static"

if [ $? -ne 0 ]
then
  echo "ERROR: No se ha podido acceder a $MAIN_APP/static"
  exit 1
fi

if [ -d bootstrap ]
then
  echo "ERROR: Ya existe el directorio bootstrap"
  exit 1
fi

wget http://twitter.github.com/bootstrap/assets/bootstrap.zip

if [ $? -ne 0 ]
then
  echo "ERROR: No se ha podido descargar http://twitter.github.com/bootstrap/assets/bootstrap.zip"
  exit 1
fi

unzip bootstrap.zip

if [ $? -ne 0 ]
then
  echo "ERROR: No se ha podido descomprimir bootstrap.zip"
  exit 1
fi

rm bootstrap.zip

if [ $? -ne 0 ]
then
  echo "ERROR: No se ha podido borrar bootstrap.zip"
  exit 1
fi

exit 0
