# coding=utf-8
# Create your views here.

from django.shortcuts import render_to_response, render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.decorators import permission_required
from django import forms
from trabajo.models import Postulacion, Rol, Trabajo
from agencia.models import Agenciado
from django.template import loader, Context
from agencia.mail import AgenciaMail
from django.conf import settings
from django.contrib import messages

class SeleccionarYAgregarAgenciadosForm(forms.ModelForm):
  ids = forms.CharField(widget = forms.HiddenInput(), required = True)
  class Meta:
    model = Postulacion
    fields = ('rol', 'estado')

# Verifica que tenga permisos el usuario para agregar agenciados a un trabajo
@permission_required('trabajo.add_postulacion',raise_exception=True)
def agregar_agenciados_seleccionados_a_rol(request):

  # Se obtienen los agenciados asociados a los IDs
  if request.method == 'GET':
    ids = request.GET['ids']
  else:
    ids = request.POST['ids']
  listado_ids=ids.split(',')
  agenciados=Agenciado.objects.filter(id__in=listado_ids)

  # Se crea el formulario con el campo trabajo y el campo estado en funcion del modelo Postulación
  # En caso de ser un metodo POST:
  if request.method == 'POST':
    form = SeleccionarYAgregarAgenciadosForm(request.POST)
    # Se valida el formulario
    if form.is_valid():
      # Se obtienen el trabajo y el estado seleccionados
      rol = form.cleaned_data['rol']
      estado_id = form.cleaned_data['estado']
      postulaciones_ya_existentes=[]
      postulaciones_realizadas_con_exito=[]
      # Por cada agenciado:
      for agenciado in agenciados:
        try:
          # Si el agenciado ya se encuentra asignado al trabajo, se guarda en el listado de agenciados ya asignados
          postulacion = Postulacion.objects.get(agenciado=agenciado.id,rol=rol.id)
          postulaciones_ya_existentes+=[postulacion]
          continue
        except Postulacion.DoesNotExist:
          # Sino, se asigna el agenciado al trabajo como una Postulacion con el estado seleccionado en el formulario y se guarda el agenciado en el listado de agenciados asignado con éxito
          postulacion=Postulacion(agenciado=agenciado, rol=rol, estado=estado_id)
          postulacion.save()
          postulaciones_realizadas_con_exito+=[postulacion]

      # Se obtienen los IDs de las postulacion como un string de ids separadas por comas.
      ids_exito = str([ int(str(postulacion.id)) for postulacion in postulaciones_realizadas_con_exito ])[1:-1]
      ids_existentes = str([ int(str(postulacion.id)) for postulacion in postulaciones_ya_existentes ])[1:-1]

      # Se muestran los resultados de la operación
      return redirect('/trabajo/resultados/agregar/agenciados/seleccionados/a/rol/%s/%s/?ids_exito=%s&ids_existentes=%s' % (
        rol.id,
        estado_id,
        ids_exito, 
        ids_existentes,))

  # Sino
  else:
    form = SeleccionarYAgregarAgenciadosForm(initial={'ids': ids})

  return render(request,'trabajo/rol/agregar_agenciados_seleccionados.html',{'form':form, 'agenciados':agenciados})

@permission_required('trabajo.add_postulacion',raise_exception=True)
def resultados_agregar_agenciados_seleccionados_a_rol(request,id_rol,id_estado):

  ids_exito = request.GET['ids_exito'].strip()
  if ids_exito:
    listado_ids_exito = [ int(x) for x in ids_exito.split(',') ]
  else:
    listado_ids_exito = []

  ids_existentes = request.GET['ids_existentes'].strip()
  if ids_existentes:
    listado_ids_existentes = [ int(x) for x in ids_existentes.split(',') ]
  else:
    listado_ids_existentes = []

  postulaciones_realizadas_con_exito=Postulacion.objects.filter(id__in=listado_ids_exito)
  postulaciones_ya_existentes=Postulacion.objects.filter(id__in=listado_ids_existentes)
  rol = Rol.objects.get(pk=id_rol)

  return render(request,'trabajo/rol/resultados_agregar_agenciados_seleccionados.html',
    {'postulaciones_realizadas_con_exito': postulaciones_realizadas_con_exito, 
    'postulaciones_ya_existentes': postulaciones_ya_existentes, 
    'rol': rol, 
    'estado': Postulacion.DICT_ESTADO_POSTULACION[id_estado] })


class MailForm(forms.Form):
  # @todo Agregar múltiples destinatarios.
  destinatario=forms.EmailField()
  asunto=forms.CharField()

@permission_required('trabajo.mail_productora',raise_exception=True)
def trabajo_enviar_mail_productora(request,trabajo_id):
  
  trabajo=Trabajo.objects.get(pk=trabajo_id)

  if request.method == 'POST':
    form = MailForm(request.POST)
    if form.is_valid():
      template = loader.get_template('trabajo/trabajo/cuerpo_mail_productora.html')
      context = Context({'trabajo':trabajo})
      asunto = form.cleaned_data['asunto']
      destinatario = form.cleaned_data['destinatario']

      text_content = 'Este mensagem deve ser visualizado em formato HTML.'
      html_content = template.render(context)
      msg = AgenciaMail(asunto, text_content, [destinatario])
      msg.set_html_body(html_content)
      msg.send()
      messages.success(request, 'Trabalho enviado com sucesso a %s'%destinatario)
      return redirect('/admin/trabajo/trabajo/%s/'%trabajo_id)
  else:
    asunto = 'Agencia %s - Detalhe de trabalho "%s"' % (settings.AMBIENTE.agencia.nombre, trabajo.titulo)
    form = MailForm(initial={'destinatario':trabajo.productora.mail, 'asunto': asunto })

  return render(request,'trabajo/trabajo/enviar_mail_productora.html',{'form': form, 'trabajo': trabajo})
