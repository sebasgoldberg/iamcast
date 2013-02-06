# Create your views here.

from django.shortcuts import render_to_response, render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth.forms import UserCreationForm, SetPasswordForm, PasswordResetForm
from django.contrib.auth.models import Group
from django.contrib.auth import authenticate, login
from django.forms import ModelForm
from django.forms.extras.widgets import SelectDateWidget
from agencia.models import Agenciado, Telefono, FotoAgenciado, VideoAgenciado
from agencia.models import validarTelefonoIngresado, validarFotoIngresada
from datetime import date
from django.forms.models import inlineformset_factory
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.contrib import messages
from django import forms
from django.conf import settings

from itertools import chain
from django.forms.widgets import CheckboxSelectMultiple, CheckboxInput
from django.utils.encoding import force_unicode
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe
from django.template import RequestContext
from agencia.mail import MailAgencia
from django.template import loader

class BPCheckboxSelectMultiple(CheckboxSelectMultiple):

  def render(self, name, value, attrs=None, choices=()):
    if value is None: value = []
    has_id = attrs and 'id' in attrs
    final_attrs = self.build_attrs(attrs, name=name)
    output = [u'<div class="span-24">']
    # Normalize to strings
    str_values = set([force_unicode(v) for v in value])
    for i, (option_value, option_label) in enumerate(chain(self.choices, choices)):
      # If an ID attribute was given, add a numeric index as a suffix,
      # so that the checkboxes don't all have the same ID attribute.
      if has_id:
        final_attrs = dict(final_attrs, id='%s_%s' % (attrs['id'], i))
        label_for = u' for="%s"' % final_attrs['id']
      else:
        label_for = ''

      cb = CheckboxInput(final_attrs, check_test=lambda value: value in str_values)
      option_value = force_unicode(option_value)
      rendered_cb = cb.render(name, option_value)
      option_label = conditional_escape(force_unicode(option_label))
      if ((i+1) % 6) == 0:
        indicador_ultimo_linea = u'last'
      else:
        indicador_ultimo_linea = u''
      output.append(u'<div class="span-4 %s"><label%s>%s %s</label></div>' % (indicador_ultimo_linea, label_for, rendered_cb, option_label))
    output.append(u'</div>')
    return mark_safe(u'\n'.join(output))

class AgenciadoForm(ModelForm):
  class Meta:
    model = Agenciado
    exclude = ('activo', 'fecha_ingreso')
    widgets = {
      'fecha_nacimiento': SelectDateWidget(years=range(date.today().year-100,date.today().year+1)),
      'deportes': BPCheckboxSelectMultiple,
      'danzas': BPCheckboxSelectMultiple,
      'instrumentos': BPCheckboxSelectMultiple,
      'idiomas': BPCheckboxSelectMultiple,
      }

BaseTelefonoFormSet = inlineformset_factory(Agenciado, Telefono, extra=6, max_num=6)
BaseFotoAgenciadoFormSet = inlineformset_factory(Agenciado, FotoAgenciado, extra=6, max_num=6)
VideoAgenciadoFormSet = inlineformset_factory(Agenciado, VideoAgenciado, extra=6, max_num=6, exclude=['codigo_video'])

class TelefonoFormSet(BaseTelefonoFormSet):
  def clean(self):
    super(TelefonoFormSet,self).clean()
    validarTelefonoIngresado(self)

class FotoAgenciadoFormSet(BaseFotoAgenciadoFormSet):
  def clean(self):
    super(FotoAgenciadoFormSet,self).clean()
    validarFotoIngresada(self)

@login_required
def index(request):
  try:
    agenciado=Agenciado.objects.get(user__id=request.user.id)
  except Agenciado.DoesNotExist:
    agenciado=Agenciado(
      user=request.user,
      nombre = request.user.first_name,
      apellido = request.user.last_name,
      mail = request.user.email,
      fecha_ingreso = date.today(),
      activo=False,
    )

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
      messages.success(request, 'Dados atualizados com sucesso')
      return redirect('/agenciado/')
  else:
    form = AgenciadoForm(instance=agenciado)
    telefonoFormSet=TelefonoFormSet(instance=agenciado)
    fotoAgenciadoFormSet=FotoAgenciadoFormSet(instance=agenciado)
    videoAgenciadoFormSet=VideoAgenciadoFormSet(instance=agenciado)
  return render(request,'agenciado/agenciado.html',{'form':form, 'telefonoFormSet':telefonoFormSet, 'fotoAgenciadoFormSet':fotoAgenciadoFormSet, 'videoAgenciadoFormSet':videoAgenciadoFormSet, })

def validate_unique_mail(value):
  users=User.objects.filter(email=value)
  if len(users)>0:
    raise ValidationError('O email ingresado ja existe')

class UserCreateForm(UserCreationForm):
  email = forms.EmailField(required=True, validators=[validate_unique_mail])
  first_name = forms.CharField( max_length=30, required=True)
  last_name = forms.CharField( max_length=30, required=True)

  class Meta:
    model = User
    fields = ( "username", 'password1', 'password2', "email", "first_name", 'last_name', )

def registro(request):
  if request.method == 'POST':
    form = UserCreateForm(request.POST)
    if form.is_valid():
      user = form.save()
      user = authenticate(username=request.POST['username'], password=request.POST['password1'])
      login(request,user)

      asunto = 'Sua conta esta creada'
      template = loader.get_template('user/mail/creacion.txt')
      context = RequestContext(request)
      text_content = template.render(context)
      msg = MailAgencia(asunto, text_content, [user.email])
      msg.send()

      messages.success(request,'Registro realizado com sucesso!')
      messages.info(request,'Temos enviado para seu email dados da sua nova conta.')
      messages.info(request,'Por favor atualice os dados de seu perfil a ser analizados por nossa agencia.')
      return redirect('/agenciado/')
  else:
    form = UserCreateForm()

  return render(request,'user/registro.html',{'form':form, })

