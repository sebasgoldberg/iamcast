# coding=utf-8

from django.db import models
from agencia.models import Agenciado
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill, Adjust
from datetime import date, datetime
from agencia.models import Estado, Ciudad, Compania
from django.contrib.auth.models import User
from django.db.models.signals import pre_save
from django.dispatch import receiver
import re

class Direccion(models.Model):
  descripcion = models.CharField(max_length=60, verbose_name=u'Descripção',blank=True,null=True)
  estado = models.ForeignKey(Estado,on_delete=models.PROTECT,null=True, blank=True, verbose_name=u'Estado')
  ciudad = models.ForeignKey(Ciudad,on_delete=models.PROTECT, verbose_name='Cidade',null=True, blank=True)
  barrio = models.CharField(max_length=60, verbose_name='Barrio', blank=True, null=True)
  direccion = models.CharField(max_length=120, verbose_name='Endereço', blank=True, null=True)
  codigo_postal = models.CharField(max_length=40, verbose_name='CEP', blank=True, null=True)
  class Meta:
    abstract = True
    verbose_name = u"Endereço"
    verbose_name_plural = u"Endereços"

class Telefono(models.Model):
  compania = models.ForeignKey(Compania, null=True, blank=True,on_delete=models.PROTECT,related_name='telefono_productora_set')
  telefono = models.CharField(max_length=60)
  def __unicode__(self):
    return u'%s (%s)' % (self.telefono,self.compania)
  class Meta:
    abstract = True
    verbose_name = u"Telefone"
    verbose_name_plural = u"Telefones"

class Evento(Direccion):
  fecha = models.DateTimeField(default=datetime.today(),verbose_name=u'Data do evento', blank=True, null=True)
  class Meta:
    abstract = True
    verbose_name = u'Evento'
    verbose_name_plural = u'Eventos'

class Productora(models.Model):
  user= models.OneToOneField(User, null=True, blank=True, editable=False)

  # Datos 
  nombre = models.CharField(max_length=60, verbose_name='Nome')
  mail = models.EmailField(verbose_name='e-mail')

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

  def telefonos(self):
    html = '<ul>'
    for telefono in self.telefonoproductora_set.all():
      html += '<li>%s</li>'%telefono
    html += '</ul>'
    return html
  telefonos.allow_tags = True
  telefonos.short_description = u'Telefones'

  def trabajos_activos(self):
    html = '<ul>'
    for trabajo in Trabajo.filter_activos(self.trabajo_set):
      html += '<li>%s</li>'%trabajo.admin_link()
    html += '</ul>'
    return html
  trabajos_activos.allow_tags = True
  trabajos_activos.short_description = u'Trabalhos ativos'
    
  def trabajos_iniciados(self):
    html = '<ul>'
    for trabajo in Trabajo.filter_iniciados(self.trabajo_set):
      html += '<li>%s</li>'%trabajo.admin_link()
    html += '</ul>'
    return html
  trabajos_iniciados.allow_tags = True
  trabajos_iniciados.short_description = u'Trabalhos iniciados'
    

class DireccionProductora(Direccion):
  productora = models.ForeignKey(Productora, verbose_name=u'Produtora')
  def __unicode__(self):
    return u'%s, %s, %s, %s, %s (%s)' % (self.direccion, self.barrio, self.ciudad, self.estado, self.codigo_postal, self.descripcion)

class TelefonoProductora(Telefono):
  productora = models.ForeignKey(Productora, verbose_name=u'Produtora')

