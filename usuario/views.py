# coding=utf-8
# Create your views here.

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.template import loader
from agencia.mail import MailAgencia
from django.contrib import messages
from django.template import RequestContext
from usuario.forms import UsuarioSetPasswordForm, UsuarioPasswordResetForm, UserCreateForm
from django.utils.translation import ugettext as _
from django.utils.translation import ugettext_lazy
from django.contrib.auth import logout
from django.contrib.auth import authenticate, login

@login_required
def cambio_clave(request):
  if request.method == 'POST':
    form = UsuarioSetPasswordForm(request.user,request.POST)

    if form.is_valid():
      form.save()
      messages.success(request, _(u'Sua senha foi trocada com sucesso'))
      return redirect('/usuario/cambio/clave/')
  else:
    form = UsuarioSetPasswordForm(request.user)


  return render(request,'usuario/cambio_clave.html',{'form':form})

def reiniciar_clave(request):
  if request.method == 'POST':
    form = UsuarioPasswordResetForm(request.POST)
    if form.is_valid():
      users=User.objects.filter(email=request.POST['email'])
      for user in users:
        password = User.objects.make_random_password()
        user.set_password(password)
        user.save()

        asunto = _(u'Sua senha ha mudado')
        template = loader.get_template('usuario/mail/cambio_clave.txt')
        context = RequestContext(request,{'usuario':user, 'clave':password})
        text_content = template.render(context)
        msg = MailAgencia(asunto,text_content,[user.email])
        msg.send()

        messages.success(request, _(u'Nova senha gerada com sucesso'))
        messages.info(request, _(u'Mail com nova senha enviado para %s')%user.email)

      next_page = form.cleaned_data['next_page']
      if not next_page:
        next_page = '/usuario/cambio/clave/'
      return redirect(next_page)
  else:
    form = UsuarioPasswordResetForm(initial={'next_page':request.GET.get('next')})

  return render(request,'usuario/reiniciar_clave.html',{'form':form,})

def logout_view(request):
  logout(request)
  return redirect('/')

def registro(request):
  if request.method == 'POST':
    form = UserCreateForm(request.POST)
    if form.is_valid():
      user = form.save()
      user = authenticate(username=request.POST['username'], password=request.POST['password1'])
      login(request,user)

      asunto = _(u'Sua conta esta creada')
      template = loader.get_template('usuario/mail/creacion.txt')
      context = RequestContext(request)
      text_content = template.render(context)
      msg = MailAgencia(asunto, text_content, [user.email])
      msg.send()

      messages.success(request,_(u'Registro realizado com sucesso!'))
      messages.info(request,_(u'Temos enviado para seu email dados da sua nova conta.'))
      messages.info(request,_(u'Por favor atualice os dados de seu perfil a ser analizados por nossa agencia.'))

      next_page = form.cleaned_data['next_page']
      if not next_page:
        next_page = '/'

      return redirect(next_page)
  else:
    next_page = request.GET.get('next')
    form = UserCreateForm(initial={'next_page':next_page})

  return render(request,'usuario/registro.html',{'form':form, })
