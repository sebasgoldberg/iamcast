# coding=utf-8
from django.core.management.base import BaseCommand, CommandError
from agencia.models import Ciudad, Danza, Deporte, Estado, EstadoDientes, Idioma, Instrumento, Ojos, Pelo, Piel, Talle, Agenciado, FotoAgenciado, VideoAgenciado, Compania, Telefono, validarTelefonoIngresado, validarFotoIngresada
import pymssql
from django.core.files.images import ImageFile
import re

class Command(BaseCommand):

  compania_nextel = Compania.objects.get(descripcion='Nextel')

  help=u'Migra los datos actuales en la base de datos de produccion de la aplicacion DELPHI a la base de datos de esta aplicacion'

  def migrarTablasSimples(self,cursor,tabla,clase):

    cursor.execute('SELECT * FROM '+tabla)

    for row in cursor:
      #self.stdout.write('%s\n'%row['descripcion'].decode('unicode-escape'))
      #self.stdout.write(row['descripcion']+'\n')
      instanciaClase=clase(descripcion=row['descripcion'].decode('unicode-escape'))
      instanciaClase.save()

    self.stdout.write('La tabla %s se a migrado correctamente al modelo %s\n'%(tabla,clase))


  def migrarTablaManyOneMany(self,tablaIntermedia,tablaDescripcion,claseModelo,relatedManager,recursoId):
    
    cursor=self.connection.cursor()

    cursor.execute(
      'select td.descripcion descripcion '+
      'from '+tablaIntermedia+' ti inner join '+tablaDescripcion+'s td '+
      'on ti.'+tablaDescripcion+'_id = td.id '+
      'where recurso_id = '+str(recursoId)
    )

    for row in cursor:
      instancia=claseModelo.objects.get(descripcion=row['descripcion'].decode('unicode-escape'))
      relatedManager.add(instancia)

  def addTelefono(self,agenciado,telefono, compania=None):
    
    if telefono == '':
      return

    agenciado.telefono_set.create( telefono = telefono, compania = compania )
    
  def migrarAgenciados(self,cursor):
    
