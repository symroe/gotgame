from __future__ import absolute_import

from tastypie import fields

from core.resources import GotGameModelResource

from player.api.authentication import ActivePlayerAuthentication

from ..models import Console, Title, ConsoleNetwork


class TitleResource(GotGameModelResource):
    class Meta:
        queryset = Title.objects.all()
        allowed_methods = []
        fields = ['platformTag']
        authentication = ActivePlayerAuthentication()
        include_resource_uri = False


class ConsoleResource(GotGameModelResource):
    titles = fields.ToManyField(
        TitleResource, 'title_set', full=True, null=False, blank=False
    )

    class Meta:
        queryset = Console.objects.all()
        allowed_methods = []
        fields = ['name']
        authentication = ActivePlayerAuthentication()
        include_resource_uri = False


class ConsoleNetworkResource(GotGameModelResource):
    consoles = fields.ToManyField(
        ConsoleResource, 'console_set', full=True, null=False, blank=False
    )

    class Meta:
        queryset = ConsoleNetwork.objects.all()
        allowed_methods = ['get']
        fields = ['name']
        authentication = ActivePlayerAuthentication()
        include_resource_uri = False
