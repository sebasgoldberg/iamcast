from django.contrib.auth.forms import AuthenticationForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Hidden
from django.contrib.auth.forms import SetPasswordForm, PasswordResetForm
from django import forms
from django.utils.translation import ugettext as _
from django.utils.translation import ugettext_lazy

class AgenciaAuthenticationForm(AuthenticationForm):

  def __init__(self, request=None, *args, **kwargs):

    self.helper = FormHelper()
    self.helper.form_class = 'uniForm'
    self.helper.form_method = 'post'
    self.helper.form_action = 'django.contrib.auth.views.login'
    self.helper.add_input(Submit('submit',_('Ingresar')))

    if request: 
      next_page = request.GET.get('next')
      if next_page:
        self.helper.add_input(Hidden('next', next_page))

    super(AgenciaAuthenticationForm, self).__init__(request, *args, **kwargs)

class AgenciaSetPasswordForm(SetPasswordForm):
  def __init__(self, *args, **kwargs):
    self.helper = FormHelper()
    self.helper.form_class = 'uniForm'
    self.helper.form_method = 'post'
    self.helper.form_action = '/agencia/cambio/clave/'
    self.helper.add_input(Submit('submit',_('Trocar')))
    super(AgenciaSetPasswordForm, self).__init__(*args, **kwargs)

class AgenciaPasswordResetForm(PasswordResetForm):
  next_page = forms.CharField(widget=forms.HiddenInput,required=False)
  def __init__(self, *args, **kwargs):
    self.helper = FormHelper()
    self.helper.form_class = 'uniForm'
    self.helper.form_method = 'post'
    self.helper.form_action = '/agencia/reiniciar/clave/'
    self.helper.add_input(Submit('submit',_('Gerar')))
    super(AgenciaPasswordResetForm, self).__init__(*args, **kwargs)