# @todo Quitar restricción de cantidad
    query="\
      SELECT top 5 \
        ag.id, \
        nombre, \
        apellido, \
        fecha_nacimiento, \
        sexo, \
        pi.descripcion piel, \
        direccion, \
        codigo_postal, \
        barrio, \
        ci.descripcion ciudad, \
        es.descripcion estado, \
        telefono_particular, \
        tel_particular_alt_1, \
        tel_particular_alt_2, \
        telefono_movil, \
        telefono_movil_alternativo_1, \
        telefono_movil_alternativo_2, \
        nextel, \
        responsable, \
        documento_RG, \
        documento_CPF, \
        altura, \
        peso, \
        ta.descripcion talle, \
        pe.descripcion pelo, \
        oj.descripcion ojos, \
        calzado, \
        esdi.descripcion estado_dientes, \
        talle_pantalon, \
        talle_camisa, \
        mail, \
        cuenta_bancaria, \
        indicador_maneja, \
        indicador_tiene_registro, \
        fecha_ingreso, \
        trabaja_como_extra, \
        como_nos_conocio, \
        observaciones \
      FROM \
        recurso ag inner join piel pi \
        on ag.piel_id = pi.id \
        inner join ciudad ci \
        on ag.ciudad_id = ci.id \
        inner join estado es \
        on ag.estado_id = es.id \
        inner join talle ta \
        on ag.talle_id = ta.id \
        inner join pelo pe \
        on ag.pelo_id = pe.id \
        inner join ojos oj \
        on ag.ojos_id = oj.id \
        inner join estado_dientes esdi \
        on ag.estado_dientes_id = esdi.id"

    cursor.execute(query)

    idRecursos={}

    for row in cursor:
      #self.stdout.write(row['descripcion']+'\n')
      piel=Piel.objects.get(descripcion=row['piel'].decode('unicode-escape'))
      ciudad=Ciudad.objects.get(descripcion=row['ciudad'].decode('unicode-escape'))
      estado=Estado.objects.get(descripcion=row['estado'].decode('unicode-escape'))
      talle=Talle.objects.get(descripcion=row['talle'].decode('unicode-escape'))
      pelo=Pelo.objects.get(descripcion=row['pelo'].decode('unicode-escape'))
      ojos=Ojos.objects.get(descripcion=row['ojos'].decode('unicode-escape'))
      estadoDientes=EstadoDientes.objects.get(descripcion=row['estado_dientes'].decode('unicode-escape'))

      if row['mail'].decode('unicode-escape')=='':
        mail = None
      else:
        mail = row['mail'].decode('unicode-escape')

      repat=re.compile("^0*$")
      if repat.search(row['documento_CPF']) is None:
        documento_cpf = row['documento_CPF']
      else:
        documento_cpf = None

      agenciado=Agenciado(
        mail = mail,
        # Datos personales
        nombre = row['nombre'].decode('unicode-escape'),
        apellido = row['apellido'].decode('unicode-escape'),
        fecha_nacimiento = row['fecha_nacimiento'],
        # Datos Administrativos
        documento_rg = row['documento_RG'],
        documento_cpf = documento_cpf,
        responsable = row['responsable'].decode('unicode-escape'),
        cuenta_bancaria = row['cuenta_bancaria'],
        indicador_tiene_registro = row['indicador_tiene_registro'],
        # Datos de direccion
        estado = estado,
        ciudad = ciudad,
        barrio = row['barrio'].decode('unicode-escape'),
        direccion = row['direccion'].decode('unicode-escape'),
        codigo_postal = row['codigo_postal'],
        # Datos de contacto
        #nextel = row['nextel'],
        # Caracteristicas fisicas
        #SEXO=(
         # ('M', 'Masculino'),
         # ('F', 'Femenino'),
        #)
        sexo = row['sexo'],
        ojos = ojos,
        pelo = pelo,
        piel = piel,
        altura = row['altura'],
        peso = row['peso'],
        talle = talle,
        talle_camisa = row['talle_camisa'],
        talle_pantalon = row['talle_pantalon'],
        calzado = row['calzado'],
        estado_dientes = estadoDientes,
        # Habilidades
        #deportes = models.ManyToManyField(Deporte)
        #danzas = models.ManyToManyField(Danza)
        #instrumentos = models.ManyToManyField(Instrumento)
        #idiomas = models.ManyToManyField(Idioma)
        indicador_maneja = row['indicador_maneja'],
        # Otros datos
        trabaja_como_extra = row['trabaja_como_extra'],
        como_nos_conocio = row['como_nos_conocio'].decode('unicode-escape'),
        observaciones = row['observaciones'].decode('unicode-escape'),
        activo = True,
        fecha_ingreso = row['fecha_ingreso'],
        recurso_id = row['id']
        )

      agenciado.save()
      
      idRecursos[agenciado.id]=row['id']
    
      self.addTelefono(agenciado,row['nextel'],self.compania_nextel)
      self.addTelefono(agenciado,row['telefono_particular'])
      self.addTelefono(agenciado,row['tel_particular_alt_1'])
      self.addTelefono(agenciado,row['tel_particular_alt_2'])
      self.addTelefono(agenciado,row['telefono_movil'])
      self.addTelefono(agenciado,row['telefono_movil_alternativo_1'])
      self.addTelefono(agenciado,row['telefono_movil_alternativo_2'])

    for idAgenciado, idRecurso in idRecursos.iteritems():

      agenciado=Agenciado.objects.get(id=idAgenciado)

      self.migrarTablaManyOneMany('Deporte_Recurso','Deporte',Deporte,agenciado.deportes,idRecurso)
      self.migrarTablaManyOneMany('Danza_Recurso','Danza',Danza,agenciado.danzas,idRecurso)
      self.migrarTablaManyOneMany('Instrumento_Recurso','Instrumento',Instrumento,agenciado.instrumentos,idRecurso)
      self.migrarTablaManyOneMany('Idioma_Recurso','Idioma',Idioma,agenciado.idiomas,idRecurso)

      self.stdout.write('Se migro correctamente el recurso %s en el agenciado %s\n'%(str(idRecurso),idAgenciado))

    self.stdout.write('La tabla %s se a migrado correctamente al modelo %s\n'%('recurso',Agenciado))


  def handle(self,*args,**options):

    self.connection = pymssql.connect(host='25.92.66.172', user='aretha', password='aretha01', database='alternativa', as_dict=True)
    cursor = self.connection.cursor()

    self.migrarTablasSimples(cursor,'Ciudad',Ciudad)
    self.migrarTablasSimples(cursor,'Danzas',Danza)
    self.migrarTablasSimples(cursor,'Deportes',Deporte)
    self.migrarTablasSimples(cursor,'Estado',Estado)
    self.migrarTablasSimples(cursor,'Estado_Dientes',EstadoDientes)
    self.migrarTablasSimples(cursor,'Idiomas',Idioma)
    self.migrarTablasSimples(cursor,'Instrumentos',Instrumento)
    self.migrarTablasSimples(cursor,'Ojos',Ojos)
    self.migrarTablasSimples(cursor,'Pelo',Pelo)
    self.migrarTablasSimples(cursor,'Piel',Piel)
    self.migrarTablasSimples(cursor,'Talle',Talle)

    self.migrarAgenciados(cursor)

    self.connection.close()

