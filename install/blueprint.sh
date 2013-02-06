if [ -d alternativa/static/css/blueprint ]
then
  echo "Ya existe la carpeta blueprint alternativa/static/css/, es muy factible que ya esté instalado"
  exit 0
fi

mkdir -p alternativa/static/css/blueprint.tmp

if [ $? -ne 0 ]
then
  exit 1
fi

cd alternativa/static/css/blueprint.tmp

if [ $? -ne 0 ]
then
  exit 1
fi

git init

if [ $? -ne 0 ]
then
  exit 1
fi

git pull git://github.com/joshuaclayton/blueprint-css.git

if [ $? -ne 0 ]
then
  exit 1
fi

mv blueprint ../

if [ $? -ne 0 ]
then
  exit 1
fi

cd ..

rm -rf blueprint.tmp

if [ $? -ne 0 ]
then
  exit 1
fi

