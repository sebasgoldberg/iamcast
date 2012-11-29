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
    descripcion = models.CharField(max_length=60, unique=True)
    def __unicode__(self):
      return self.descripcion

class Danza(models.Model):
    descripcion = models.CharField(max_length=60, unique=True)
    def __unicode__(self):
      return self.descripcion

class Deporte(models.Model):
    descripcion = models.CharField(max_length=60, unique=True)
    def __unicode__(self):
      return self.descripcion

class Estado(models.Model):
    descripcion = models.CharField(max_length=60, unique=True)
    def __unicode__(self):
      return self.descripcion

class EstadoDientes(models.Model):
    descripcion = models.CharField(max_length=60, unique=True)
    def __unicode__(self):
      return self.descripcion

class Idioma(models.Model):
    descripcion = models.CharField(max_length=60, unique=True)
    def __unicode__(self):
      return self.descripcion

class Instrumento(models.Model):
    descripcion = models.CharField(max_length=60, unique=True)
    def __unicode__(self):
      return self.descripcion

class Ojos(models.Model):
    descripcion = models.CharField(max_length=60, unique=True)
    def __unicode__(self):
      return self.descripcion

class Pelo(models.Model):
    descripcion = models.CharField(max_length=60, unique=True)
    def __unicode__(self):
      return self.descripcion

class Piel(models.Model):
    descripcion = models.CharField(max_length=60, unique=True)
    def __unicode__(self):
      return self.descripcion

class Talle(models.Model):
    descripcion = models.CharField(max_length=60, unique=True)
    def __unicode__(self):
      return self.descripcion

class Agenciado(models.Model):
    def save(self, *args, **kwargs):

      if not self.user:
        if self.mail != '':
          password = User.objects.make_random_password()
          self.user = User.objects.create_user(self.mail,self.mail,password)
          #self.user = User.objects.create_user(self.mail,self.mail)
          # @todo Notificar de la creacion del usuario
          from django.core.mail import EmailMessage
          cuerpo="\
Oi %s!\n\
\n\
Voce tem uma nova conta em http://192.168.15.128:8000/agencia/agenciado/ com dados de sue perfil.\n\
\n\
Voce podera ingresar a sua nova conta com seu usuario (%s) e sua clave (%s).\n\
\n\
Por favor, verifique se os dados da sua conta som corretos. Em caso de precisar modifique os dados que correspondam.\n\
\n\
Atentamente, o equipe da Alternativa" % (self.nombre,self.user.username,password)
          email = EmailMessage('AgenciaAlternativa - Tu perfila a sido creado', cuerpo, to=['agencia.test@gmail.com'])
          email.send()

      super(Agenciado, self).save(args,kwargs)


    user= models.OneToOneField(User, null=True, blank=True, editable=False)

    #
    mail = models.EmailField(unique=True)

    # Datos personales
    nombre = models.CharField(max_length=60)
    apellido = models.CharField(max_length=60)
    fecha_nacimiento = models.DateField()

    # Datos Administrativos
    documento_rg = models.CharField(max_length=60,unique=True)
    documento_cpf = models.CharField(max_length=60,unique=True)
    responsable = models.CharField(max_length=60, blank=True)
    cuenta_bancaria = models.CharField(max_length=100, blank=True)

    # Datos de direccion
    estado = models.ForeignKey(Estado)
    ciudad = models.ForeignKey(Ciudad)
    barrio = models.CharField(max_length=60)
    direccion = models.CharField(max_length=120)
    codigo_postal = models.CharField(max_length=40)

    # Datos de contacto
    nextel = models.CharField(max_length=60, blank=True)

    # Caracteristicas fisicas
    SEXO=(
      ('M', 'Masculino'),
      ('F', 'Femenino'),
    )
    sexo = models.CharField(max_length=1,choices=SEXO)
    ojos = models.ForeignKey(Ojos)
    pelo = models.ForeignKey(Pelo)
    piel = models.ForeignKey(Piel)
    altura = models.FloatField()
    peso = models.FloatField()
    talle = models.ForeignKey(Talle)
    talle_camisa = models.IntegerField()
    talle_pantalon = models.IntegerField()
    calzado = models.IntegerField()
    estado_dientes = models.ForeignKey(EstadoDientes)

    # Habilidades
    deportes = models.ManyToManyField(Deporte, blank=True)
    danzas = models.ManyToManyField(Danza, blank=True)
    instrumentos = models.ManyToManyField(Instrumento, blank=True)
    idiomas = models.ManyToManyField(Idioma, blank=True)
    indicador_maneja = models.BooleanField()
    indicador_tiene_registro = models.BooleanField()

    # Otros datos
    trabaja_como_extra = models.BooleanField()
    como_nos_conocio = models.TextField(blank=True)
    observaciones = models.TextField(blank=True)

    # Datos administrativos del sistema 
    activo = models.BooleanField()
    fecha_ingreso = models.DateField()
    recurso_id = models.IntegerField(null=True, editable=False) #Clave en aplicacion DELPHI

    def __unicode__(self):
      return self.nombre+' '+self.apellido

    def thumbnail(self):
      url = ''
      if any(self.fotoagenciado_set.order_by('id')):
        url = self.fotoagenciado_set.order_by('id')[:1][0].foto.url
      return "<img src='%s' height=100 />" % url
    thumbnail.allow_tags = True
    def telefonos(self):
      listadoTelefonos=[]
      for telefono in self.telefono_set.all():
        listadoTelefonos.append(telefono.telefono)
      return '<br />'.join(listadoTelefonos)
    telefonos.allow_tags = True
    def descripcion(self):
      return 'Edad %s, sexo %s, olhos %s, cabelo %s, pele %s, atura %s, peso %s, estado dentes %s.'%(str(self.edad()), dict(self.SEXO)[self.sexo],self.ojos,self.pelo,self.piel,self.altura,self.peso, self.estado_dientes)
    def edad(self):
      # @todo Definir como corresponde sin aproximar
      return (date.today()-self.fecha_nacimiento).days/365

