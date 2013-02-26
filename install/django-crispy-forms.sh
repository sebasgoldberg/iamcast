pip install --upgrade django-crispy-forms

if [ $? -ne 0 ]
then
  echo "ERROR: Error al ejecutar 'pip install --upgrade django-crispy-forms'"
  exit 1
fi

exit 0
