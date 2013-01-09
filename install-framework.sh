apt-get install apache2
apt-get install mysql-server
# @todo Verificar si es necesario instalar cython
#apt-get install cython
apt-get install libapache2-mod-wsgi
apt-get install python-mysqldb
apt-get install python-imaging

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

apt-get install python-pip
pip install Django

# Se crean las carpetas que no están incluidas en el repo
mkdir -p uploads/agenciados/fotos
chmod 777 -R uploads

echo 'A continuación debería realizar las siguientes tareas:'
echo '1) Crear la base de datos y usuario según ha definido en alternativa/settings.py.'
echo '2) Ejecutar el script reiniciar.sh'
echo '3) Crear la configuracion para el servidor virtual en /etc/apache2/sites-available y crear el correspondiente link a dicha configuración en /etc/apache2/sites-enabled'

