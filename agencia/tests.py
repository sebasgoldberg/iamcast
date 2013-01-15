# coding=utf-8
"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""
from agencia.models import Ciudad, Danza, Deporte, Estado, EstadoDientes, Idioma, Instrumento, Ojos, Pelo, Piel, Talle, Agenciado, FotoAgenciado, VideoAgenciado, Compania, Telefono
from django.test import TestCase
from datetime import date
from datetime import timedelta
from django.db import IntegrityError
from django.core.exceptions import ValidationError

class AgenciaTestCase(TestCase):

  fixtures = ['test-data.yaml']

  def get_agenciado_default(self):
    """
    Obtiene un agenciado con datos por default.
    El agenciado devuelto no contendrá los siguientes datos:
    mail, rg, cpf
    Verifica que al crear un agenciado se cree el correspondiente usuario
    y que los datos del usuario y el agenciado se correspondan.
    """
    agenciado=Agenciado()
    agenciado.mail = u'test100@test.com'
    ## Datos personales
    agenciado.nombre = u'Test'
    agenciado.apellido = u'Test'
    agenciado.fecha_nacimiento = date(1982,12,20)
    ## Datos Administrativos
    agenciado.documento_rg = u'123100'
    agenciado.documento_cpf = u'123100'
    agenciado.responsable = u'Responsable de Test'
    #cuenta_bancaria: 
    ## Datos de direccion
    agenciado.estado = Estado.objects.get()
    agenciado.ciudad = Ciudad.objects.get()
    agenciado.barrio = u'Barrio de Test'
    agenciado.direccion = u'Direccion de Test'
    agenciado.codigo_postal = u'1234'
    ## Datos de contacto
    #nextel: 
    ## Caracteristicas fisicas
    agenciado.sexo = u'M'
    agenciado.ojos = Ojos.objects.get() 
    agenciado.pelo = Pelo.objects.get() 
    agenciado.piel = Piel.objects.get() 
    agenciado.altura = 1.81
    agenciado.peso = 82
    agenciado.talle = Talle.objects.get() 
    agenciado.talle_camisa = u'38'
    agenciado.talle_pantalon = u'36'
    agenciado.calzado = u'44'
    agenciado.estado_dientes = EstadoDientes.objects.get() 
    ## Habilidades
    #deportes:
    #danzas: 
    #instrumentos: 
    #idiomas: 
    agenciado.indicador_maneja = True
    agenciado.indicador_tiene_registro = False
    ## Otros datos
    agenciado.trabaja_como_extra = False
    agenciado.como_nos_conocio = u'Por Internet'
    #observaciones: 
    ## Datos administrativos del sistema 
    agenciado.activo = True
    agenciado.fecha_ingreso = date(2013,01,14)
    #recurso_id: 

    return agenciado

  def test_creacion_usuario_al_crear_agenciado(self):
    """
    Verifica que al crear un agenciado se cree el correspondiente usuario
    y que los datos del usuario y el agenciado se correspondan.
    """
    agenciado = self.get_agenciado_default()
    #agenciado.mail = u'test@test.com'
    #agenciado.documento_rg = u'123'
    #agenciado.documento_cpf = u'123'

    agenciado.save()

    agenciado=Agenciado.objects.get(mail='test@test.com')

    self.assertIsNotNone(agenciado.user)
    self.assertEqual(agenciado.mail,agenciado.user.email)
    self.assertEqual(agenciado.nombre,agenciado.user.first_name)
    self.assertEqual(agenciado.apellido,agenciado.user.last_name)

  def test_modificacion_usuario_al_modificar_agenciado(self):
    """
    Verifica que al crear un agenciado se cree el correspondiente usuario
    y que los datos del usuario y el agenciado se correspondan.
    """
    agenciado = self.get_agenciado_default()
    agenciado.mail = u'test110@test.com'
    agenciado.documento_rg = u'123110'
    agenciado.documento_cpf = u'123110'

    agenciado.save()

    agenciado=Agenciado.objects.get(mail='test110@test.com')
    agenciado.mail = u'test111@test.com'
    agenciado.documento_rg = u'123111'
    agenciado.documento_cpf = u'123110'
    agenciado.save()

    agenciado=Agenciado.objects.get(mail='test111@test.com')

    self.assertEqual(agenciado.mail,agenciado.user.email)
    self.assertEqual(agenciado.nombre,agenciado.user.first_name)
    self.assertEqual(agenciado.apellido,agenciado.user.last_name)

  def test_unicidad(self):
    """
    Verifica que se respete la unicidad de los campos mail, RG y CPF del 
    agenciado.
    """
    agenciado = self.get_agenciado_default()
    agenciado.mail = u'test101@test.com'
    agenciado.documento_rg = u'123101'
    agenciado.documento_cpf = u'123101'
    agenciado.save()

    agenciado = self.get_agenciado_default()
    agenciado.mail = u'test101@test.com'
    agenciado.documento_rg = u'123102'
    agenciado.documento_cpf = u'123102'
    self.assertRaises(IntegrityError,agenciado.save) 

    agenciado = self.get_agenciado_default()
    agenciado.mail = u'test102@test.com'
    agenciado.documento_rg = u'123101'
    agenciado.documento_cpf = u'123102'
    self.assertRaises(IntegrityError,agenciado.save) 

    agenciado = self.get_agenciado_default()
    agenciado.mail = u'test102@test.com'
    agenciado.documento_rg = u'123102'
    agenciado.documento_cpf = u'123101'
    self.assertRaises(IntegrityError,agenciado.save) 

    agenciado = self.get_agenciado_default()
    agenciado.mail = u'test102@test.com'
    agenciado.documento_rg = u'123102'
    agenciado.documento_cpf = u'123102'
    agenciado.save()

  def test_fecha_nacimiento_menor_fecha_dia(self):
    # @todo redefinir test utilizando formularios ya que los validadores no corren a nivel del modelo
    return
    agenciado = self.get_agenciado_default()
    agenciado.mail = u'test120@test.com'
    agenciado.documento_rg = u'123120'
    agenciado.documento_cpf = u'123120'
    agenciado.fecha_nacimiento = date.today() + timedelta(days=1)
    self.assertRaises(ValidationError,agenciado.save) 
