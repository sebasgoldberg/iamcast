# coding=utf-8
# Create your views here.

from django.shortcuts import render_to_response, render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
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
from django.template import loader, Context
from agencia.mail import MailAgencia
from django.contrib import messages
from trabajo.models import Trabajo, ItemPortfolio
from django.template import RequestContext
from agencia.forms import AgenciaSetPasswordForm, AgenciaPasswordResetForm

def index(request):
  trabajos = Trabajo.objects.filter(estado='AT').order_by('-fecha_ingreso')[:3]
  portfolio = ItemPortfolio.objects.order_by('-fecha')[:3]
  return render(request,'agencia/index.html', { 'trabajos': trabajos, 'portfolio': portfolio})

def logout_view(request):
  logout(request)
  return redirect('/agencia/')

@login_required
def cambio_clave(request):
  if request.method == 'POST':
    form = AgenciaSetPasswordForm(request.user,request.POST)

    if form.is_valid():
      form.save()
      messages.success(request, 'Sua senha foi trocada com sucesso')
      return redirect('/agencia/cambio/clave/')
  else:
    form = AgenciaSetPasswordForm(request.user)


  return render(request,'agencia/cambio_clave.html',{'form':form})

def reiniciar_clave(request):
  if request.method == 'POST':
    form = AgenciaPasswordResetForm(request.POST)
    if form.is_valid():
      users=User.objects.filter(email=request.POST['email'])
      for user in users:
        password = User.objects.make_random_password()
        user.set_password(password)
        user.save()

        asunto = 'Sua senha ha mudado'
        template = loader.get_template('user/mail/cambio_clave.txt')
        context = RequestContext(request,{'usuario':user, 'clave':password})
        text_content = template.render(context)
        msg = MailAgencia(asunto,text_content,[user.email])
        msg.send()

        messages.success(request, 'Nova senha gerada com sucesso')
        messages.info(request, 'Mail com nova senha enviado para %s'%user.email)

      next_page = form.cleaned_data['next_page']
      if not next_page:
        next_page = '/agencia/cambio/clave/'
      return redirect(next_page)
  else:
    form = AgenciaPasswordResetForm(initial={'next_page':request.GET.get('next')})

  return render(request,'user/reiniciar_clave.html',{'form':form,})

def contacto(request):
  return render(request,'agencia/contacto.html')

