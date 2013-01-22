# coding=utf-8
# Create your views here.

from django.shortcuts import render_to_response, render, redirect
from django.contrib.auth.decorators import login_required
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import permission_required
from django import forms
from trabajo.models import Postulacion
from agencia.models import Agenciado

class SeleccionarYAgregarAgenciadosForm(ModelForm):
  ids = forms.CharField(widget = forms.HiddenInput(), required = True)
  class Meta:
    model = Postulacion
    fields = ('rol', 'estado')

# Verifica que tenga permisos el usuario para agregar agenciados a un trabajo
@permission_required('trabajo.add_postulacion',raise_exception=True)
def seleccionar_y_agregar_agenciados(request):

  # Se obtienen los agenciados asociados a los IDs
  if request.method == 'GET':
    ids = request.GET['ids']
  else:
    ids = request.POST['ids']
  listado_ids=[int(x) for x in ids.split(",")]
  agenciados=Agenciado.objects.filter(id__in=listado_ids)

  # Se crea el formulario con el campo trabajo y el campo estado en funcion del modelo Postulación
  # En caso de ser un metodo POST:
  if request.method == 'POST':
    form = SeleccionarYAgregarAgenciadosForm(request.Post)
    # Se valida el formulario
    if form.is_valid():
      # Se obtienen el trabajo y el estado seleccionados
      trabajo_id = form.cleaned_data['trabajo']
      estado_id = form.cleaned_data['estado']
      agenciados_ya_postulados=[]
      agenciados_postulados_con_exito=[]
      # Por cada agenciado:
      for agenciado in agenciados:
        try:
          # Si el agenciado ya se encuentra asignado al trabajo, se guarda en el listado de agenciados ya asignados
          Postulacion.objects.get(agenciado=agenciado.id,trabajo=trabajo_id)
          agenciados_ya_postulados+=[agenciado]
          continue
        except Postulacion.DoesNotExist:
          # Sino, se asigna el agenciado al trabajo como una Postulacion con el estado seleccionado en el formulario y se guarda el agenciado en el listado de agenciados asignado con éxito
          postulacion=Postulacion(agenciado=agenciado, trabajo=trabajo_id, estado=estado_id)
          postulacion.save()
          agenciados_postulados_con_exito+=[agenciado]

      # Se muestran los resultados de la operación
      return redirect('/admin/trabajo/trabajo/%s/' % trabajo.id)

  # Sino
  else:
    form = SeleccionarYAgregarAgenciadosForm()
    form.ids = ids
    # Se muestra el formulario, y debajo del mismo los agenciados a ser asignados.
    pass
      #@todo Indicar cambio de password satisfactorio

  return render(request,'trabajo/seleccionar_y_agregar_agenciados.html',{'form':form, 'agenciados':agenciados})

