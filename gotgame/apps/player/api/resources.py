from __future__ import absolute_import

import facebook

from django.conf.urls import url
from django.http import HttpResponse

from tastypie.utils import trailing_slash
from tastypie import http, fields
from tastypie.resources import ModelResource

from title.models import Title, Console
from streak.models import Streak

from ..models import Player
from ..utils import create_or_update_player_from_token

from .authentication import ActivePlayerAuthentication
from .authorization import PlayerAuthorization

# POST parameter used during authentication.
USER_TOKEN_PARAM = 'user_token'

class PlayerTitleResource(ModelResource):
    class Meta:
        queryset = Title.objects.all()
        allowed_methods = ['get', ]
        # fields = ['id', 'fb_id', 'fb_token']
        authentication = ActivePlayerAuthentication()
        # authorization = PlayerAuthorization(player_rel='player__pk')
        include_resource_uri = False

class PlayerConsoleResource(ModelResource):
    class Meta:
        queryset = Console.objects.all()
        allowed_methods = ['get', ]
        # fields = ['id', 'fb_id', 'fb_token']
        authentication = ActivePlayerAuthentication()
        authorization = PlayerAuthorization(player_rel='player__pk')
        include_resource_uri = False

class PlayerActiveStreakResource(ModelResource):
    class Meta:
        queryset = Streak.objects.filter(active=True)
        allowed_methods = ['get', ]
        # fields = ['id', 'fb_id', 'fb_token']
        # authentication = ActivePlayerAuthentication()
        # authorization = PlayerAuthorization(player_rel='player__pk')
        include_resource_uri = False

class PlayerInActiveStreakResource(ModelResource):
    
    
    
    class Meta:
        queryset = Streak.objects.filter(active=False)
        allowed_methods = ['get', ]
        # fields = ['id', 'fb_id', 'fb_token']
        # authentication = ActivePlayerAuthentication()
        # authorization = PlayerAuthorization(player_rel='player__pk')
        include_resource_uri = False
    


class PlayerResource(ModelResource):
    """
    Player Resource.

    It adds a custom authenticate method.
    """
    
    titles = fields.ToManyField(
        PlayerTitleResource, 'titles', full=True, null=True, blank=True
    )
    consoles = fields.ToManyField(
        PlayerConsoleResource, 'consoles', full=True, null=True, blank=True
    )
    active_streaks = fields.ToManyField(
        PlayerActiveStreakResource, attribute=lambda bundle: Streak.objects.filter(player=bundle.obj, active=True), full=True, null=True, blank=True
    )
    inactive_streaks = fields.ToManyField(
        PlayerInActiveStreakResource, attribute=lambda bundle: Streak.objects.filter(player=bundle.obj, active=False), full=True, null=True, blank=True
    )
    
    
    class Meta:
        queryset = Player.objects.all()
        allowed_methods = ['get', ]
        authentication = ActivePlayerAuthentication()
        authorization = PlayerAuthorization(player_rel='pk')
        include_resource_uri = False

    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/authenticate%s$" % (self._meta.resource_name, trailing_slash()),
                self.wrap_view('authenticate'), name="authenticate"),
        ]
    
    def authenticate(self, request, **kwargs):
        """
        POST API call to authenticate a Player given a `user_token` (POST
        param), that is, the token generated by Facebook during the login
        process. This means that the facebook login has to be completed offline
        and before calling this API end point.
    
        It returns:
            * 400: If `user_token` not provided
            * 401: If `user_token` is invalid or the Player has been banned
            * 201: If a new Player has been created.
                   The field `new_player` will be True.
            * 200: If the Player was already existing.
                   The field `new_player` will be False.
    
        """
        self.method_check(request, allowed=['post'])
    
        deserialized = self.deserialize(request, request.body, format=request.META.get('CONTENT_TYPE', 'application/json'))
        deserialized = self.alter_deserialized_detail_data(request, deserialized)
    
        # user_token required, otherwise => 400
        user_token = deserialized.get(USER_TOKEN_PARAM)
    
        if not user_token:
            return self.error_response(request, 'user_token required', response_class=http.HttpBadRequest)
    
        try:
            player, created = create_or_update_player_from_token(user_token)
        except facebook.GraphAPIError as e:
            return self.error_response(request, e.message, response_class=http.HttpUnauthorized)
    
        # authenticating
        request.META[FACEBOOK_TOKEN_HEADER] = user_token
        self.is_authenticated(request)
    
        # returning the (new) player
        bundle = self.build_bundle(obj=player, request=request)
        bundle.data['new_player'] = created
        bundle = self.full_dehydrate(bundle)
        bundle = self.alter_detail_data_to_serialize(request, bundle)
    
        # if new player, notify friends
        if created:
            new_player_notify_friends.delay(player)
    
        return self.create_response(
            request, bundle,
            response_class=http.HttpCreated if created else HttpResponse
        )
    
