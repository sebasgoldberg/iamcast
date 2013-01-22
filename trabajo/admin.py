# coding=utf-8
from trabajo.models import Rol, ItemPortfolio, Trabajo, Postulacion
from django.contrib import admin
from django.forms import CheckboxSelectMultiple
from django.db import models
from django.forms.models import BaseInlineFormSet
from django.http import HttpResponseRedirect
from agencia.admin import AgenciadoAdmin


def add_agenciados_trabajo(modeladmin, request, queryset):
  selected = request.POST.getlist(admin.ACTION_CHECKBOX_NAME)
  #ct = ContentType.objects.get_for_model(queryset.model)
  return HttpResponseRedirect("/trabajo/seleccionar/y/agregar/agenciados/?ids=%s" %  ",".join(selected))

add_agenciados_trabajo.short_description='Adicionar agenciados selecionados a trabalho'

# IMPORTANTE: El agregado de la accion se hace de la siguiente forma porque si solo se hiciese con '+=' y el listado estuviese vacío, entonces la acción se registraría para todos los modelos. Este imagino que debe ser un bug de django. Con append ocurre el mismo error.
if len(AgenciadoAdmin.actions)==0:
  AgenciadoAdmin.actions=[add_agenciados_trabajo]
else:
  AgenciadoAdmin.actions+=[add_agenciados_trabajo]

admin.site.register(Rol)
admin.site.register(ItemPortfolio)
admin.site.register(Trabajo)
admin.site.register(Postulacion)
