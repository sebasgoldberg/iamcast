from agencia.models import Ciudad, Danza, Deporte, Estado, EstadoDientes, Idioma, Instrumento, Ojos, Pelo, Piel, Talle, Agenciado, FotoAgenciado, VideoAgenciado, Compania, Telefono, validarTelefonoIngresado, validarFotoIngresada
from django.contrib import admin
from django.forms import CheckboxSelectMultiple
from django.db import models
from django.forms.models import BaseInlineFormSet

class TelefonoFormSet(BaseInlineFormSet):
  def clean(self):
    super(TelefonoFormSet,self).clean()
    validarTelefonoIngresado(self)

class FotoAgenciadoFormSet(BaseInlineFormSet):
  def clean(self):
    super(FotoAgenciadoFormSet,self).clean()
    validarFotoIngresada(self)

class TelefonoInline(admin.TabularInline):
  model=Telefono
  extra=1
  max_num=6
  formset=TelefonoFormSet

class FotoAgenciadoInline(admin.TabularInline):
  model=FotoAgenciado
  extra=1
  max_num=6
  formset=FotoAgenciadoFormSet

class VideoAgenciadoInline(admin.TabularInline):
  model=VideoAgenciado
  extra=1
  max_num=6

class AgenciadoAdmin(admin.ModelAdmin):
  readonly_fields=['id','thumbnails']
  fieldsets=[
    (None, {'fields':['thumbnails','id','mail']}),
    ('Datos personales', {'fields':[('nombre', 'apellido', 'fecha_nacimiento')]}),
    ('Datos Administrativos', { 'fields':[ ('documento_rg', 'documento_cpf'), 'responsable', 'cuenta_bancaria']}),
    ('Datos de direccion', { 'fields':[ ('estado', 'ciudad', 'barrio'), ('direccion', 'codigo_postal')]}),
    ('Caracteristicas fisicas', { 'fields':[ 'sexo', ('ojos', 'pelo', 'piel', 'estado_dientes'), ('altura', 'peso', 'talle', 'talle_camisa', 'talle_pantalon', 'calzado')]}),
    ('Habilidades', { 'fields':[ ('deportes', 'danzas'), ('instrumentos', 'idiomas'), ('indicador_maneja', 'indicador_tiene_registro')]}),
    ('Otros datos', { 'fields':[ 'trabaja_como_extra', 'como_nos_conocio', 'observaciones', 'activo', 'fecha_ingreso']}),
  ]
  inlines=[TelefonoInline, FotoAgenciadoInline, VideoAgenciadoInline]
  list_display=['thumbnail','id','apellido','nombre','fecha_nacimiento','descripcion','telefonos','mail', 'responsable']
  list_display_links = ('thumbnail', 'id')
  list_filter=['activo','sexo','ojos','pelo','piel','deportes','danzas','instrumentos','idiomas','fecha_ingreso']
  search_fields=['nombre','apellido','responsable','mail','id']
  date_hierarchy='fecha_nacimiento'
  filter_horizontal=['deportes','danzas','instrumentos','idiomas']
  list_per_page = 40
  actions_on_bottom = True

admin.site.register(Agenciado,AgenciadoAdmin)
admin.site.register(Ciudad)
admin.site.register(Danza)
admin.site.register(Deporte)
admin.site.register(Estado)
admin.site.register(EstadoDientes)
admin.site.register(Idioma)
admin.site.register(Instrumento)
admin.site.register(Ojos)
admin.site.register(Pelo)
admin.site.register(Piel)
admin.site.register(Talle)
admin.site.register(Compania)
