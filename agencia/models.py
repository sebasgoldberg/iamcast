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
from django.contrib.auth.models import User
from datetime import date
from django.core.exceptions import ValidationError
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill, Adjust
from django.conf import settings
from agencia.video import Video
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.translation import ugettext as _
from django.utils.translation import ugettext_lazy

# @pre Esta rutina se llama desde el metodo clean de una clase que lo redefine y hereda de formset
def validarUnoIngresado(formset,campo,mensaje):
  if any(formset.errors):
    return
  for form in formset.forms:
    if not campo in form.cleaned_data:
      continue
    if form.cleaned_data[campo] != "" and not form.cleaned_data['DELETE']:
      return
  raise ValidationError(mensaje)

def validarTelefonoIngresado(formset):
  validarUnoIngresado(formset,'telefono',_(u'Tem que informar um telefone'))

def validarFotoIngresada(formset):
  validarUnoIngresado(formset,'foto',_(u'Tem que subir uma foto'))

class Ciudad(models.Model):
    descripcion = models.CharField(max_length=60, unique=True, verbose_name=ugettext_lazy(u'Descripção'))
    def __unicode__(self):
      return self.descripcion
    class Meta:
      ordering = ['descripcion']
      verbose_name = ugettext_lazy(u"Cidade")
      verbose_name_plural = ugettext_lazy(u"Cidades")

class Danza(models.Model):
    descripcion = models.CharField(max_length=60, unique=True, verbose_name=ugettext_lazy(u'Descripção'))
    def __unicode__(self):
      return self.descripcion
    class Meta:
      ordering = ['descripcion']
      verbose_name = ugettext_lazy(u"Dança")
      verbose_name_plural = ugettext_lazy(u"Danças")

class Deporte(models.Model):
    descripcion = models.CharField(max_length=60, unique=True, verbose_name=ugettext_lazy(u'Descripção'))
    def __unicode__(self):
      return self.descripcion
    class Meta:
      ordering = ['descripcion']
      verbose_name = ugettext_lazy(u"Esporte")
      verbose_name_plural = ugettext_lazy(u"Esportes")

class Estado(models.Model):
    descripcion = models.CharField(max_length=60, unique=True, verbose_name=ugettext_lazy(u'Descripção'))
    def __unicode__(self):
      return self.descripcion
    class Meta:
      ordering = ['descripcion']

class EstadoDientes(models.Model):
    descripcion = models.CharField(max_length=60, unique=True, verbose_name=ugettext_lazy(u'Descripção'))
    def __unicode__(self):
      return self.descripcion
    class Meta:
      ordering = ['descripcion']
      verbose_name = ugettext_lazy(u"Estado Dentes")
      verbose_name_plural = ugettext_lazy(u"Estados Dentes")

class Idioma(models.Model):
    descripcion = models.CharField(max_length=60, unique=True, verbose_name=ugettext_lazy(u'Descripção'))
    def __unicode__(self):
      return self.descripcion
    class Meta:
      ordering = ['descripcion']

class Instrumento(models.Model):
    descripcion = models.CharField(max_length=60, unique=True, verbose_name=ugettext_lazy(u'Descripção'))
    def __unicode__(self):
      return self.descripcion
    class Meta:
      ordering = ['descripcion']

class Ojos(models.Model):
    descripcion = models.CharField(max_length=60, unique=True, verbose_name=ugettext_lazy(u'Descripção'))
    def __unicode__(self):
      return self.descripcion
    class Meta:
      ordering = ['descripcion']
      verbose_name = ugettext_lazy(u"Olhos")
      verbose_name_plural = ugettext_lazy(u"Olhos")

class Pelo(models.Model):
    descripcion = models.CharField(max_length=60, unique=True, verbose_name=ugettext_lazy(u'Descripção'))
    def __unicode__(self):
      return self.descripcion
    class Meta:
      ordering = ['descripcion']
      verbose_name = ugettext_lazy(u"Cabelo")
      verbose_name_plural = ugettext_lazy(u"Cabelos")

