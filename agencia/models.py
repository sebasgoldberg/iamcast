# coding=utf-8
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
from iamsoft.cross.direccion.models import Direccion
from iamsoft.cross.telefono.models import Telefono as BaseTelefono
from perfil.models import Danza, Deporte, EstadoDientes, Idioma, Instrumento, Ojos, Pelo, Piel, Talle
from django.contrib import messages

# @pre Esta rutina se llama desde el metodo clean de una clase que lo redefine y hereda de formset
def validarUnoIngresado(formset,campo,mensaje):
  if any(formset.errors):
    return
  for form in formset.forms:
    if not campo in form.cleaned_data:
      continue
    if form.cleaned_data[campo] != "":
      if not formset.can_delete: 
        return
      if not form.cleaned_data['DELETE']:
        return
  raise ValidationError(mensaje)

def validarDireccionIngresada(formset):
  validarUnoIngresado(formset,'direccion',_(u'Tem que informar o endereço'))

def validarTelefonoIngresado(formset):
  validarUnoIngresado(formset,'telefono',_(u'Tem que informar um telefone'))

def validarFotoIngresada(formset):
  validarUnoIngresado(formset,'foto',_(u'Tem que subir uma foto'))

class Agencia(models.Model):
  nombre = models.CharField(max_length=60, unique=True, verbose_name=ugettext_lazy(u'Nome'), null=False, blank=False)
  email = models.EmailField(verbose_name=ugettext_lazy(u'e-mail'), null=False, blank=False)
  activa = models.BooleanField(default=True, verbose_name=ugettext_lazy(u'Ativa'),help_text=ugettext_lazy(u'Só debería ter uma unica agencia ativa'))
  logo = models.ImageField(upload_to='agencias/logos/', verbose_name=ugettext_lazy(u'Logo'), help_text = ugettext_lazy(u'Logo a ser visualizado no site da agencia'), null=True, blank=True)
  favicon = models.ImageField(upload_to='agencias/logos/', verbose_name=ugettext_lazy(u'Favicon'), help_text=ugettext_lazy(u'Imagem com extenção ico de 48x48 pixels'), null=True, blank=True)
  titulo_home = models.CharField(max_length=100, verbose_name=ugettext_lazy(u'Titulo pagina inicial'), null=True, blank=True)
  presentacion_home = models.TextField(null=True, blank=True, verbose_name=ugettext_lazy(u'Presentação pagina inicial'))
  mapa_contacto = models.TextField(null=True, blank=True, verbose_name=ugettext_lazy(u'Mapa pagina contato'), help_text=ugettext_lazy(u'Aqui tem que colar o HTML gerado no google maps a partir de seu endereço'))
  class Meta:
    ordering = ['nombre']
    verbose_name = ugettext_lazy(u"Agencia")
    verbose_name_plural = ugettext_lazy(u"Agencias")

  def __unicode__(self):
    return self.nombre

  def telefonos(self):
    listado_telefonos = []
    for telefono in self.telefonoagencia_set.all():
      listado_telefonos += [telefono.telefono]
    return listado_telefonos

  def direccion(self):
    direcciones = self.direccionagencia_set.all()
    if direcciones:
      return str(direcciones[0])
    return ''

  @staticmethod
  def get_activa(request=None):
    agencias = Agencia.objects.filter(activa=True).order_by('-id')
    if not agencias:
      mensaje=_(u'Não tem registrada uma agencia ativa. Tem que ser creada una agencia ativa na administracão do site.')
      if request:
        messages.warning(request,mensaje)
      return Agencia(nombre='Agencia',email='mail@agencia.com')
    return agencias[0]

class TelefonoAgencia(BaseTelefono):
  agencia = models.ForeignKey(Agencia,null=False, blank=False, verbose_name=ugettext_lazy(u'Agencia'))
  class Meta:
    verbose_name = ugettext_lazy(u"Telefone da Agencia")
    verbose_name_plural = ugettext_lazy(u"Telefones da Agencia")

class DireccionAgencia(Direccion):
  agencia = models.ForeignKey(Agencia,null=False, blank=False, verbose_name=ugettext_lazy(u'Agencia'))
  class Meta:
    verbose_name = ugettext_lazy(u"Endereço da Agencia")
    verbose_name_plural = ugettext_lazy(u"Endereços da Agencia")

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

    """
    # Datos de direccion
    estado = models.ForeignKey(Estado,on_delete=models.PROTECT,null=True, blank=False, verbose_name=ugettext_lazy(u'Estado'))
    ciudad = models.ForeignKey(Ciudad,on_delete=models.PROTECT, verbose_name=ugettext_lazy(u'Cidade'),null=True, blank=False)
    barrio = models.CharField(max_length=60, verbose_name=ugettext_lazy(u'Barrio'))
    direccion = models.CharField(max_length=120, verbose_name=ugettext_lazy(u'Endereço'))
    codigo_postal = models.CharField(max_length=40, verbose_name=ugettext_lazy(u'CEP'))
    """

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

class DireccionAgenciado(Direccion):
  agenciado = models.ForeignKey(Agenciado, verbose_name=ugettext_lazy(u'Agenciado'))

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

class Telefono(BaseTelefono):
    agenciado = models.ForeignKey(Agenciado)
