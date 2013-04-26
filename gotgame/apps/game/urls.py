from django.conf.urls import patterns, url
from django.views.generic import TemplateView

from .views import GameResultView


urlpatterns = patterns('',
    url(r'^result/', GameResultView.as_view(), name='game_result'),
)
