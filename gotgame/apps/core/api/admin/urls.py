from django.contrib.admin.views.decorators import staff_member_required
from django.conf.urls.defaults import *

from .views import ApiExplorerView


urlpatterns = patterns('',
    url(r'^api-explorer/$', staff_member_required(ApiExplorerView.as_view()))
)
