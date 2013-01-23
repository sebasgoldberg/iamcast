# coding=utf-8
from trabajo.models import Productora, Rol, ItemPortfolio, Trabajo, Postulacion
from django.contrib import admin
from django.forms import CheckboxSelectMultiple
from django.db import models
from django.forms.models import BaseInlineFormSet
from django.http import HttpResponseRedirect
from agencia.admin import AgenciadoAdmin

class PostulacionInline(admin.TabularInline):
  model=Postulacion
  extra=1
  readonly_fields=['thumbnail_agenciado_link']
  fields=['thumbnail_agenciado_link', 'agenciado', 'estado']

class RolAdmin(admin.ModelAdmin):
  readonly_fields=[
    'id', 'cantidad_postulados_casting', 'cantidad_seleccionados_casting',
    'cantidad_seleccionados_trabajo', 'cantidad_trabajos_realizados',
    'cantidad_trabajos_pagados', 'trabajo_admin_link',
  ]
  inlines=[PostulacionInline]
  fieldsets=[
    (None, {'fields':['id']}),
    ('Dados do rol procurado', 
      {'fields':[('descripcion', 'trabajo', 'trabajo_admin_link' ), ('caracteristicas',)]}),
    ('Dados das postulaçoes', 
      { 'fields':[ 
        ('cantidad_postulados_casting', 'cantidad_seleccionados_casting', 
        'cantidad_seleccionados_trabajo', 'cantidad_trabajos_realizados', 
        'cantidad_trabajos_pagados')]}),
  ]
  list_display=[
    'id', 'descripcion', 'trabajo', 'cantidad_postulados_casting', 
    'cantidad_seleccionados_casting', 'cantidad_seleccionados_trabajo', 
    'cantidad_trabajos_realizados', 'cantidad_trabajos_pagados', 'caracteristicas',
  ]
  list_display_links = ['id']
  list_filter=['trabajo__estado', 'trabajo']
  search_fields=['trabajo__titulo', 'descripcion', 'id']

class RolInline(admin.TabularInline):
  model=Rol
  extra=1
  readonly_fields=['rol_admin_link']
  fields=['rol_admin_link', 'descripcion', 'caracteristicas']

class TrabajoAdmin(admin.ModelAdmin):
  readonly_fields=['id','thumbnail_img_link']
  inlines=[RolInline]
  list_display=['thumbnail_img','id','titulo', 'estado', 'descripcion', 
    'fecha_ingreso', 'roles']
  list_display_links = ('thumbnail_img', 'id')
  list_filter=['estado']
  search_fields=['titulo','id']
  date_hierarchy='fecha_ingreso'
  fieldsets=[
    (None, {'fields':['id', 'thumbnail_img_link']}),
    ('Dados do trabalho', 
      {'fields':['titulo', 'productora', 'estado', 'fecha_ingreso', 'descripcion', 'imagen']}),
    ('Dados do test', 
      { 'fields':[ 
        ('fecha_test', 'estado_test', 'ciudad_test', 
        'barrio_test', 'direccion_test' )]}),
    ('Dados do trabalho', 
      { 'fields':[ 
        ('fecha_trabajo', 'estado_trabajo', 'ciudad_trabajo', 
        'barrio_trabajo', 'direccion_trabajo' )]}),
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

admin.site.register(Productora)
admin.site.register(Rol,RolAdmin)
admin.site.register(ItemPortfolio)
admin.site.register(Trabajo,TrabajoAdmin)
#admin.site.register(Postulacion,PostulacionAdmin)
