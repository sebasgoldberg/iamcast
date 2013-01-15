from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from agencia.models import Agenciado
from django.contrib.auth.models import User
from django.http import HttpRequest
from django.core.mail import EmailMessage

@receiver(post_save, sender=Agenciado)
def callback_mail_creacion_agenciado(sender, instance, created, raw, using, **kwargs):
  if instance.user is None:
    if instance.mail != '':
      password = User.objects.make_random_password()
      instance.user = User.objects.create_user(instance.mail,instance.mail,password)
      instance.user.first_name = instance.nombre 
      instance.user.last_name = instance.apellido 
      instance.user.email = instance.mail 
      instance.user.save()
      instance.save()
      # @todo Quitar return
      return
      # @todo Armar la url absoluta en forma dinamica.
      # @todo Enviar mail al agenciado
      cuerpo="\
Oi %s!\n\
\n\
Voce tem uma nova conta em https://agenciaalternativa.com/agencia/agenciado/ com dados de sue perfil.\n\
\n\
Voce podera ingresar a sua nova conta com seu usuario (%s) e sua clave (%s).\n\
\n\
Por favor, verifique se os dados da sua conta som corretos. Em caso de precisar modifique os dados que correspondam.\n\
\n\
Atentamente, o equipe da Alternativa" % (instance.nombre,instance.user.username,password)
      email = EmailMessage('AgenciaAlternativa - Seu perfil ja esta creado', cuerpo, to=['agencia.test@gmail.com'])
      email.send()
  else:
    modificado = False
    if instance.nombre != instance.user.first_name:
      instance.user.first_name = instance.nombre 
      modificado = True
    if instance.apellido != instance.user.last_name:
      instance.user.last_name = instance.apellido 
      modificado = True
    if instance.mail != instance.user.email:
      instance.user.email = instance.mail 
      modificado = True
    if modificado:
      instance.user.save()


