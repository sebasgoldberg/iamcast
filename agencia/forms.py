from django.contrib.auth.forms import AuthenticationForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Hidden
from django.contrib.auth.forms import SetPasswordForm, PasswordResetForm
from django import forms
from django.utils.translation import ugettext as _
from django.utils.translation import ugettext_lazy
from direccion.forms import BaseDireccionForm
from agencia.models import DireccionAgencia, DireccionAgenciado

class DireccionAgenciaForm(BaseDireccionForm):
  class Meta:
    model = DireccionAgencia

class DireccionAgenciadoForm(BaseDireccionForm):
  class Meta:
    model = DireccionAgenciado
