# coding=utf-8

from django.db import models
from agencia.models import Agenciado
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill, Adjust
from datetime import date

class ItemPortfolio(models.Model):
    titulo = models.CharField(max_length=100, unique_for_date='fecha')
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
    titulo = models.CharField(max_length=100, unique_for_date='fecha_ingreso')
    descripcion = models.TextField(verbose_name=u'Descripçao')
    imagen = models.ImageField(upload_to='trabajo/trabajo/',blank=True)
    thumbnail = ImageSpecField([Adjust(contrast=1.2, sharpness=1.1), ResizeToFill(100,100)], image_field='imagen', format='JPEG', options={'quality': 90})
    ESTADO_TRABAJO=(
      ('IN',u'Inicial'),
      ('AT',u'Ativo'),
      ('PC',u'Pendente de cobrar'),
      ('FI',u'Finalizado'),
    )
# @todo agregar validación entre secuencia de las distintas fechas
    fecha_ingreso = models.DateField(default=date.today(),verbose_name=u'Data ingreso')
    fecha_trabajo_desde = models.DateField(default=date.today(),verbose_name=u'Data trabalho desde')
    fecha_trabajo_hasta = models.DateField(default=date.today(),verbose_name=u'Data trabalho ate')
    fecha_finalizacion = models.DateField(default=date.today(),verbose_name=u'Data finalização')
    estado = models.CharField(max_length=2,choices=ESTADO_TRABAJO,null=False)
    def __unicode__(self):
      return '%s (%s)' % (self.titulo, self.fecha_ingreso)
    class Meta:
      verbose_name = u'Trabalho'
      verbose_name_plural = u"Trabalhos" 
      ordering = ['-fecha_ingreso']

    def thumbnail_img(self):
      url = ''
      if self.thumbnail:
        url = self.thumbnail.url
      return "<img src='%s' height=100 />" % url
    thumbnail_img.allow_tags = True

    def thumbnail_img_link(self):
      url = ''
      if self.thumbnail:
        url = self.thumbnail.url
      return "<a href='%s'><img src='%s' height=100 /></a>" % (self.imagen.url, url)
    thumbnail_img_link.allow_tags = True

class Rol(models.Model):
    trabajo = models.ForeignKey(Trabajo,on_delete=models.PROTECT)
    descripcion = models.CharField(max_length=60, verbose_name=u'Descripçao')
    caracteristicas = models.TextField(verbose_name=u'Caraterísticas')
    cantidad = models.IntegerField(verbose_name=u'Quantidade de procurados',blank=True,null=True)
    def __unicode__(self):
      return '%s | %s' % (self.trabajo,  self.descripcion)
    class Meta:
      ordering = ['-trabajo__fecha_ingreso','descripcion']
      verbose_name = u"Rol"
      verbose_name_plural = u"Roles" 
      unique_together = (("trabajo", "descripcion"),)

    def cantidad_postulados_casting(self):
      return self.postulacion_set.filter(estado='PC').count()
    cantidad_postulados_casting.short_description = 'Postulados casting'
    def cantidad_seleccionados_casting(self):
      return self.postulacion_set.filter(estado='SC').count()
    cantidad_seleccionados_casting.short_description = 'Selecionados casting'
    def cantidad_seleccionados_trabajo(self):
      return self.postulacion_set.filter(estado='ST').count()
    cantidad_seleccionados_trabajo.short_description = 'Selecionados trabalho'
    def cantidad_trabajos_realizados(self):
      return self.postulacion_set.filter(estado='TR').count()
    cantidad_trabajos_realizados.short_description = 'Trabalhos realizados'
    def cantidad_trabajos_pagados(self):
      return self.postulacion_set.filter(estado='TP').count()
    cantidad_trabajos_pagados.short_description = 'Trabalhos pagados'

class Postulacion(models.Model):
    agenciado = models.ForeignKey(Agenciado,on_delete=models.PROTECT)
    rol = models.ForeignKey(Rol,on_delete=models.PROTECT)
    ESTADO_POSTULACION=(
      ('PC', u'Postulado para casting'),
      ('SC', u'Selecionado para casting'),
      ('ST', u'Selecionado para trabalho'),
      ('TR', u'Trabalho realisado'),
      ('TP', u'Trabalho pagado'),
    )
    DICT_ESTADO_POSTULACION=dict(ESTADO_POSTULACION)
    estado = models.CharField(max_length=2,choices=ESTADO_POSTULACION)
    def __unicode__(self):
      return '%s | %s | %s' % (self.agenciado,Postulacion.DICT_ESTADO_POSTULACION[self.estado],self.rol)
    class Meta:
      ordering = ['-rol__trabajo__fecha_ingreso', 'rol__descripcion', 'agenciado__nombre', 'agenciado__apellido']
      verbose_name = u'Postulaçao'
      verbose_name_plural = u"Postulaçoes" 
      unique_together = (("agenciado", "rol"),)

    def trabajo_rol(self):
      return str(self.rol.trabajo)

    def thumbnail_agenciado_link(self):
      return self.agenciado.thumbnail_agenciado_link()
    thumbnail_agenciado_link.allow_tags = True

    def nombre_agenciado(self):
      return self.agenciado.nombre

    def apellido_agenciado(self):
      return self.agenciado.apellido
