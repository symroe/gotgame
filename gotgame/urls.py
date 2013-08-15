from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'gotgame.views.home', name='home'),
    # url(r'^gotgame/', include('gotgame.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # url(r'^game/', include('game.urls')),
    url(r'^admin/', include(admin.site.urls))
)


from tastypie.api import Api
from player.api.resources import PlayerResource

api_v1 = Api(api_name='v1')
api_v1.register(PlayerResource())

urlpatterns += patterns('',
    (r'^api/', include(api_v1.urls)),
)
