# Create your views here.

from django.shortcuts import render_to_response, render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group
from django.contrib.auth import authenticate, login
from django.forms import ModelForm
from django.forms.widgets import CheckboxSelectMultiple
from django.forms.extras.widgets import SelectDateWidget
from agencia.models import Agenciado, Telefono
from datetime import date
from django.forms.models import inlineformset_factory

def index(request):
  return render(request,'agencia/index.html')

class AgenciadoForm(ModelForm):
  class Meta:
    model = Agenciado
    exclude = ('activo', 'fecha_ingreso')
    widgets = {
      'fecha_nacimiento': SelectDateWidget,
      'deportes': CheckboxSelectMultiple,
      'danzas': CheckboxSelectMultiple,
      'instrumentos': CheckboxSelectMultiple,
      'idiomas': CheckboxSelectMultiple,
      }

@login_required
def agenciado(request):

  TelefonoFormSet = inlineformset_factory(Agenciado, Telefono, extra=1)

  try:
    agenciado=Agenciado.objects.get(user__id=request.user.id)
  except Agenciado.DoesNotExist:
    agenciado=Agenciado()
    agenciado.user=request.user
    agenciado.fecha_ingreso = date.today()

  if request.method == 'POST':
    form = AgenciadoForm(request.POST,instance=agenciado)
    telefonoFormSet=TelefonoFormSet(request.POST,instance=agenciado)
    if form.is_valid() and telefonoFormSet.is_valid():
      form.save()
      telefonoFormSet.save()
      redirect('/agencia/agenciado/')
  else:
    form = AgenciadoForm(instance=agenciado)
    telefonoFormSet=TelefonoFormSet(instance=agenciado)
  return render(request,'agencia/agenciado.html',{'form':form, 'telefonoFormSet':telefonoFormSet})

def logout_view(request):
  logout(request)
  return redirect('/agencia/')

def registro(request):
  if request.method == 'POST':
    form = UserCreationForm(request.POST)
    if form.is_valid():
      user = form.save()
      grupo=Group.objects.get(name='agenciado')
      user = authenticate(username=request.POST['username'], password=request.POST['password1'])
      login(request,user)
      return redirect('/agencia/agenciado/')
  else:
    form = UserCreationForm()

  return render(request,'agencia/registro.html',{'form':form})
