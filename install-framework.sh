apt-get install apache2
apt-get install mysql-server
# @todo Verificar si es necesario instalar cython
#apt-get install cython
apt-get install libapache2-mod-wsgi
apt-get install python-mysqldb
apt-get install python-imaging
# El paquete a continuación es necesario para interactuar con base de datos Microsoft SQL Server
apt-get install python-pymssql 
apt-get install python-pip
pip install Django
echo 'Por favor, debe crear la base de datos y usuario según ha definido en alternativa/settings.py.'
echo 'Luego debe ejecutar el script reiniciar.sh'
