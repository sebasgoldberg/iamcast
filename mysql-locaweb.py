#!/usr/bin/python
from subprocess import call
from alternativa.ambiente import ambiente

#mysql agenciaalterna -h mysql01.agenciaalternativa.com -u agenciaalterna -p
call([
  'mysql',
  ambiente.locaweb.db.name,
  '-h',ambiente.locaweb.db.host,
  '-u',ambiente.locaweb.db.user,
  '-p%s'%ambiente.locaweb.db.password
  ])
#select data, link from portifolio where tipo = 'V'
