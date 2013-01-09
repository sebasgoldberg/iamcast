from django.core.management.base import BaseCommand, CommandError
from agencia.models import Ciudad, Danza, Deporte, Estado, EstadoDientes, Idioma, Instrumento, Ojos, Pelo, Piel, Talle, Agenciado, Rol, TrabajoRealizadoAgenciado, FotoAgenciado, VideoAgenciado, Compania, ItemPortfolio, Trabajo, Telefono, Postulacion
import pymssql
from django.core.files.images import ImageFile

class Command(BaseCommand):

  help=u'Migra las fotos en una ruta determinada de los recursos DELPHI a los agenciados'

  # Migra cada foto para el agenciado pasado
  # @pre La foto del agenciado se encuentra en carpeta self.origenFotos, con el siguiente nombre:
  #   <imagen_recurso.id>.jpg
  # De forma que el path absoluto sera 
  #   self.origenFotos/<imagen_recurso.id>.jpg
  # El contenido de la foto sera la correspondiente al campo imagen_recurso.imagen para el
  # id encontrado en el nombre.
  # @pre el agenciado pasado contendra el campo recurso_id y se correspondera con el de la
  # aplicacion DELPHI
  def migrarFotos(self,agenciado):
    
    if not agenciado.recurso_id:
      return

    cursor=self.connection.cursor()

    cursor.execute(
      'select id, imagen '+
      'from imagen_recurso '+
      'where recurso_id = '+str(agenciado.recurso_id)
    )

    for row in cursor:

      #filename='/home/cerebro/django-projects/alternativa/uploads/agenciados/fotos/'+str(row['id'])

      f=open(self.origenFotos+'/'+str(row['id'])+'.jpg','rb')
      imageFile=ImageFile(f)

      fa=agenciado.fotoagenciado_set.create( )
      fa.foto.save(str(row['id'])+'.jpg',imageFile,save=True)

      self.stdout.write('Foto agregada al agenciado %s\n'%agenciado)
      f.close()
    

  def handle(self,*args,**options):

    self.connection = pymssql.connect(host='25.92.66.172', user='aretha', password='aretha01', database='alternativa', as_dict=True)

    cursor = self.connection.cursor()

    self.origenFotos='/mnt/hgfs/vm-compartido/fotos-recursos'

    self.migrarFotos(Agenciado.objects.get(recurso_id=17))
    self.migrarFotos(Agenciado.objects.get(recurso_id=18))

    self.connection.close()

