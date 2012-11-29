from agencia.models import Ciudad, Danza, Deporte, Estado, EstadoDientes, Idioma, Instrumento, Ojos, Pelo, Piel, Talle, Agenciado, Rol, TrabajoRealizadoAgenciado, FotoAgenciado, VideoAgenciado, Compania, ItemPortfolio, Trabajo, Telefono, Postulacion
from django.contrib import admin
from django.forms import CheckboxSelectMultiple
from django.db import models
from django.forms.models import BaseInlineFormSet
from django.core.exceptions import ValidationError

class TelefonoFormSet(BaseInlineFormSet):
  def clean(self):
    """Verifica que al menos se haya ingresado algun telefono"""
    if any(self.errors):
      return
    for form in self.forms:
      if not 'telefono' in form.cleaned_data:
        continue
      if form.cleaned_data['telefono'] != "" and not form.cleaned_data['DELETE']:
        return
    raise ValidationError('Tem que informar um telefone')

class FotoAgenciadoFormSet(BaseInlineFormSet):
  def clean(self):
    """Verifica que al menos se haya ingresado una foto"""
    if any(self.errors):
      return
    for form in self.forms:
      if not 'foto' in form.cleaned_data:
        continue
      if form.cleaned_data['foto'] != "" and not form.cleaned_data['DELETE']:
        return
    raise ValidationError('Tem que subir uma foto')

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
  fieldsets=[
    (None, {'fields':['mail']}),
    ('Datos personales', {'fields':[('nombre', 'apellido', 'fecha_nacimiento')]}),
    ('Datos Administrativos', { 'fields':[ ('documento_rg', 'documento_cpf'), 'responsable', 'cuenta_bancaria']}),
    ('Datos de direccion', { 'fields':[ ('estado', 'ciudad', 'barrio'), ('direccion', 'codigo_postal')]}),
    ('Datos de contacto', { 'fields':[ 'nextel']}),
    ('Caracteristicas fisicas', { 'fields':[ 'sexo', ('ojos', 'pelo', 'piel', 'estado_dientes'), ('altura', 'peso', 'talle', 'talle_camisa', 'talle_pantalon', 'calzado')]}),
    ('Habilidades', { 'fields':[ ('deportes', 'danzas'), ('instrumentos', 'idiomas'), ('indicador_maneja', 'indicador_tiene_registro')]}),
    ('Otros datos', { 'fields':[ 'trabaja_como_extra', 'como_nos_conocio', 'observaciones', 'activo', 'fecha_ingreso']}),
  ]
  inlines=[TelefonoInline, FotoAgenciadoInline, VideoAgenciadoInline]
  list_display=['thumbnail','id','apellido','nombre','fecha_nacimiento','descripcion','telefonos','mail', 'responsable']
  list_filter=['sexo','ojos','pelo','piel','fecha_ingreso']
  search_fields=['nombre','apellido','responsable','mail','id']
  date_hierarchy='fecha_nacimiento'
  filter_horizontal=['deportes','danzas','instrumentos','idiomas']

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
admin.site.register(Rol)

admin.site.register(TrabajoRealizadoAgenciado)

admin.site.register(Compania)
admin.site.register(ItemPortfolio)
admin.site.register(Trabajo)
admin.site.register(Postulacion)
