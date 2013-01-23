# coding=utf-8

from django.db import models
from agencia.models import Agenciado
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill, Adjust
from datetime import date, datetime
from agencia.models import Estado, Ciudad, Compania
from django.contrib.auth.models import User

class Productora(models.Model):
  user= models.OneToOneField(User, null=True, blank=True, editable=False)

  # Datos 
  nombre = models.CharField(max_length=60, verbose_name='Nome')
  mail = models.EmailField(verbose_name='e-mail')

  # Datos de direccion
  estado = models.ForeignKey(Estado,on_delete=models.PROTECT,null=True, blank=False)
  ciudad = models.ForeignKey(Ciudad,on_delete=models.PROTECT, verbose_name='Cidade',null=True, blank=False)
  barrio = models.CharField(max_length=60)
  direccion = models.CharField(max_length=120, verbose_name='Endereço')
  codigo_postal = models.CharField(max_length=40, verbose_name='CEP')

  imagen = models.ImageField(upload_to='trabajo/productora/', null=True, blank=True)
  thumbnail = ImageSpecField(
    [Adjust(contrast=1.2, sharpness=1.1), ResizeToFill(100,100)],
    image_field='imagen', format='JPEG', options={'quality': 90}
    )
  def __unicode__(self):
    return self.nombre
  class Meta:
    ordering = ['nombre']
    verbose_name = u"Produtora"
    verbose_name_plural = u"Produtoras"

class Telefono(models.Model):
  compania = models.ForeignKey(Compania, null=True, blank=True,on_delete=models.PROTECT,related_name='telefono_productora_set')
  productora = models.ForeignKey(Productora, verbose_name=u'Produtora')
  telefono = models.CharField(max_length=60)
  def __unicode__(self):
    return self.telefono

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

# @todo agregar direeccion, horario y fecha del test 
class Trabajo(models.Model):
    titulo = models.CharField(max_length=100, unique_for_date='fecha_ingreso')
    productora= models.ForeignKey(Productora,on_delete=models.PROTECT)
    descripcion = models.TextField(verbose_name=u'Descripçao')
    imagen = models.ImageField(upload_to='trabajo/trabajo/',blank=True)
    thumbnail = ImageSpecField([Adjust(contrast=1.2, sharpness=1.1), ResizeToFill(100,100)], image_field='imagen', format='JPEG', options={'quality': 90})
    ESTADO_TRABAJO=(
      ('IN',u'Inicial'),
      ('AT',u'Ativo'),
      ('PC',u'Pendente de cobrar'),
      ('FI',u'Finalizado'),
    )
    estado = models.CharField(max_length=2,choices=ESTADO_TRABAJO,null=False)
# @todo agregar validación entre secuencia de las distintas fechas
    fecha_ingreso = models.DateField(default=date.today(),verbose_name=u'Data ingreso')

    # Datos del test
    fecha_test = models.DateTimeField(default=datetime.today(),verbose_name=u'Data do test')
    estado_test = models.ForeignKey(Estado,on_delete=models.PROTECT,null=True, blank=False, related_name='test_set')
    ciudad_test = models.ForeignKey(Ciudad,on_delete=models.PROTECT, verbose_name='Cidade',null=True, blank=False, related_name='test_set')
    barrio_test = models.CharField(max_length=60)
    direccion_test = models.CharField(max_length=120, verbose_name='Endereço')

    # Datos del trabajo
    fecha_trabajo = models.DateTimeField(default=datetime.today(),verbose_name=u'Data do trabalho')
    estado_trabajo = models.ForeignKey(Estado,on_delete=models.PROTECT,null=True, blank=False, related_name='trabajo_set')
    ciudad_trabajo = models.ForeignKey(Ciudad,on_delete=models.PROTECT, verbose_name='Cidade',null=True, blank=False, related_name='trabajo_set')
    barrio_trabajo = models.CharField(max_length=60)
    direccion_trabajo = models.CharField(max_length=120, verbose_name='Endereço')

    def __unicode__(self):
      return '%s (%s)' % (self.titulo, self.fecha_ingreso)
    class Meta:
      verbose_name = u'Trabalho'
      verbose_name_plural = u"Trabalhos e roles" 
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

    def roles(self):
      roles=self.rol_set.all()
      html = '</ul>'
      for rol in roles:
        html+='<li>%s</li>' % rol.rol_admin_link()
      html += '</ul>'
      return html
    roles.allow_tags = True

class Rol(models.Model):
    trabajo = models.ForeignKey(Trabajo,on_delete=models.PROTECT)
    descripcion = models.CharField(max_length=60, verbose_name=u'Descripçao')
    caracteristicas = models.TextField(verbose_name=u'Caraterísticas')
    def __unicode__(self):
      return '%s (%s)' % (self.descripcion, self.trabajo.titulo)
    class Meta:
      ordering = ['-trabajo__fecha_ingreso','descripcion']
      verbose_name = u"Rol"
      verbose_name_plural = u"Roles e postulaçoes" 
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

    def rol_admin_link(self):
      if self.id is None:
        return None
      return "<a href='/admin/trabajo/rol/%s/'>%s</a>" % (self.id, str(self))
    rol_admin_link.allow_tags=True

    def trabajo_admin_link(self):
      if self.trabajo.id is None:
        return None
      return "<a href='/admin/trabajo/trabajo/%s/'>%s</a>" % (self.trabajo.id, str(self.trabajo))
    trabajo_admin_link.allow_tags=True

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

