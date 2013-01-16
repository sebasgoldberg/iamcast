from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from agencia.models import Agenciado
from django.contrib.auth.models import User
from django.http import HttpRequest
from django.core.mail import EmailMessage
from django.db.utils import IntegrityError

@receiver(post_save, sender=Agenciado)
def callback_mail_creacion_agenciado(sender, instance, created, raw, using, **kwargs):
  if instance.user is None:
    if instance.mail is not None:
      nombre = instance.nombre
      apellido = instance.apellido
      username = '%s_%s_%s' % (nombre.replace(' ','')[:11],apellido.replace(' ','')[:11],str(instance.recurso_id))
      password = User.objects.make_random_password()
      try:
        instance.user = User.objects.create_user(username,instance.mail,password)
      except IntegrityError:
        # @todo Tener en cuenta el '_.', luego de esto aparece el mail verdadero
        instance.user = User.objects.create_user(username,str(instance.recurso_id)+'_.'+instance.mail,password)
      instance.user.first_name = instance.nombre[:30]
      instance.user.last_name = instance.apellido[:30]
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
    if instance.nombre[:30] != instance.user.first_name:
      instance.user.first_name = instance.nombre[:30]
      modificado = True
    if instance.apellido[:30] != instance.user.last_name:
      instance.user.last_name = instance.apellido[:30]
      modificado = True
    #if instance.mail != instance.user.email:
    #  instance.user.email = instance.mail 
    #  modificado = True
    if modificado:
      instance.user.save()


