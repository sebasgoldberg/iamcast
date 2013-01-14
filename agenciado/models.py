from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from agencia.models import Agenciado
from django.core.exceptions import ValidationError

@receiver(pre_save, sender=Agenciado)
def callback_mail_creacion_agenciado(sender, **kwargs):

  if not sender.user:
    if sender.mail != '':
      password = User.objects.make_random_password()
      sender.user = User.objects.create_user(sender.mail,sender.mail,password)
      from django.core.mail import EmailMessage
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
Atentamente, o equipe da Alternativa" % (sender.nombre,sender.user.username,password)
      email = EmailMessage('AgenciaAlternativa - Seu perfil ja esta creado', cuerpo, to=['agencia.test@gmail.com'])
      email.send()