class Piel(models.Model):
    descripcion = models.CharField(max_length=60, unique=True, verbose_name=ugettext_lazy(u'Descripção'))
    def __unicode__(self):
      return self.descripcion
    class Meta:
      ordering = ['descripcion']
      verbose_name = ugettext_lazy(u"Pele")
      verbose_name_plural = ugettext_lazy(u"Peles")

class Talle(models.Model):
    descripcion = models.CharField(max_length=60, unique=True, verbose_name=ugettext_lazy(u'Descripção'))
    def __unicode__(self):
      return self.descripcion
    class Meta:
      ordering = ['descripcion']
      verbose_name = ugettext_lazy(u"Manequem")
      verbose_name_plural = ugettext_lazy(u"Manequems")

def validate_fecha_nacimiento(value):
  if value > date.today():
    raise ValidationError(_(u'A data de nascimento nao pode ser maior que a data do dia'))

def validate_altura(value):
  if value < 15:
    raise ValidationError(_(u'A atura debe ser informada em centimetros'))

class Agenciado(models.Model):

    user= models.OneToOneField(User, null=True, blank=True, editable=False)

    # @todo Ver si se puede quitar null luego de migrar, agregar validacion de que si ya existe que tenga asignado responsable
    # @todo Agregar validación de obligatoriedad cuando no es editado por un agenciador
    mail = models.EmailField(verbose_name=ugettext_lazy(u'e-mail'), null=True, blank=False)

    # Datos personales
    nombre = models.CharField(max_length=60, verbose_name=ugettext_lazy(u'Nome'))
    apellido = models.CharField(max_length=60, verbose_name=ugettext_lazy(u'Sobrenome'))
    fecha_nacimiento = models.DateField(verbose_name=ugettext_lazy(u'Data nascimento'),validators=[validate_fecha_nacimiento])

    # Datos Administrativos
    # @todo Ver si se puede quitar null luego de migrar, agregar validacion de que si ya existe que tenga asignado responsable
    documento_rg = models.CharField(max_length=60, verbose_name=ugettext_lazy(u'RG'))
    # @todo Ver si se puede quitar null luego de migrar, agregar validacion de que si ya existe que tenga asignado responsable
    documento_cpf = models.CharField(max_length=60, verbose_name=ugettext_lazy(u'CPF'),null=True)
    responsable = models.CharField(max_length=60, blank=True, verbose_name=ugettext_lazy(u'Responsabel'))
    cuenta_bancaria = models.CharField(max_length=100, blank=True, verbose_name=ugettext_lazy(u'Conta bancaria'))

    # Datos de direccion
    estado = models.ForeignKey(Estado,on_delete=models.PROTECT,null=True, blank=False, verbose_name=ugettext_lazy(u'Estado'))
    ciudad = models.ForeignKey(Ciudad,on_delete=models.PROTECT, verbose_name=ugettext_lazy(u'Cidade'),null=True, blank=False)
    barrio = models.CharField(max_length=60, verbose_name=ugettext_lazy(u'Barrio'))
    direccion = models.CharField(max_length=120, verbose_name=ugettext_lazy(u'Endereço'))
    codigo_postal = models.CharField(max_length=40, verbose_name=ugettext_lazy(u'CEP'))

    # Caracteristicas fisicas
    SEXO=(
      ('M', _(u'Masculino')),
      ('F', _(u'Femenino')),
    )
    DICT_SEXO=dict(SEXO)
    sexo = models.CharField(max_length=1,choices=SEXO, verbose_name=ugettext_lazy(u'Sexo'))
    ojos = models.ForeignKey(Ojos,on_delete=models.PROTECT, verbose_name=ugettext_lazy(u'Olhos'),null=True, blank=False)
    pelo = models.ForeignKey(Pelo,on_delete=models.PROTECT, verbose_name=ugettext_lazy(u'Cabelo'),null=True, blank=False)
    piel = models.ForeignKey(Piel,on_delete=models.PROTECT, verbose_name=ugettext_lazy(u'Pele'),null=True, blank=False)
    altura = models.FloatField(verbose_name=ugettext_lazy(u'Atura'),validators=[validate_altura])
    peso = models.FloatField(verbose_name=ugettext_lazy(u'Peso'))
    talle = models.ForeignKey(Talle,on_delete=models.PROTECT, verbose_name=ugettext_lazy(u'Manequem'),null=True, blank=False)
    talle_camisa = models.IntegerField(verbose_name=ugettext_lazy(u'Camisa'))
    talle_pantalon = models.IntegerField(verbose_name=ugettext_lazy(u'Calça'))
    calzado = models.IntegerField(verbose_name=ugettext_lazy(u'Calçado'))
    estado_dientes = models.ForeignKey(EstadoDientes,on_delete=models.PROTECT, verbose_name=ugettext_lazy(u'Estado Dentes'),null=True, blank=False)

    # Habilidades
    deportes = models.ManyToManyField(Deporte, blank=True, verbose_name=ugettext_lazy(u'Esportes'))
    danzas = models.ManyToManyField(Danza, blank=True, verbose_name=ugettext_lazy(u"Danças"))
    instrumentos = models.ManyToManyField(Instrumento, blank=True, verbose_name=ugettext_lazy(u'Instrumentos'))
    idiomas = models.ManyToManyField(Idioma, blank=True, verbose_name=ugettext_lazy(u'Idiomas'))
    indicador_maneja = models.BooleanField(verbose_name=ugettext_lazy(u'Dirige'))
    indicador_tiene_registro = models.BooleanField(verbose_name=ugettext_lazy(u'Habilitação'))

    # Otros datos
    trabaja_como_extra = models.BooleanField(verbose_name=ugettext_lazy(u'Figuração'))
    como_nos_conocio = models.TextField(blank=True, verbose_name=ugettext_lazy(u'Como nos conheceu'))
    observaciones = models.TextField(blank=True, verbose_name=ugettext_lazy(u'Observaçoes'))

    # Datos administrativos del sistema 
    activo = models.BooleanField(default=True, verbose_name=ugettext_lazy(u'Ativo'))
    fecha_ingreso = models.DateField(default=date.today(), verbose_name=ugettext_lazy(u'Data de agenciamento'))
    recurso_id = models.IntegerField(null=True, editable=False) #Clave en aplicacion DELPHI

    def __unicode__(self):
      return u'%s %s (%s)' % (self.nombre, self.apellido, self.fecha_nacimiento)

    def thumbnail(self):
      url = ''
      if any(self.fotoagenciado_set.order_by('id')):
        url = self.fotoagenciado_set.order_by('id')[:1][0].thumbnail.url
      return "<img src='%s' height=100 />" % url
    thumbnail.allow_tags = True
    thumbnail.short_description = ugettext_lazy(u'Imagem')

    def thumbnail_url(self):
      url = ''
      if any(self.fotoagenciado_set.order_by('id')):
        url = self.fotoagenciado_set.order_by('id')[:1][0].thumbnail.url
      return url

    def thumbnails(self):
      html=''
      fotos=self.fotoagenciado_set.order_by('id')
      for foto in fotos:
        url = foto.foto.url
        url_thumbnail = foto.thumbnail.url
        html = html + "<a href='%s'><img src='%s' height=100 /></a>" % (url,url_thumbnail)
      return html
    thumbnails.allow_tags = True
    thumbnails.short_description = ugettext_lazy(u'Imagems')

    def thumbnails_absolute_uri(self):
      html=''
      fotos=self.fotoagenciado_set.order_by('id')
      for foto in fotos:
        url = "http://%s%s" % (settings.AMBIENTE.dominio, foto.foto.url)
        url_thumbnail = "http://%s%s" % (settings.AMBIENTE.dominio, foto.thumbnail.url)
        html = html + "<a href='%s'><img src='%s' height=100 /></a>" % (url,url_thumbnail)
      return html
    thumbnails_absolute_uri.allow_tags = True
    thumbnails_absolute_uri.short_description = ugettext_lazy(u'Imagems')

    def thumbnail_agenciado_link(self):
      return "<a href='/admin/agencia/agenciado/%s/'>%s</a>" % (str(self.id),self.thumbnail())
    thumbnail_agenciado_link.allow_tags = True
    thumbnail_agenciado_link.short_description = ugettext_lazy(u'Link ao agenciado')

    def html_small_youtube_iframes(self):
      html=''
      for video in self.videoagenciado_set.all():
        html="%s %s"%(html,video.html_small_youtube_iframe())
      return html
    html_small_youtube_iframes.allow_tags = True
    html_small_youtube_iframes.short_description = ugettext_lazy(u'Video')

    def telefonos(self):
      listadoTelefonos=[]
      for telefono in self.telefono_set.all():
        if telefono.compania is not None:
          listadoTelefonos.append('%s: %s' % (telefono.compania, telefono.telefono))
        else:
          listadoTelefonos.append(telefono.telefono)
      return '<br />'.join(listadoTelefonos)
    telefonos.allow_tags = True
    telefonos.short_description = ugettext_lazy(u'Telefones')

    def admin_link(self):
      if self is None:
        return ''
      return "<a href='/admin/agencia/agenciado/%s/'>%s</a>" % (self.id,self)
    admin_link.allow_tags=True
    admin_link.short_description = ugettext_lazy(u'Link ao agenciado')

    def descripcion(self):
      return _(u'Edad %(edad)s, sexo %(sexo)s, olhos %(ojos)s, cabelo %(pelo)s, pele %(piel)s, atura %(altura)s, peso %(peso)s, estado dentes %(estado_dientes)s.')%{'edad':str(self.edad()), 'sexo':Agenciado.DICT_SEXO[self.sexo], 'ojos':self.ojos, 'pelo':self.pelo, 'piel':self.piel, 'altura':self.altura, 'peso':self.peso, 'estado_dientes':self.estado_dientes}
    def edad(self):
      return (date.today()-self.fecha_nacimiento).days/365
    descripcion.short_description = ugettext_lazy(u'Descripção')

    def ids_roles_postulaciones(self):
      return [ postulacion.rol.id for postulacion in self.postulacion_set.all() ]

    class Meta:
      ordering = ['nombre', 'apellido']

