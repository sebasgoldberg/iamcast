echo "A continuación se importarán paises, estados y ciudades."
echo "Esta tarea puede demorar bastante tiempo."
echo "Los estados y ciudades a importar serán filtrados en caso de existir alguna señal."
echo "En caso de no existir ninguna señal serán importados todos los datos."
./manage.py syncdb
./manage.py migrate
./manage.py cities_light
#./manage.py cities_light --force-import BR
#./manage.py cities_light --force-import AR
