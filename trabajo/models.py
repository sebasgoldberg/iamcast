# coding=utf-8
# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#     * Rearrange models' order
#     * Make sure each model has one field with primary_key=True
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.

from django.db import models
from agencia.models import Agenciado

class Rol(models.Model):
    descripcion = models.CharField(max_length=60, unique=True, verbose_name=u'Descripçao')
    def __unicode__(self):
      return self.descripcion
    class Meta:
      ordering = ['descripcion']
      verbose_name = "Rol"
      verbose_name_plural = "Roles"

class ItemPortfolio(models.Model):
    titulo = models.CharField(max_length=100, unique=True)
    url = models.URLField()
    fecha = models.DateTimeField(verbose_name='Data')
    def __unicode__(self):
      return self.titulo
    class Meta:
      ordering = ['-fecha']
      verbose_name = "Item Portfolio"
      verbose_name_plural = "Portfolio"

class Trabajo(models.Model):
    titulo = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(verbose_name=u'Descripçao')
    def __unicode__(self):
      return self.descripcion
    class Meta:
      ordering = ['descripcion']

class Postulacion(models.Model):
    agenciado = models.ForeignKey(Agenciado,on_delete=models.PROTECT)
    trabajo = models.ForeignKey(Trabajo,on_delete=models.PROTECT)
    ESTADO_POSTULACION=(
      ('PO', 'POSTULADO'),
    )
    estado = models.CharField(max_length=2,choices=ESTADO_POSTULACION)
    def __unicode__(self):
      return self.estado+'-'+self.trabajo+'-'+self.agenciado