class ItemPortfolio(models.Model):
    titulo = models.CharField(max_length=100, unique_for_date='fecha')
    video = models.URLField(unique=True, null=True, blank=True)
    codigo_video = models.CharField(max_length=30, unique=True, null=True, blank=True)
    # agregar rutas a configuracion del apache, al archivo settings y crear carpetas correspondientes
    imagen = models.ImageField(upload_to='trabajo/portfolio/', null=True, blank=True)
    thumbnail = ImageSpecField([Adjust(contrast=1.2, sharpness=1.1), ResizeToFill(358,202)], image_field='imagen', format='JPEG', options={'quality': 90})
    fecha = models.DateField(default=date.today(),verbose_name=u'Data')
    def __unicode__(self):
      return self.titulo
    class Meta:
      ordering = ['-fecha']
      verbose_name = u"Item Portfolio"
      verbose_name_plural = u"Portfolio"
    def get_youtube_iframe_url(self):
      return (u'http://www.youtube.com/embed/%s' % self.codigo_video)
    get_youtube_iframe_url.allow_tags = True
    def html_youtube_iframe(self):
      return '<iframe width="358" height="202" src="%s" frameborder="0" allowfullscreen></iframe>' % self.get_youtube_iframe_url()
    html_youtube_iframe.allow_tags = True 
    html_youtube_iframe.short_description = u'Video'
    def html_small_youtube_iframe(self):
      return '<iframe width="186" height="105" src="%s" frameborder="0" allowfullscreen></iframe>' % self.get_youtube_iframe_url()
    html_small_youtube_iframe.allow_tags = True 
    html_small_youtube_iframe.short_description = u'Video'
    def html_media(self):
      if self.codigo_video:
        return self.html_youtube_iframe()
      else:
        return self.html_thumbnail()
    html_media.allow_tags = True
    html_media.short_description = u'Video ou imagem'
    def html_small_media(self):
      if self.codigo_video:
        return self.html_small_youtube_iframe()
      else:
        return self.html_thumbnail()
    html_small_media.allow_tags = True
    html_small_media.short_description = u'Video ou imagem'
    def html_thumbnail(self):
      if not self.imagen:
        return
      return "<a href='%s'><img src='%s'/></a>" % (self.imagen.url, self.thumbnail.url)

    def url_to_codigo_video(self):
      if self.video is None:
        return
      if re.search('^.*v=',self.video):
        self.codigo_video = re.sub('^.*v=','',self.video)
        self.codigo_video = re.sub('&.*$','',self.codigo_video)
      elif re.search('[^?]',self.video):
        self.codigo_video = re.sub('^.*/','',self.video)

@receiver(pre_save, sender=ItemPortfolio)
def callback_save_item_portfolio(sender, instance, raw, using, **kwargs):
  instance.url_to_codigo_video()

class Trabajo(models.Model):
    titulo = models.CharField(max_length=100, unique_for_date='fecha_ingreso')
    productora= models.ForeignKey(Productora,on_delete=models.PROTECT, verbose_name=u'Produtora')
    descripcion = models.TextField(verbose_name=u'Descripção')
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

    @staticmethod
    def filter_iniciados(queryset):
      return queryset.filter(estado='IN')

    @staticmethod
    def filter_activos(queryset):
      return queryset.filter(estado='AT')

    def __unicode__(self):
      return u'%s (%s)' % (self.titulo, self.fecha_ingreso)
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
    thumbnail_img.short_description = u'Imagem'

    def thumbnail_img_link(self):
      url = ''
      if self.thumbnail:
        url = self.thumbnail.url
      return "<a href='%s'><img src='%s' height=100 /></a>" % (self.imagen.url, url)
    thumbnail_img_link.allow_tags = True
    thumbnail_img_link.short_description = u'Imagem'

    def roles(self):
      roles=self.rol_set.all()
      html = '</ul>'
      for rol in roles:
        html+='<li>%s</li>' % rol.admin_link()
      html += '</ul>'
      return html
    roles.allow_tags = True
    roles.short_description = u'Perfis'

    def productora_admin_link(self):
      if self.productora.id is None:
        return None
      return "<a href='/admin/trabajo/productora/%s/'>%s</a>" % (self.productora.id, str(self.productora))
    productora_admin_link.allow_tags=True
    productora_admin_link.short_description = u'Link a produtora'

    def admin_link(self):
      if self.id is None:
        return None
      return "<a href='/admin/trabajo/trabajo/%s/'>%s</a>" % (self.id, str(self))
    admin_link.allow_tags=True
    admin_link.short_description = u'Link ao trabalho'

TIPO_EVENTO_TRABAJO=(
  ('C', u'Casting'),
  ('B', u'Callback'),
  ('P', u'Proba de roupa'),
  ('R', u'Realização do trabalho'),
  ('O', u'Outro'),
)
DICT_TIPO_EVENTO_TRABAJO=dict(TIPO_EVENTO_TRABAJO)

class EventoTrabajo(Evento):
  tipo = models.CharField(max_length=1,choices=TIPO_EVENTO_TRABAJO)
  trabajo = models.ForeignKey(Trabajo,on_delete=models.PROTECT)
  class Meta(Evento.Meta):
    verbose_name = 'Evento do trabalho'
    verbose_name_plural = 'Eventos do trabalho'
  def descripcion_tipo(self):
    return DICT_TIPO_EVENTO_TRABAJO[self.tipo]
  def __unicode__(self):
    return u'%s | %s | %s | %s, %s, %s, %s, %s' % (EventoTrabajo.descripcion_tipo(self), self.descripcion, self.fecha, self.direccion, self.barrio, self.ciudad, self.estado, self.codigo_postal)