class Rol(models.Model):
    descripcion = models.CharField(max_length=60, unique=True)
    def __unicode__(self):
      return self.descripcion

class TrabajoRealizadoAgenciado(models.Model):
    rol = models.ForeignKey(Rol)
    agenciado = models.ForeignKey(Agenciado)
    producto = models.CharField(max_length=100)
    fecha_trabajo = models.DateField()
    cache = models.DecimalField(max_digits=11, decimal_places=2)
    productora = models.CharField(max_length=100)
    fecha_pago = models.DateField()

class FotoAgenciado(models.Model):
    agenciado = models.ForeignKey(Agenciado)
    foto = models.ImageField(upload_to='agenciados/fotos/')
    def __unicode__(self):
      return self.foto.url

class VideoAgenciado(models.Model):
    agenciado = models.ForeignKey(Agenciado)
    url = models.URLField()
    def __unicode__(self):
      return self.url

class Compania(models.Model):
    descripcion = models.CharField(max_length=100, unique=True)
    def __unicode__(self):
      return self.descripcion

class ItemPortfolio(models.Model):
    titulo = models.CharField(max_length=100, unique=True)
    url = models.URLField()
    fecha = models.DateTimeField()
    def __unicode__(self):
      return self.titulo

class Trabajo(models.Model):
    titulo = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField()
    def __unicode__(self):
      return self.descripcion

class Telefono(models.Model):
    compania = models.ForeignKey(Compania, null=True, blank=True)
    agenciado = models.ForeignKey(Agenciado)
    telefono = models.CharField(max_length=60)
    def __unicode__(self):
      return self.telefono
    
class Postulacion(models.Model):
    agenciado = models.ForeignKey(Agenciado)
    trabajo = models.ForeignKey(Trabajo)
    ESTADO_POSTULACION=(
      ('PO', 'POSTULADO'),
    )
    estado = models.CharField(max_length=2,choices=ESTADO_POSTULACION)
    def __unicode__(self):
      return self.estado+'-'+self.trabajo+'-'+self.agenciado
