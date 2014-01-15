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

from iampacks.agencia.trabajo.models import Trabajo


class CustomIndexDashboard(Dashboard):
    """
    Custom index dashboard for www.
    """
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
                    'title': _(u'facebook'),
                    'url': 'https://www.facebook.com/AgenciaAlternativa',
                    'external': True,
                },
                {
                    'title': _(u'Proponer una mejora'),
                    'url': 'https://github.com/sebasgoldberg/iamcast/issues/new#',
                    'external': True,
                },
            ]
        ))

        self.children.append(modules.Feed(
            title=_('Ultimas novedades de la aplicacion'),
            feed_url='https://github.com/sebasgoldberg/agencia/commits/master.atom',
            column=3,
            limit=5,
        ))
