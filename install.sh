#!/bin/bash
./manage.py dbcreate # Solucionar problema en syncdb --all
./manage.py syncdb --noinput
./manage.py migrate
./manage.py syncdb --all # Necesario para cargar permisos
./manage.py loadciudades
mkdir -p uploads/agenciados/fotos
mkdir -p uploads/cache/agenciados/fotos
mkdir -p uploads/agencias/logos
mkdir -p uploads/tmp
./manage.py setpermissions
./manage.py collectstatic --noinput
./manage.py loadperfil # Lleva como parámetro el idioma aplicar traducciones correspondientes
./manage.py loadgroups
./manage.py a2create
./manage.py domainupdate
