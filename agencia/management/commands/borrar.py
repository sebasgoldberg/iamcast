from django.core.management.base import BaseCommand, CommandError
from agencia.models import Ciudad, Danza, Deporte, Estado, EstadoDientes, Idioma, Instrumento, Ojos, Pelo, Piel, Talle, Agenciado, FotoAgenciado, VideoAgenciado, Compania, Telefono

class Command(BaseCommand):

  help=u'Borrar todos los datos de la aplicacion agencia'

  def borrarClaseSimple(self,clase):

    instanciasClase=clase.objects.all()

    for instanciaClase in instanciasClase:
      instanciaClase.delete()

    self.stdout.write('Los datos del modelo %s se han borrado correctamente\n'%clase)

  def handle(self,*args,**options):

    self.borrarClaseSimple(TrabajoRealizadoAgenciado)
    self.borrarClaseSimple(Postulacion)
    self.borrarClaseSimple(Trabajo)

    self.borrarClaseSimple(Agenciado)

    self.borrarClaseSimple(Ciudad)
    self.borrarClaseSimple(Danza)
    self.borrarClaseSimple(Deporte)
    self.borrarClaseSimple(Estado)
    self.borrarClaseSimple(EstadoDientes)
    self.borrarClaseSimple(Idioma)
    self.borrarClaseSimple(Instrumento)
    self.borrarClaseSimple(Ojos)
    self.borrarClaseSimple(Pelo)
    self.borrarClaseSimple(Piel)
    self.borrarClaseSimple(Talle)

    self.borrarClaseSimple(Rol)
    self.borrarClaseSimple(Compania)

    self.borrarClaseSimple(Telefono)
    self.borrarClaseSimple(FotoAgenciado)
    self.borrarClaseSimple(VideoAgenciado)

    self.borrarClaseSimple(ItemPortfolio)

