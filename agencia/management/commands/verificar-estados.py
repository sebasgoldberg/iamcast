from django.core.management.base import BaseCommand, CommandError
from agencia.models import Estado
from cities_light.models import Region
from django.conf import settings

class Command(BaseCommand):

  help=u'Verifica si los estados del modelo agencia.models.Estado existen en los estados del modelo cities_light.models.Region'

  def handle(self,*args,**options):

    self.stdout.write('Estados no encontrados:\n')
    cantidad_estados_no_encontrados=0

    for estado in Estado.objects.all():
      if not Region.objects.filter(country__code2='BR',name=estado.descripcion):
        self.stdout.write(u'%s\n'%estado.descripcion)
        cantidad_estados_no_encontrados+=1
        
    self.stdout.write('No se han encontrado %s estados.\n'%cantidad_estados_no_encontrados)
