from django.core.management.base import BaseCommand, CommandError
from agencia.models import Ciudad
from cities_light.models import City
from django.conf import settings

class Command(BaseCommand):

  help=u'Verifica si las ciudades del modelo agencia.models.Ciudad existen en las ciudades del modelo cities_light.models.City'

  def handle(self,*args,**options):

    self.stdout.write('Ciudades no encontradas:\n')
    cantidad_ciudades_no_encontradas=0

    for ciudad in Ciudad.objects.all():
      if not City.objects.filter(region__country__code2='BR',name=ciudad.descripcion):
        self.stdout.write(u'%s\n'%ciudad.descripcion)
        cantidad_ciudades_no_encontradas+=1
        
    self.stdout.write('No se han encontrado %s ciudades.\n'%cantidad_ciudades_no_encontradas)
