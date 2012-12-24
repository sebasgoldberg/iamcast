# Create your views here.

from django.shortcuts import render_to_response, render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth.forms import UserCreationForm, SetPasswordForm, PasswordResetForm
from django.contrib.auth.models import Group
from django.contrib.auth import authenticate, login
from django.forms import ModelForm
from django.forms.widgets import CheckboxSelectMultiple
from django.forms.extras.widgets import SelectDateWidget
from agencia.models import Agenciado, Telefono, FotoAgenciado, VideoAgenciado, validarTelefonoIngresado, validarFotoIngresada
from datetime import date
from django.forms.models import inlineformset_factory
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

def index(request):
  return render(request,'agencia/index.html')

class AgenciadoForm(ModelForm):
  class Meta:
    model = Agenciado
    exclude = ('activo', 'fecha_ingreso')
    widgets = {
      'fecha_nacimiento': SelectDateWidget(years=range(date.today().year-100,date.today().year+1)),
      'deportes': CheckboxSelectMultiple,
      'danzas': CheckboxSelectMultiple,
      'instrumentos': CheckboxSelectMultiple,
      'idiomas': CheckboxSelectMultiple,
      }

BaseTelefonoFormSet = inlineformset_factory(Agenciado, Telefono, extra=6, max_num=6)
BaseFotoAgenciadoFormSet = inlineformset_factory(Agenciado, FotoAgenciado, extra=6, max_num=6)
VideoAgenciadoFormSet = inlineformset_factory(Agenciado, VideoAgenciado, extra=6, max_num=6)

class TelefonoFormSet(BaseTelefonoFormSet):
  def clean(self):
    super(TelefonoFormSet,self).clean()
    validarTelefonoIngresado(self)

class FotoAgenciadoFormSet(BaseFotoAgenciadoFormSet):
  def clean(self):
    super(FotoAgenciadoFormSet,self).clean()
    validarFotoIngresada(self)

@login_required
def agenciado(request):
  try:
    agenciado=Agenciado.objects.get(user__id=request.user.id)
  except Agenciado.DoesNotExist:
    agenciado=Agenciado()
    agenciado.user=request.user
    agenciado.fecha_ingreso = date.today()
    agenciado.activo=False

  if request.method == 'POST':
    form = AgenciadoForm(request.POST,instance=agenciado)
    telefonoFormSet=TelefonoFormSet(request.POST,request.FILES,instance=agenciado)
    fotoAgenciadoFormSet=FotoAgenciadoFormSet(request.POST,request.FILES,instance=agenciado)
    videoAgenciadoFormSet=VideoAgenciadoFormSet(request.POST,request.FILES,instance=agenciado)
    if form.is_valid() and telefonoFormSet.is_valid() and fotoAgenciadoFormSet.is_valid() and videoAgenciadoFormSet.is_valid():
      form.save()
      telefonoFormSet.save()
      fotoAgenciadoFormSet.save()
      videoAgenciadoFormSet.save()
      #@todo Indicar que los datos se han guardado en forma satisfactoria
      return redirect('/agencia/agenciado/')
  else:
    form = AgenciadoForm(instance=agenciado)
    telefonoFormSet=TelefonoFormSet(instance=agenciado)
    fotoAgenciadoFormSet=FotoAgenciadoFormSet(instance=agenciado)
    videoAgenciadoFormSet=VideoAgenciadoFormSet(instance=agenciado)
  return render(request,'agencia/agenciado.html',{'form':form, 'telefonoFormSet':telefonoFormSet, 'fotoAgenciadoFormSet':fotoAgenciadoFormSet, 'videoAgenciadoFormSet':videoAgenciadoFormSet})

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
      #@todo Indicar registro satisfactorio y que por favor complete sus datos a ser analizados por la agencia
      return redirect('/agencia/agenciado/')
  else:
    form = UserCreationForm()

  return render(request,'agencia/registro.html',{'form':form})

@login_required
def cambio_clave(request):
  if request.method == 'POST':
    form = SetPasswordForm(request.user,request.POST)
    if form.is_valid():
      form.save()
      #@todo Indicar cambio de password satisfactorio
      return redirect('/agencia/cambio/clave/')
  else:
    form = SetPasswordForm(request.user)

  return render(request,'agencia/cambio_clave.html',{'form':form})

def reiniciar_clave(request):
  if request.method == 'POST':
    form = PasswordResetForm(request.POST)
    if form.is_valid():
      user=User.objects.get(email=request.POST['email'])
      password = User.objects.make_random_password()
      user.set_password(password)
      user.save()
      # @todo Armar la url absoluta en forma dinamica.
      # @todo Enviar mail al agenciado
      cuerpo="\
Oi %s!\n\
\n\
Voce tem uma nova senha.\n\
\n\
Sua nova senha e (%s). Lembre que seu usuario e (%s).\n\
\n\
Voce pode trocar sua senha accesando a http://192.168.15.128:8000/agencia/cambio/clave/\n\
\n\
Atentamente, o equipe da Alternativa" % (user.username,password,user.username)
      from django.core.mail import EmailMessage
      email = EmailMessage('AgenciaAlternativa - Sua senha ha mudado', cuerpo, to=['agencia.test@gmail.com'])
      email.send()

      #@todo Indicar cambio de password satisfactorio
      return redirect('/agencia/reiniciar/clave/')
  else:
    form = PasswordResetForm()

  return render(request,'agencia/reiniciar_clave.html',{'form':form})
