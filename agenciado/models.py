# coding=utf-8
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from agencia.models import Agenciado
from django.contrib.auth.models import User
from django.http import HttpRequest
from django.core.mail import EmailMessage
from django.db.utils import IntegrityError
from django.conf import settings

# @todo Ver si va a aplicar lo de la creación automática del usuario por agenciado
#@receiver(post_save, sender=Agenciado)
def callback_creacion_agenciado(sender, instance, created, raw, using, **kwargs):
  if instance.user is None:
    if instance.mail is not None:
      nombre = instance.nombre
      apellido = instance.apellido
      username = '%s_%s_%s' % (nombre.replace(' ','')[:11],apellido.replace(' ','')[:11],str(instance.recurso_id))
      password = User.objects.make_random_password()
      instance.user = User.objects.create_user(username,instance.mail,password)
      instance.user.first_name = instance.nombre[:30]
      instance.user.last_name = instance.apellido[:30]
      instance.user.email = instance.mail 
      instance.user.save()
      instance.save()
  else:
    modificado = False
    if instance.nombre[:30] != instance.user.first_name:
      instance.user.first_name = instance.nombre[:30]
      modificado = True
    if instance.apellido[:30] != instance.user.last_name:
      instance.user.last_name = instance.apellido[:30]
      modificado = True
    if instance.user.email != '' and instance.mail != instance.user.email:
      instance.user.email = instance.mail 
      modificado = True
    if modificado:
      instance.user.save()

@receiver(post_save, sender=User)
def callback_mail_creacion_usuario(sender, instance, created, raw, using, **kwargs):
  if not settings.AMBIENTE_PRODUCTIVO:
    return
  if created:
    if instance.email is not None:
      domain=settings.AMBIENTE.dominio
      cuerpo=u"\
Oi %s!\n\
\n\
Voce tem uma nova conta em http://%s/ com dados de sue perfil.\n\
\n\
Se voce e um agenciado, entao pode caregar informaçao de seu perfil: http://%s/agenciado/\n\
\n\
Se voce e um agenciador pode accesar a administraçao do site: http://%s/admin/\n\
\n\
Voce podera ingresar a sua nova conta com seu usuario (%s) e sua chave.\n\
\n\
Se voce nao lembra sua chave, podera gerarla de novo aqui: http://%s/agencia/reiniciar/clave/\n\
\n\
Por favor, verifique se os dados da sua conta som corretos. Em caso de precisar modifique os dados que correspondam.\n\
\n\
Atentamente, o equipe da Alternativa\n\
agencia.alternativa@gmail.com" % (instance.first_name,domain,domain,domain,instance.username,domain)
      # @todo enviar al mail correspondiente
      email = EmailMessage('AgenciaAlternativa[no responder] - Sua conta esta creada', cuerpo, to=[instance.email])
      email.send()
