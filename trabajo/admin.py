# coding=utf-8
from trabajo.models import Productora, Rol, ItemPortfolio, Trabajo, Postulacion, DireccionProductora, TelefonoProductora, EventoTrabajo, EventoRol
from django.contrib import admin
from django.forms import CheckboxSelectMultiple
from django.db import models
from django.forms.models import BaseInlineFormSet
from django.http import HttpResponseRedirect
from agencia.admin import AgenciadoAdmin
from django.forms.widgets import Textarea

class PostulacionInline(admin.TabularInline):
  model=Postulacion
  extra=1
  readonly_fields=['thumbnail_agenciado_link', 'agenciado_admin_link']
  fields=['thumbnail_agenciado_link', 'agenciado_admin_link', 'agenciado', 'estado']

class AgenciadoPostulacionInline(admin.TabularInline):
  model=Postulacion
  extra=1
  readonly_fields=['rol_admin_link']
  fields=['rol_admin_link', 'rol', 'estado']

class DireccionProductoraInline(admin.TabularInline):
  model=DireccionProductora
  extra = 1

class TelefonoProductoraInline(admin.TabularInline):
  model=TelefonoProductora
  extra = 1

class EventoInline(admin.TabularInline):
  extra = 0
  fields = ['tipo', 'descripcion', 'fecha', 'estado', 'ciudad', 'barrio', 'direccion']
  
class EventoTrabajoInline(EventoInline):
  model=EventoTrabajo

class EventoRolInline(EventoInline):
  model=EventoRol

class TrabajoInline(admin.TabularInline):
  model = Trabajo
  extra = 1
  readonly_fields = [ 'admin_link' ]
  fields = ['admin_link', 'titulo', 'estado', 'fecha_ingreso', 'descripcion', 'imagen']
  formfield_overrides = {
    models.TextField: {'widget': Textarea(attrs={'rows':4})},
  }

class ProductoraAdmin(admin.ModelAdmin):
  inlines = [DireccionProductoraInline, TelefonoProductoraInline, TrabajoInline]

class RolAdmin(admin.ModelAdmin):
  readonly_fields=[
    'id', 'cantidad_postulados_casting', 'cantidad_seleccionados_casting',
    'cantidad_seleccionados_trabajo', 'cantidad_trabajos_realizados',
    'cantidad_trabajos_pagados', 'trabajo_admin_link',
  ]
  inlines=[EventoRolInline, PostulacionInline]
  fieldsets=[
    (None, {'fields':['id']}),
    ('Dados do rol procurado', 
      {'fields':[('descripcion', 'trabajo', 'trabajo_admin_link' ), 'cache', ('caracteristicas',)]}),
    ('Dados das postulaçoes', 
      { 'fields':[ 
        ('cantidad_postulados_casting', 'cantidad_seleccionados_casting', 
        'cantidad_seleccionados_trabajo', 'cantidad_trabajos_realizados', 
        'cantidad_trabajos_pagados')]}),
  ]
  list_display=[
    'id', 'descripcion', 'trabajo', 'cache', 'cantidad_postulados_casting', 
    'cantidad_seleccionados_casting', 'cantidad_seleccionados_trabajo', 
    'cantidad_trabajos_realizados', 'cantidad_trabajos_pagados', 'caracteristicas',
  ]
  list_display_links = ['id']
  list_filter=['trabajo__estado', 'trabajo']
  search_fields=['trabajo__titulo', 'descripcion', 'id']

class RolInline(admin.TabularInline):
  model=Rol
  extra=1
  readonly_fields=['admin_link']
  fields=['admin_link', 'descripcion', 'cache','caracteristicas']
  formfield_overrides = {
    models.TextField: {'widget': Textarea(attrs={'rows':4})},
  }

class TrabajoAdmin(admin.ModelAdmin):
  readonly_fields=['id','thumbnail_img_link', 'productora_admin_link']
  inlines=[EventoTrabajoInline,RolInline]
  list_display=['thumbnail_img','id','titulo', 'estado', 'descripcion', 
    'fecha_ingreso', 'roles']
  list_display_links = ('thumbnail_img', 'id')
  list_filter=['estado']
  search_fields=['titulo','id']
  date_hierarchy='fecha_ingreso'
  fieldsets=[
    (None, {'fields':['id', 'thumbnail_img_link']}),
    ('Dados do trabalho', 
      {'fields':['titulo', ('productora', 'productora_admin_link'), 'estado', 'fecha_ingreso', 'descripcion', 'imagen']}),
  ]

class PostulacionAdmin(admin.ModelAdmin):
  readonly_fields=['id']
  list_display=['id', 'trabajo_rol', 'rol', 'thumbnail_agenciado_link', 'agenciado', 'estado']
  list_display_links = ('id',)
  list_filter=['rol', 'estado']
  search_fields=['trabajo__titulo', 'rol__descripcion', 'agenciado__nombre', 'agenciado__apellido', 'id']
  list_editable=['estado']

def add_agenciados_trabajo(modeladmin, request, queryset):
  selected = request.POST.getlist(admin.ACTION_CHECKBOX_NAME)
  return HttpResponseRedirect("/trabajo/seleccionar/y/agregar/agenciados/?ids=%s" %  ",".join(selected))

add_agenciados_trabajo.short_description='Adicionar agenciados selecionados a trabalho'

# IMPORTANTE: El agregado de la accion se hace de la siguiente forma porque si solo se hiciese con '+=' y el listado estuviese vacío, entonces la acción se registraría para todos los modelos. Este imagino que debe ser un bug de django. Con append ocurre el mismo error.
if len(AgenciadoAdmin.actions)==0:
  AgenciadoAdmin.actions=[add_agenciados_trabajo]
else:
  AgenciadoAdmin.actions+=[add_agenciados_trabajo]

AgenciadoAdmin.inlines+=[AgenciadoPostulacionInline]

admin.site.register(Productora,ProductoraAdmin)
admin.site.register(Rol,RolAdmin)
admin.site.register(ItemPortfolio)
admin.site.register(Trabajo,TrabajoAdmin)
#admin.site.register(Postulacion,PostulacionAdmin)
