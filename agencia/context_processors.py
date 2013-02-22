from alternativa.ambiente import ambiente
from agencia.models import FotoAgenciado


def add_ambiente(request):
    """
    Devuelve los datos del ambiente
    """
    return {'ambiente': ambiente }

def add_thumbnails_urls(request):
  """
  Devuelve 10 agenciados al azar que contengan al menos un thumbnai
  """
  todos = FotoAgenciado.objects.filter(agenciado__activo=True).order_by('?')
  thumbnails_urls = []
  for imagen_agenciado in todos:
    try:
      thumbnails_urls.append(imagen_agenciado.mini_thumbnail.url)
    except:
      continue
    if len(thumbnails_urls)==17:
      break

  return {'thumbnails_urls': thumbnails_urls}
