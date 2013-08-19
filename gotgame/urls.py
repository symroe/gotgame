from django.conf.urls import patterns, include, url
from django.conf import settings

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'gotgame.views.home', name='home'),
    # url(r'^gotgame/', include('gotgame.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # url(r'^game/', include('game.urls')),

    (r'^admin/api/', include('core.api.admin.urls')),

    url(r'^admin/', include(admin.site.urls)),
)

if settings.DEVELOPMENT:
    from django.views.generic import TemplateView
    from django.contrib.auth.decorators import login_required

    urlpatterns += patterns('',
            url(r'^get_fb_token/$', login_required(TemplateView.as_view(template_name='get_fb_token.html'))),
    )


from tastypie.api import Api
from player.api.resources import PlayerResource

api_v1 = Api(api_name='v1')
api_v1.register(PlayerResource())

urlpatterns += patterns('',
    (r'^api/', include(api_v1.urls)),
)
