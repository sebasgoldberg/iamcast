#!/bin/bash

### Variables globales
WD="$(readlink -f "$(dirname "$0")")"

INSTALL_FRAMEWORK=' '
INSTALL_IAMPACKS=' '
INSTALL_NOIP=' '

if [ $# -eq 0 ]
then
  INSTALL_FRAMEWORK='X'
  INSTALL_IAMPACKS='X'
  INSTALL_NOIP='X'
elif [ $1 = '-f' ]
then
  INSTALL_FRAMEWORK='X'
elif [ $1 = '-i' ]
then
  INSTALL_IAMPACKS='X'
elif [ $1 = '-n' ]
then
  INSTALL_NOIP='X'
elif [ $1 = '-h' ]
then
  echo "$0 [option]"
  echo "no option installs all."
  echo "-f Installs only framework."
  echo "-i Installs only iampacks"
  echo "-n Installs only no-ip"
fi

function install_django_crispy_forms
{
  pip install --upgrade django-crispy-forms

  if [ $? -ne 0 ]
  then
    echo "ERROR: Error al ejecutar 'pip install --upgrade django-crispy-forms'"
    exit 1
  fi
}

function install_standard_framework
{
  if [ "$INSTALL_FRAMEWORK" = ' ' ]
  then
    return 0
  fi

  apt-get update

  apt-get -y install make
  apt-get -y install bc
  apt-get -y install apache2
  apt-get -y install mysql-server
  apt-get -y install cython
  apt-get -y install libapache2-mod-wsgi
  apt-get -y install python-mysqldb
  apt-get -y install python-imaging
  apt-get -y install mercurial #necesario para hacer el pull de algunos pagetes a ser instalados
  apt-get -y install unzip
  apt-get -y install gettext
  apt-get -y install python-pip
  apt-get -y install curl
  apt-get -y install build-essential

  pip install Django==1.4.3

# Instalacion de paquete para manejo de thumbnails
  pip install django-imagekit==2.0.4
  pip install requests

# Instalacion de PyYaml
  mkdir pyyaml
  cd pyyaml
  hg clone https://bitbucket.org/xi/pyyaml
  cd pyyaml
  python setup.py install
  cd ../..
  rm -rf pyyaml

# Generación de los directorios donde estarán los certificados
  if [ ! -d /etc/apache2/ssl ]
  then
    mkdir /etc/apache2/ssl 
  fi

  a2enmod ssl
  a2enmod rewrite
  service apache restart

  apt-get -y install python-coverage

  install_django_crispy_forms

  easy_install South
  pip install django-cities-light

  pip install django-grappelli==2.4.8
}

function install_iampacks
{
  if [ "$INSTALL_IAMPACKS" = ' ' ]
  then
    return 0
  fi

  echo "Se realiza la instalación de los paquetes de iamsoft."

  DIST_PACKAGE_DIR="$(readlink -f "$(dirname "$(python -c 'import django;print django.__file__')")/..")"
  #DIST_PACKAGE_DIR="/usr/local/lib/python2.7/dist-packages"

  if [ $? -ne 0 ]
  then
    echo "ERROR: No se pudo obtener el directorio dist-packages de python."
    exit 1
  fi

  cd "$DIST_PACKAGE_DIR"

  if [ -d "iampacks" ]
  then
    echo "ERROR: Parecería ser que ya ha sido instalado iampacks."
    return 1
  fi

  mkdir iampacks
  cd iampacks
  touch __init__.py

  git clone https://github.com/sebasgoldberg/cross.git
  git clone https://github.com/sebasgoldberg/agencia.git

  ./cross/compile_messages.sh
  ./agencia/compile_messages.sh

}

function get_ambient_parameter
{
  echo "$(python -c "from iamsoft.ambiente import ambiente; print ambiente.$1" )"
}

function crear_usuario_y_base_datos
{
  cd "$(readlink -f "$(dirname "$0")")"

  DB_NAME="$(get_ambient_parameter "db.name")"
  DB_USER="$(get_ambient_parameter "db.user")"
  DB_PASS="$(get_ambient_parameter "db.password")"

  echo "Se procede a crear base de datos y usuario de base de datos, por favor introduzca la contraseña del usuario root:"

  (echo "create database $DB_NAME character set utf8;"
  echo "create user '$DB_USER'@'localhost' identified by '$DB_PASS';"
  echo "grant all on $DB_NAME.* to $DB_USER;"
  ) | mysql -u root -p

  if [ $? -ne 0 ]
  then
    echo "ERROR: Ha ocurrido un error al intentar crear usuario y base de datos de iamsoft."
    return 1
  fi

}

function create_ambient_dir
{
  DIR="$(get_ambient_parameter "$1")"

  if [ $? -ne 0 ]
  then
    echo 'ERROR: No se ha podido obtener el path de agencias del ambiente.'
    return 1
  fi

  if [ ! -d "$DIR" ]
  then
    mkdir "$DIR"
    if [ $? -ne 0 ]
    then
      echo "Error al crear '$DIR'"
      exit 1
    fi
  fi

  chgrp -R www-data "$DIR"

  if [ $? -ne 0 ]
  then
    echo "Error al cambiar grupo a www-data '$DIR'"
    exit 1
  fi
}

function install_no_ip
{
  #http://www.noip.com/support/knowledgebase/installing-the-linux-dynamic-update-client-on-ubuntu/
  #How to install No-IP Linux Dynamic Update Client (DUC) on your Ubuntu 12.04 LTS.

  if [ "$INSTALL_NOIP" = ' ' ]
  then
    return 0
  fi

  echo "Se procede con la instalación no-ip."

  cd /usr/local/src/

  if [ $? -ne 0 ]
  then
    echo "Error al intentar acceder a /usr/local/src/."
    exit 1
  fi
  
  if [ -d 'noip-2.1.9-1' ]
  then
    echo "Error: Parecería ser que no-ip ya se encuentra instalado."
    exit 1
  fi

  wget http://www.no-ip.com/client/linux/noip-duc-linux.tar.gz
  
  if [ $? -ne 0 ]
  then
    echo "Error al intentar descargar la aplicación."
    exit 1
  fi
  
  tar xf noip-duc-linux.tar.gz
  
  if [ $? -ne 0 ]
  then
    echo "Error al intentar descomprimir la aplicación."
    exit 1
  fi
  
  cd noip-2.1.9-1/
  
  if [ $? -ne 0 ]
  then
    echo "Error al intentar acceder a noip-2.1.9-1."
    exit 1
  fi
  
  make install

  if [ $? -ne 0 ]
  then
    echo "Error al intentar instalar la aplicación."
    exit 1
  fi

  noip2
  
  if [ $? -ne 0 ]
  then
    echo "Error al intentar ejecutar el servicio."
    exit 1
  fi

  # To Configure the Client:
  # As root again (or with sudo) issue the below command:
  # /usr/local/bin/noip2 -C (dash capital C, this will create the default config file)
  # You will then be prompted for your username and password for No-IP, as well as which host names you wish to update. Be careful, one of the questions is “Do you wish to update all hosts”. If answered incorrectly this could effect host names in your account that are pointing at other locations.
  # Now the client is installed and configured, you just need to launch it. Simply issue this final command to launch the client in the background:
  # /usr/local/bin/noip2
}

install_standard_framework

install_iampacks

install_no_ip

exit 0


