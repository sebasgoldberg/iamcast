apt-get install apache2
apt-get install mysql-server
# @todo Verificar si es necesario instalar cython
#apt-get install cython
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
  wget http://pymssql.googlecode.com/files/pymssql-2.0.0b1-dev-20111019.tar.gz
  if [ $? -ne 0 ]
  then
    echo "No se ha encontrado el paquete para la instalación de pymssql. Por favor ingrese a la siguiente página http://code.google.com/p/pymssql/ y modifique url, nombre de archivo y nombre de carpeta en este script, el contexto es donde se está mostrando este mensaje."
    exit 0
  fi
  tar -zxvf pymssql-2.0.0b1-dev-20111019.tar.gz
  cd pymssql-2.0.0b1-dev-20111019/
  apt-get install cython
  python setup.py build
  python setup.py install
  cd ..
  cd ..
  rm -rf pymssql
fi

apt-get install python-pip
pip install Django

# Se crean las carpetas que no están incluidas en el repo
mkdir -p uploads/agenciados/fotos
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


echo 'A continuación debería realizar las siguientes tareas:'
echo '1) Crear la base de datos y usuario según ha definido en alternativa/settings.py.'
echo '2) Ejecutar el script reiniciar.sh'
echo '3) Crear la configuracion para el servidor virtual en /etc/apache2/sites-available (copiar el ya existente y modificar dominio) y crear el correspondiente link a dicha configuración en /etc/apache2/sites-enabled'
echo '4) Generar archivos de certificado y clave referenciados por el archivo de configuración del servidor virtual'