class FotoAgenciado(models.Model):
    agenciado = models.ForeignKey(Agenciado)
    foto = models.ImageField(upload_to='agenciados/fotos/')
    thumbnail = ImageSpecField([Adjust(contrast=1.2, sharpness=1.1), ResizeToFill(100,100)], image_field='foto', format='JPEG', options={'quality': 90})
    mini_thumbnail = ImageSpecField([Adjust(contrast=1.2, sharpness=1.1), ResizeToFill(60,60)], image_field='foto', format='JPEG', options={'quality': 90})
    def __unicode__(self):
      return self.foto.url
    class Meta:
      verbose_name = ugettext_lazy(u"Foto")
      verbose_name_plural = ugettext_lazy(u"Fotos")

class VideoAgenciado(Video):
  agenciado = models.ForeignKey(Agenciado)

@receiver(pre_save, sender=VideoAgenciado)
def callback_pre_save_videoagenciado(sender, instance, raw, using, **kwargs):
  instance.url_to_codigo_video()

class Compania(models.Model):
    descripcion = models.CharField(max_length=100, unique=True, verbose_name=ugettext_lazy(u'Descripção'))
    def __unicode__(self):
      return self.descripcion
    class Meta:
      ordering = ['descripcion']

class Telefono(models.Model):
    compania = models.ForeignKey(Compania, null=True, blank=True,on_delete=models.PROTECT, verbose_name=ugettext_lazy(u'Compania'))
    agenciado = models.ForeignKey(Agenciado)
    telefono = models.CharField(max_length=60)
    def __unicode__(self):
      return self.telefono
   
