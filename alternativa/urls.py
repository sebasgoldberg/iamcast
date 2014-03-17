from django.conf.urls import patterns, include, url
from django.conf import settings
from django.views.generic import RedirectView
from iampacks.cross.usuario.forms import UsuarioAuthenticationForm

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'alternativa.views.home', name='home'),
    # url(r'^alternativa/', include('alternativa.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^$', 'alternativa.views.home', name='home'),
    url(r'^grappelli/', include('grappelli.urls')), # grappelli URLS
    url(r'^admin/password_reset/$', RedirectView.as_view(url='/usuario/reiniciar/clave/'), name='admin_password_reset'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^uploads/(?P<path>.*)$', 'django.views.static.serve',
      {'document_root': settings.MEDIA_ROOT}),
    url(r'^agencia/', include('iampacks.agencia.agencia.urls')),
    url(r'^agenciado/', include('iampacks.agencia.agenciado.urls')),
    url(r'^trabajo/', include('iampacks.agencia.trabajo.urls')),
    url(r'^accounts/login/$', 'django.contrib.auth.views.login', {'authentication_form':UsuarioAuthenticationForm}),
    url(r'^accounts/profile/$', 'iampacks.agencia.agenciado.views.index'),
    url(r'^$', RedirectView.as_view(url='/agencia/')),
    url(r'^i18n/', include('django.conf.urls.i18n')),
    #url(r'^chaining/', include('smart_selects.urls')),
    url(r'^direccion/', include('iampacks.cross.direccion.urls')),
    url(r'^usuario/', include('iampacks.cross.usuario.urls')),
    url(r'^captcha/', include('captcha.urls')),
    url(r'^zohoverify/', include('zohoverify.urls')),
)

