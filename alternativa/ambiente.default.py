# coding=utf-8
from base_ambiente import BaseAmbiente
import os

id_agencia='iamcast'

class Ambiente(BaseAmbiente):
  productivo=False
  app_in_dev=None

  id_agencia=id_agencia

  dominio='%s.com.ar'%id_agencia
  puerto_http='8080'
  puerto_https='8081'

  class db:
    name=id_agencia
    user=id_agencia
    password='password'

  class ciudades:
    class db:
      name='ciudades'

  project_directory = '%s/' % os.path.abspath('%s/..' % os.path.split(os.path.abspath(__file__))[0])

  class email:
    host = 'smtp.gmail.com'
    user = 'user@gmail.com'
    password = 'password'
    port = 587

  class zonomi:
    api_key = None

ambiente=Ambiente()
