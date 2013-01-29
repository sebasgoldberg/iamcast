# coding=utf-8
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from agencia.models import Agenciado
from django.contrib.auth.models import User
from django.http import HttpRequest
from django.db.utils import IntegrityError
from django.conf import settings
from django.template import loader, Context
from agencia.mail import MailAgencia
from django.contrib import messages

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
      asunto = 'Sua conta esta creada'
      template = loader.get_template('user/mail/creacion.txt')
      context = Context({'ambiente':settings.AMBIENTE,'user':instance})
      text_content = template.render(context)
      msg = MailAgencia(asunto, text_content, [instance.email])
      msg.send()
      messages.information(request, 'Mail com imformação da nova conta enviado para %s'%instance.mail)

