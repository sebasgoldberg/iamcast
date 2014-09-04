# coding=utf-8
from iampacks.cross.ambiente.models import BaseAmbiente
import os

id_agencia='iamcast'

class Ambiente(BaseAmbiente):
  productivo=False
  app_in_dev=None

  id_agencia=id_agencia
  site_id=id_agencia

  dominio='%s.com.ar'%id_agencia
  puerto_http='80'
  puerto_https='443'

  admins = (
    ('admin', 'admin@xxxx.com'),
  )

  class sitio:
    class externo:
      url = None

  class db:
    name=id_agencia
    user=id_agencia
    password='password'
    class root:
      password=None

  class ciudades:
    class db:
      name='ciudades'

  project_directory = '%s/' % os.path.abspath('%s/..' % os.path.split(os.path.abspath(__file__))[0])
  wsgi_dir = os.path.dirname(__file__)

  class email:
    host = 'smtp.gmail.com'
    user = 'user@gmail.com'
    password = 'password'
    port = 587

  class zonomi:
    api_key = None

  class backup:
    user = None
    host = None
    destination = None
 
  class presentation:
    static = None

    templates = None


ambiente=Ambiente()
