# coding=utf-8
from django.db import models
import cities_light
from cities_light.models import City, Region, Country
from django.utils.translation import ugettext_lazy
from django.db import router

COUNTRY_FILTER = ('AR', 'BR')

def filter_city_import(sender, items, **kwargs):
  if items[8] not in ('AR', 'BR'):
    raise cities_light.InvalidItems()

cities_light.signals.city_items_pre_import.connect(filter_city_import)

def filter_region_import(sender, items, **kwargs):
  if items[0].split('.')[0] not in ('AR', 'BR'):
    raise cities_light.InvalidItems()

cities_light.signals.region_items_pre_import.connect(filter_region_import)

class CrossDbForeignKey(models.ForeignKey):
  def validate(self, value, model_instance):
    if self.rel.parent_link:
      return
    super(models.ForeignKey, self).validate(value, model_instance)
    if value is None:
      return

    using = router.db_for_read(self.rel.to, instance=model_instance)
    qs = self.rel.to._default_manager.using(using).filter(
          **{self.rel.field_name: value}
       )
    qs = qs.complex_filter(self.rel.limit_choices_to)
    if not qs.exists():
      raise exceptions.ValidationError(self.error_messages['invalid'] % {
        'model': self.rel.to._meta.verbose_name, 'pk': value})

class Direccion(models.Model):
  descripcion = models.CharField(max_length=60, verbose_name=ugettext_lazy(u'Descripção'),blank=True,null=True)
  pais = CrossDbForeignKey(Country,on_delete=models.PROTECT, verbose_name=ugettext_lazy(u'Pais'),null=True, blank=False, limit_choices_to = {'code2__in': COUNTRY_FILTER})
  estado = CrossDbForeignKey(Region, on_delete=models.PROTECT, verbose_name=ugettext_lazy(u'Estado'),null=True, blank=False)
  ciudad = CrossDbForeignKey(City, on_delete=models.PROTECT, verbose_name=ugettext_lazy(u'Cidade'),null=True, blank=False)
  barrio = models.CharField(max_length=60, verbose_name=ugettext_lazy(u'Barrio'), blank=True, null=True)
  direccion = models.CharField(max_length=120, verbose_name=ugettext_lazy(u'Endereço'))
  codigo_postal = models.CharField(max_length=40, verbose_name=ugettext_lazy(u'CEP'), blank=True, null=True)

  class Meta:
    abstract = True
    verbose_name = ugettext_lazy(u"Endereço")
    verbose_name_plural = ugettext_lazy(u"Endereços")

  def __unicode__(self):
    return "%s, %s, %s, %s" % (self.direccion, self.barrio, self.ciudad, self.codigo_postal)

