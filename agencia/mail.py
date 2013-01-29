# coding=utf-8
from django import forms
from django.conf import settings
from django.template import loader, Context
from django.core.mail import EmailMultiAlternatives
from django.contrib import messages

class MailForm(forms.Form):
  # @todo Agregar múltiples destinatarios.
  destinatario=forms.EmailField()
  asunto=forms.CharField()

class MailAgencia(EmailMultiAlternatives):

  def __init__(self,asunto, cuerpo_de_texto, destinatarios):
    
    _asunto = 'Agencia %s - %s' % (settings.AMBIENTE.agencia.nombre, asunto)
    _headers = {'Reply-To': settings.AMBIENTE.agencia.email}
    
    self.mensaje = EmailMultiAlternatives(
      _asunto,
      cuerpo_de_texto,
      settings.AMBIENTE.email.user,
      destinatarios,
      headers = _headers
    )

  def set_html_body(self,html_content):
    self.mensaje.attach_alternative(html_content, "text/html")

  def send(self):
    self.mensaje.send()
