#!/usr/bin/python
from subprocess import call
from alternativa.ambiente import ambiente

call([
  'mysql',
  ambiente.locaweb.db.name,
  '-h',ambiente.locaweb.db.host,
  '-u',ambiente.locaweb.db.user,
  '-p%s'%ambiente.locaweb.db.password
  ])
