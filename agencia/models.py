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
  validarUnoIngresado(formset,'telefono','Tem que informar um telefone')

def validarFotoIngresada(formset):
  validarUnoIngresado(formset,'foto','Tem que subir uma foto')

class Ciudad(models.Model):
    descripcion = models.CharField(max_length=60, unique=True, verbose_name=u'Descripçao')
    def __unicode__(self):
      return self.descripcion
    class Meta:
      ordering = ['descripcion']
      verbose_name = "Cidade"
      verbose_name_plural = "Cidades"

class Danza(models.Model):
    descripcion = models.CharField(max_length=60, unique=True, verbose_name=u'Descripçao')
    def __unicode__(self):
      return self.descripcion
    class Meta:
      ordering = ['descripcion']
      verbose_name = u"Dança"
      verbose_name_plural = u"Danças"

class Deporte(models.Model):
    descripcion = models.CharField(max_length=60, unique=True, verbose_name=u'Descripçao')
    def __unicode__(self):
      return self.descripcion
    class Meta:
      ordering = ['descripcion']
      verbose_name = "Esporte"
      verbose_name_plural = "Esportes"

class Estado(models.Model):
    descripcion = models.CharField(max_length=60, unique=True, verbose_name=u'Descripçao')
    def __unicode__(self):
      return self.descripcion
    class Meta:
      ordering = ['descripcion']

class EstadoDientes(models.Model):
    descripcion = models.CharField(max_length=60, unique=True, verbose_name=u'Descripçao')
    def __unicode__(self):
      return self.descripcion
    class Meta:
      ordering = ['descripcion']
      verbose_name = "Estado Dentes"
      verbose_name_plural = "Estados Dentes"

class Idioma(models.Model):
    descripcion = models.CharField(max_length=60, unique=True, verbose_name=u'Descripçao')
    def __unicode__(self):
      return self.descripcion
    class Meta:
      ordering = ['descripcion']

class Instrumento(models.Model):
    descripcion = models.CharField(max_length=60, unique=True, verbose_name=u'Descripçao')
    def __unicode__(self):
      return self.descripcion
    class Meta:
      ordering = ['descripcion']

class Ojos(models.Model):
    descripcion = models.CharField(max_length=60, unique=True, verbose_name=u'Descripçao')
    def __unicode__(self):
      return self.descripcion
    class Meta:
      ordering = ['descripcion']
      verbose_name = "Olhos"
      verbose_name_plural = "Olhos"

class Pelo(models.Model):
    descripcion = models.CharField(max_length=60, unique=True, verbose_name=u'Descripçao')
    def __unicode__(self):
      return self.descripcion
    class Meta:
      ordering = ['descripcion']
      verbose_name = "Cabelo"
      verbose_name_plural = "Cabelos"

class Piel(models.Model):
    descripcion = models.CharField(max_length=60, unique=True, verbose_name=u'Descripçao')
    def __unicode__(self):
      return self.descripcion
    class Meta:
      ordering = ['descripcion']
      verbose_name = "Pele"
      verbose_name_plural = "Peles"

class Talle(models.Model):
    descripcion = models.CharField(max_length=60, unique=True, verbose_name=u'Descripçao')
    def __unicode__(self):
      return self.descripcion
    class Meta:
      ordering = ['descripcion']
      verbose_name = "Manequem"
      verbose_name_plural = "Manequems"

