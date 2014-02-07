# coding=utf-8
"""
This file was generated with the customdashboard management command and
contains the class for the main dashboard.

To activate your index dashboard add the following to your settings.py::
    GRAPPELLI_INDEX_DASHBOARD = 'iamcast.dashboard.CustomIndexDashboard'
"""

from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse

from grappelli.dashboard import modules, Dashboard
from grappelli.dashboard.utils import get_admin_site_name
from django.conf import settings

from iampacks.agencia.trabajo.models import Trabajo, EventoTrabajo, EventoRol

from datetime import datetime, date, timedelta


class CustomIndexDashboard(Dashboard):
    """
    Custom index dashboard for www.
    """
    def add_eventos_del_dia(self):

      today_date=date.today()

      eventos_dia_trabajo=list(
        EventoTrabajo.objects.filter(
          fecha__year=today_date.year,
          fecha__month=today_date.month,
          fecha__day=today_date.day).order_by('fecha')
        )

      eventos_dia_rol=list(
        EventoRol.objects.filter(
          fecha__year=today_date.year,
          fecha__month=today_date.month,
          fecha__day=today_date.day).order_by('fecha')
        )

      eventos_dia=eventos_dia_trabajo+eventos_dia_rol

      eventos_dia.sort(key=lambda x: x.fecha)

      links=tuple([
        ['%s - %s'%(e, e.get_object()), e.get_object().admin_url()] for e in eventos_dia
        ])

      self.children.append(modules.LinkList(
        _('Eventos del Dia'),
        column=3,
        children=links
      ))

      return links

    def add_proximos_eventos(self):

      tomorow_date=date.today() + timedelta(days=1)
      tomorow_datetime=datetime(tomorow_date.year,tomorow_date.month,tomorow_date.day)
      week_date=date.today() + timedelta(days=6)
      week_datetime=datetime(week_date.year,week_date.month,week_date.day)

      proximos_eventos_trabajo=list(
        EventoTrabajo.objects.filter(fecha__gte=tomorow_datetime,fecha__lte=week_datetime)
        )

      proximos_eventos_rol=list(
        EventoRol.objects.filter(fecha__gte=tomorow_datetime,fecha__lte=week_datetime)
        )

      proximos_eventos = proximos_eventos_trabajo + proximos_eventos_rol

      proximos_eventos.sort(key=lambda x: x.fecha)

      links=tuple([
        ['%s - %s'%(e, e.get_object()), e.get_object().admin_url()] for e in proximos_eventos
        ])

      self.children.append(modules.LinkList(
        _('Proximos Eventos'),
        column=3,
        children=links
      ))

      return links

    def add_ultimos_trabajos(self,cantidad_trabajos):

      ultimos_trabajos=tuple([
        [t,t.admin_url()] for t in Trabajo.objects.order_by('-id')[:cantidad_trabajos]
        ])

      # append another link list module for "support".
      self.children.append(modules.LinkList(
        _('Ultimos Trabajos'),
        column=2,
        children=ultimos_trabajos
      ))
    
    def init_with_context(self, context):
        site_name = get_admin_site_name(context)
        
        # append a group for "Administration" & "Applications"
        self.children.append(modules.Group(
            _('Aplicaciones Principales'),
            column=1,
            collapsible=True,
            children = [
                modules.ModelList(
                    column=1,
                    collapsible=False,
                    models=('iampacks.agencia.agencia.models.Agenciado',),
                ),
                modules.ModelList(
                    column=1,
                    collapsible=False,
                    models=(
                      'iampacks.agencia.trabajo.models.Trabajo',
                      ),
                ),
                modules.ModelList(
                    column=1,
                    collapsible=False,
                    models=(
                      'iampacks.agencia.trabajo.models.ItemPortfolio',
                      ),
                ),
            ]
        ))
        
        # append an app list module for "Applications"
        self.children.append(modules.ModelList(
            _('Diccionario de datos'),
            collapsible=True,
            column=1,
            models=('iampacks.agencia.perfil.*',)
        ))
        
        # append an app list module for "Administration"
        self.children.append(modules.ModelList(
            _('Administracion de usuarios y permisos'),
            column=1,
            collapsible=False,
            models=('django.contrib.*',),
        ))

        self.add_ultimos_trabajos(5)

        # append a recent actions module
        self.children.append(modules.RecentActions(
            _('Recent Actions'),
            limit=5,
            collapsible=True,
            column=2,
        ))

        self.add_eventos_del_dia()
        self.add_proximos_eventos()

        # append another link list module for "support".
        self.children.append(modules.LinkList(
            _('Links'),
            column=3,
            children=[
                {
                    'title': settings.AMBIENTE.dominio,
                    'url': '/',
                    'external': False,
                },
                {
                    'title': _(u'Proponer una mejora'),
                    'url': 'https://github.com/sebasgoldberg/iamcast/issues/new#',
                    'external': True,
                },
            ]
        ))

