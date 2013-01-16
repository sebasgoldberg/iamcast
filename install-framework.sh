apt-get install apache2
apt-get install mysql-server
apt-get install cython
apt-get install libapache2-mod-wsgi
apt-get install python-mysqldb
apt-get install python-imaging

#Instalacion del modulo python para SQL Server

#Se verifica si hay alguna version instalada
instalar_pymssql='X'
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

apt-get install python-pip
pip install Django

# Instalacion de paquete para manejo de thumbnails
pip install django-imagekit

# Se crean las carpetas que no están incluidas en el repo
mkdir -p uploads/agenciados/fotos
mkdir -p uploads/cache/agenciados/fotos
chmod 777 -R uploads

INSTALL_SCRIPT_DIR=$(pwd)

# Instalacion de no-ip
which noip2 > /dev/null
if [ $? -ne 0 ]
then
  cd /usr/local/src/
  wget http://www.no-ip.com/client/linux/noip-duc-linux.tar.gz
  tar xf noip-duc-linux.tar.gz
  cd noip-2.1.9-1/
  make install

# Se configura como servicio y en el startup
  if [ -f noip2 ]
  then
    cp noip2 /etc/init.d/
    update-rc.d noip2 defaults 90
  else
    echo 'ERROR: No se ha encontrado script para servicio noip2'
  fi

fi
noip2

# Instalacion de PyYaml
cd "$INSTALL_SCRIPT_DIR"
apt-get install mercurial #necesario para hacer el pull del proyecto
mkdir pyyaml
cd pyyaml
hg clone https://bitbucket.org/xi/pyyaml
cd pyyaml
python setup.py install
cd ../..
rm -rf pyyaml

echo ''
echo 'A continuación debería realizar las siguientes tareas:'
echo '+ Crear la base de datos y usuario según ha definido en alternativa/settings.py.'
echo '+ Crear la configuracion para el servidor virtual en /etc/apache2/sites-available (copiar el ya existente y modificar dominio) y crear el correspondiente link a dicha configuración en /etc/apache2/sites-enabled'
echo '+ Generar archivos de certificado y clave referenciados por el archivo de configuración del servidor virtual'
echo "+ Buscar y modificar los @todo que correspondan."
echo "+ Asignar el dominio correspondiente al modelo Site"
echo '+ Ejecutar el script reiniciar.sh'
echo ''
