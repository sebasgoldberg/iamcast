cd alternativa/static

if [ $? -ne 0 ]
then
  echo "ERROR: No se ha podido acceder a alternativa/static"
  exit 1
fi

if [ -d bootstrap ]
then
  echo "ERROR: Ya existe el directorio bootstrap"
  exit 1
fi

wget https://github.com/twitter/bootstrap/zipball/master

if [ $? -ne 0 ]
then
  echo "ERROR: No se ha podido descargar https://github.com/twitter/bootstrap/zipball/master"
  exit 1
fi

unzip master

if [ $? -ne 0 ]
then
  echo "ERROR: No se ha podido descomprimir master"
  exit 1
fi

rm master

if [ $? -ne 0 ]
then
  echo "ERROR: No se ha podido borrar master"
  exit 1
fi

mv twitter-bootstrap-8c7f9c6 bootstrap

if [ $? -ne 0 ]
then
  echo "ERROR: No se ha podido realizar 'mv twitter-bootstrap-8c7f9c6 bootstrap'"
  exit 1
fi

exit 0
