from trabajo.models import Rol, ItemPortfolio, Trabajo, Postulacion
from django.contrib import admin
from django.forms import CheckboxSelectMultiple
from django.db import models
from django.forms.models import BaseInlineFormSet

admin.site.register(Rol)
admin.site.register(ItemPortfolio)
admin.site.register(Trabajo)
admin.site.register(Postulacion)
