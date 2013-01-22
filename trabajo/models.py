# coding=utf-8

from django.db import models
from agencia.models import Agenciado
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill, Adjust
from datetime import date

class ItemPortfolio(models.Model):
    titulo = models.CharField(max_length=100, unique=True)
    video = models.URLField()
    # agregar rutas a configuracion del apache, al archivo settings y crear carpetas correspondientes
    imagen = models.ImageField(upload_to='trabajo/portfolio/')
    thumbnail = ImageSpecField([Adjust(contrast=1.2, sharpness=1.1), ResizeToFill(100,100)], image_field='imagen', format='JPEG', options={'quality': 90})
    fecha = models.DateField(default=date.today(),verbose_name=u'Data')
    def __unicode__(self):
      return self.titulo
    class Meta:
      ordering = ['-fecha']
      verbose_name = u"Item Portfolio"
      verbose_name_plural = u"Portfolio"

class Trabajo(models.Model):
    titulo = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(verbose_name=u'Descripçao')
    imagen = models.ImageField(upload_to='trabajo/trabajo/',blank=True)
    thumbnail = ImageSpecField([Adjust(contrast=1.2, sharpness=1.1), ResizeToFill(100,100)], image_field='imagen', format='JPEG', options={'quality': 90})
    ESTADO_TRABAJO=(
      ('RE',u'Registrado'),
      ('AT',u'Ativo'),
      ('PC',u'Pendente de cobrar'),
      ('FI',u'Finalizado'),
    )
# @todo agregar validación entre secuencia de las distintas fechas
    fecha_ingreso = models.DateField(default=date.today(),verbose_name=u'Data ingreso')
    fecha_trabajo_desde = models.DateField(default=date.today(),verbose_name=u'Data trabalho desde')
    fecha_trabajo_hasta = models.DateField(default=date.today(),verbose_name=u'Data trabalho ate')
    fecha_finalizacion = models.DateField(default=date.today(),verbose_name=u'Data finalização')
    estado = models.CharField(max_length=2,choices=ESTADO_TRABAJO)
    def __unicode__(self):
      return '%s (%s)' % (self.titulo, self.fecha_ingreso)
    class Meta:
      ordering = ['-fecha_ingreso']

class Rol(models.Model):
    trabajo = models.ForeignKey(Trabajo,on_delete=models.PROTECT)
    descripcion = models.CharField(max_length=60, unique=True, verbose_name=u'Descripçao')
    caracteristicas = models.TextField(verbose_name=u'Caraterísticas')
    cantidad = models.IntegerField(verbose_name=u'Quantidade de procurados',blank=True,null=True)
    def __unicode__(self):
      return '%s | %s' % (self.trabajo,  self.descripcion)
    class Meta:
      ordering = ['trabajo__titulo','descripcion']
      verbose_name = u"Rol"
      verbose_name_plural = u"Roles"

class Postulacion(models.Model):
    agenciado = models.ForeignKey(Agenciado,on_delete=models.PROTECT)
    rol = models.ForeignKey(Rol,on_delete=models.PROTECT)
    ESTADO_POSTULACION=(
      ('PC', u'Postulado para casting'),
      ('ST', u'Selecionado para trabalho'),
      ('TR', u'Trabalho realisado'),
      ('TP', u'Trabalho pagado'),
    )
    DICT_ESTADO_POSTULACION=dict(ESTADO_POSTULACION)
    estado = models.CharField(max_length=2,choices=ESTADO_POSTULACION)
    def __unicode__(self):
      return '%s | %s | %s' % (self.agenciado,Postulacion.DICT_ESTADO_POSTULACION[self.estado],self.rol)
