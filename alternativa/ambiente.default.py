# coding=utf-8
from base_ambiente import BaseAmbiente
import os

class Ambiente(BaseAmbiente):
  productivo=False
  app_in_dev=None

  dominio='dev.iamcast.com.ar'
  puerto_http='8080'
  puerto_https='8081'

  class db:
    name='agencia'
    user='agencia'
    password='password'

  project_directory = '%s/' % os.path.abspath('%s/..' % os.path.split(os.path.abspath(__file__))[0])

  class email:
    host = 'smtp.gmail.com'
    user = 'user@gmail.com'
    password = 'password'
    port = 587

ambiente=Ambiente()
