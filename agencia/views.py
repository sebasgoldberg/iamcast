# coding=utf-8
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
from agencia.models import Agenciado, Telefono, FotoAgenciado, VideoAgenciado
from agencia.models import validarTelefonoIngresado, validarFotoIngresada
from datetime import date
from django.forms.models import inlineformset_factory
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.conf import settings

def index(request):
  return render(request,'agencia/index.html')

def logout_view(request):
  logout(request)
  return redirect('/agencia/')

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
      domain=settings.AMBIENTE.dominio

      cuerpo="\
Oi %s!\n\
\n\
Voce tem uma nova senha.\n\
\n\
Sua nova senha e (%s). Lembre que seu usuário e (%s).\n\
\n\
Voce pode trocar sua senha acessando a http://%s/agencia/cambio/clave/\n\
\n\
Atentamente, o equipe da Alternativa" % (user.first_name,password,user.username, domain)
      from django.core.mail import EmailMessage
      email = EmailMessage('AgenciaAlternativa - Sua senha ha mudado', cuerpo, to=[user.email])
      email.send()

      #@todo Indicar cambio de password satisfactorio
      return redirect('/agencia/reiniciar/clave/')
  else:
    form = PasswordResetForm()

  return render(request,'agencia/reiniciar_clave.html',{'form':form})