class Rol(models.Model):
    trabajo = models.ForeignKey(Trabajo,on_delete=models.PROTECT)
    descripcion = models.CharField(max_length=60, verbose_name=u'Descripção')
    cache = models.DecimalField(max_digits=15, decimal_places=4, null=True, blank=True)
    caracteristicas = models.TextField(verbose_name=u'Caraterísticas')
    def __unicode__(self):
      return u'%s (%s)' % (self.descripcion, self.trabajo.titulo)
    class Meta:
      ordering = ['-trabajo__fecha_ingreso','descripcion']
      verbose_name = u"Perfil"
      verbose_name_plural = u"Perfis" 
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

    def admin_link(self):
      if self.id is None:
        return None
      return "<a href='/admin/trabajo/rol/%s/'>%s</a>" % (self.id, str(self))
    admin_link.allow_tags = True
    admin_link.short_description = u'Link ao perfil'

    def trabajo_admin_link(self):
      return self.trabajo.admin_link()
    trabajo_admin_link.allow_tags=True
    trabajo_admin_link.short_description = u'Link ao trabalho'

class EventoRol(Evento):
  tipo = models.CharField(max_length=1,choices=TIPO_EVENTO_TRABAJO)
  rol = models.ForeignKey(Rol,on_delete=models.PROTECT,verbose_name = 'Perfil')
  class Meta(Evento.Meta):
    verbose_name = 'Evento do perfil'
    verbose_name_plural = 'Eventos do perfil'
  def descripcion_tipo(self):
    return DICT_TIPO_EVENTO_TRABAJO[self.tipo]
  def __unicode__(self):
    return u'%s | %s | %s | %s, %s, %s, %s, %s' % (self.descripcion_tipo, self.descripcion, self.fecha, self.direccion, self.barrio, self.ciudad, self.estado, self.codigo_postal)

class Postulacion(models.Model):
    agenciado = models.ForeignKey(Agenciado,on_delete=models.PROTECT)
    rol = models.ForeignKey(Rol,on_delete=models.PROTECT, verbose_name = 'Perfil')
    ESTADO_POSTULACION=(
      ('PA', u'Postulação feita pelo agenciado'),
      ('PC', u'Postulado para casting'),
      ('SC', u'Selecionado para casting'),
      ('ST', u'Selecionado para trabalho'),
      ('TR', u'Trabalho realisado'),
      ('TP', u'Trabalho pagado'),
    )
    DICT_ESTADO_POSTULACION=dict(ESTADO_POSTULACION)
    estado = models.CharField(max_length=2,choices=ESTADO_POSTULACION)
    def __unicode__(self):
      return u'%s | %s | %s' % (self.agenciado,Postulacion.DICT_ESTADO_POSTULACION[self.estado],self.rol)
    class Meta:
      ordering = ['-rol__trabajo__fecha_ingreso', 'rol__descripcion', 'agenciado__nombre', 'agenciado__apellido']
      verbose_name = u'Postulação'
      verbose_name_plural = u"Postulaçoes" 
      unique_together = (("agenciado", "rol"),)

    def trabajo_rol(self):
      return str(self.rol.trabajo)

    def thumbnail_agenciado_link(self):
      return self.agenciado.thumbnail_agenciado_link()
    thumbnail_agenciado_link.allow_tags = True
    thumbnail_agenciado_link.short_description = u'Link ao agenciado'

    def nombre_agenciado(self):
      return self.agenciado.nombre

    def apellido_agenciado(self):
      return self.agenciado.apellido

    def agenciado_admin_link(self):
      if self.agenciado.id is None:
        return ''
      return "<a href='/admin/agencia/agenciado/%s/'>%s</a>" % (self.agenciado.id, self.agenciado)
    agenciado_admin_link.allow_tags = True
    agenciado_admin_link.short_description = u'Link ao agenciado'

    def rol_admin_link(self):
      return self.rol.admin_link()
    rol_admin_link.allow_tags = True
    rol_admin_link.short_description = u'Link ao perfil'

    def descripcion_estado(self):
      return Postulacion.DICT_ESTADO_POSTULACION[self.estado]

