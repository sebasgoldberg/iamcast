# coding=utf-8
from django import forms
from django.conf import settings
from django.template import loader, Context
from django.core.mail import EmailMultiAlternatives
from django.contrib import messages

class MailForm(forms.Form):
  # @todo Agregar múltiples destinatarios.
  destinatarios=forms.CharField(widget=forms.Textarea, help_text=u'Adicione os destinatarios separados por ",", ";" ou salto de linea')
  asunto=forms.CharField()

  def get_destinatarios(self):
    destinatarios_text = self.cleaned_data['destinatarios']
    destinatarios = []
    for destinatario in destinatarios_text.replace('\n',',').replace(';',',').replace('\r',',').split(','):
      if destinatario != '':
        destinatarios+=[destinatario]
    return destinatarios
  

class MailAgencia(EmailMultiAlternatives):

  def __init__(self,asunto, cuerpo_de_texto, destinatarios,ccs=None):
    
    _asunto = 'Agencia %s - %s' % (settings.AMBIENTE.agencia.nombre, asunto)
    _headers = {'Reply-To': settings.AMBIENTE.agencia.email}
    
    self.mensaje = EmailMultiAlternatives(
      _asunto,
      cuerpo_de_texto,
      settings.AMBIENTE.email.user,
      destinatarios,
      headers = _headers,
      cc=ccs
    )

  def set_html_body(self,html_content):
    self.mensaje.attach_alternative(html_content, "text/html")

  def send(self):
    self.mensaje.send()