class Agenciado(models.Model):

    user= models.OneToOneField(User, null=True, blank=True, editable=False)

    #
    mail = models.EmailField(unique=True, verbose_name='e-mail')

    # Datos personales
    nombre = models.CharField(max_length=60, verbose_name='Nome')
    apellido = models.CharField(max_length=60, verbose_name='Sobrenome')
    fecha_nacimiento = models.DateField(verbose_name='Data nascimento')

    # Datos Administrativos
    documento_rg = models.CharField(max_length=60,unique=True, verbose_name='RG')
    documento_cpf = models.CharField(max_length=60,unique=True, verbose_name='CPF')
    responsable = models.CharField(max_length=60, blank=True, verbose_name='Responsabel')
    cuenta_bancaria = models.CharField(max_length=100, blank=True, verbose_name='Conta bancaria')

    # Datos de direccion
    estado = models.ForeignKey(Estado,on_delete=models.PROTECT)
    ciudad = models.ForeignKey(Ciudad,on_delete=models.PROTECT, verbose_name='Cidade')
    barrio = models.CharField(max_length=60)
    direccion = models.CharField(max_length=120, verbose_name='Endereço')
    codigo_postal = models.CharField(max_length=40, verbose_name='CEP')

    # Datos de contacto
    nextel = models.CharField(max_length=60, blank=True)

    # Caracteristicas fisicas
    SEXO=(
      ('M', 'Masculino'),
      ('F', 'Femenino'),
    )
    sexo = models.CharField(max_length=1,choices=SEXO)
    ojos = models.ForeignKey(Ojos,on_delete=models.PROTECT, verbose_name='Olhos')
    pelo = models.ForeignKey(Pelo,on_delete=models.PROTECT, verbose_name='Cabelo')
    piel = models.ForeignKey(Piel,on_delete=models.PROTECT, verbose_name='Pele')
    altura = models.FloatField(verbose_name='Atura')
    peso = models.FloatField()
    talle = models.ForeignKey(Talle,on_delete=models.PROTECT, verbose_name='Manequem')
    talle_camisa = models.IntegerField(verbose_name='Camisa')
    talle_pantalon = models.IntegerField(verbose_name=u'Calça')
    calzado = models.IntegerField(verbose_name=u'Calçado')
    estado_dientes = models.ForeignKey(EstadoDientes,on_delete=models.PROTECT, verbose_name='Estado Dentes')

    # Habilidades
    deportes = models.ManyToManyField(Deporte, blank=True, verbose_name='Esportes')
    danzas = models.ManyToManyField(Danza, blank=True, verbose_name=u"Danças")
    instrumentos = models.ManyToManyField(Instrumento, blank=True)
    idiomas = models.ManyToManyField(Idioma, blank=True)
    indicador_maneja = models.BooleanField(verbose_name='Dirige')
    indicador_tiene_registro = models.BooleanField(verbose_name=u'Habilitaçao')

    # Otros datos
    trabaja_como_extra = models.BooleanField(verbose_name=u'Figuraçao')
    como_nos_conocio = models.TextField(blank=True, verbose_name='Como nos conheceu')
    observaciones = models.TextField(blank=True, verbose_name=u'Observaçoes')

    # Datos administrativos del sistema 
    activo = models.BooleanField(default=True, verbose_name='Ativo')
    fecha_ingreso = models.DateField(default=date.today(), verbose_name='Data de agenciamento')
    recurso_id = models.IntegerField(null=True, editable=False) #Clave en aplicacion DELPHI

    def __unicode__(self):
      return self.nombre+' '+self.apellido

    def thumbnail(self):
      url = ''
      if any(self.fotoagenciado_set.order_by('id')):
        url = self.fotoagenciado_set.order_by('id')[:1][0].foto.url
      return "<img src='%s' height=100 />" % url
    thumbnail.allow_tags = True

    def thumbnails(self):
      html=''
      fotos=self.fotoagenciado_set.order_by('id')
      for foto in fotos:
        url = foto.foto.url
        html = html + "<a href='%s'><img src='%s' height=100 /></a>" % (url,url)
      return html
    thumbnails.allow_tags = True

    def telefonos(self):
      listadoTelefonos=[]
      for telefono in self.telefono_set.all():
        listadoTelefonos.append(telefono.telefono)
      return '<br />'.join(listadoTelefonos)
    telefonos.allow_tags = True
    telefonos.short_description = 'Telefones'


    def descripcion(self):
      return 'Edad %s, sexo %s, olhos %s, cabelo %s, pele %s, atura %s, peso %s, estado dentes %s.'%(str(self.edad()), dict(self.SEXO)[self.sexo],self.ojos,self.pelo,self.piel,self.altura,self.peso, self.estado_dientes)
    def edad(self):
      # @todo Definir como corresponde sin aproximar
      return (date.today()-self.fecha_nacimiento).days/365
    descripcion.short_description = 'Descripçao'

class FotoAgenciado(models.Model):
    agenciado = models.ForeignKey(Agenciado)
    foto = models.ImageField(upload_to='agenciados/fotos/')
    def __unicode__(self):
      return self.foto.url
    class Meta:
      verbose_name = "Foto"
      verbose_name_plural = "Fotos"

class VideoAgenciado(models.Model):
    agenciado = models.ForeignKey(Agenciado)
    url = models.URLField()
    def __unicode__(self):
      return self.url
    class Meta:
      verbose_name = "Video"
      verbose_name_plural = "Videos"

class Compania(models.Model):
    descripcion = models.CharField(max_length=100, unique=True, verbose_name=u'Descripçao')
    def __unicode__(self):
      return self.descripcion
    class Meta:
      ordering = ['descripcion']

class Telefono(models.Model):
    compania = models.ForeignKey(Compania, null=True, blank=True,on_delete=models.PROTECT)
    agenciado = models.ForeignKey(Agenciado)
    telefono = models.CharField(max_length=60)
    def __unicode__(self):
      return self.telefono
