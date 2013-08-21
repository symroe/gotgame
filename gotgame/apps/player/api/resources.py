from __future__ import absolute_import

import facebook

from django.conf.urls import url
from django.http import HttpResponse
from django.conf import settings

from tastypie.utils import trailing_slash
from tastypie import http, fields
from tastypie.validation import CleanedDataFormValidation

from title.models import Title
from streak.models import Streak

from core.resources import GotGameModelResource

from ..models import Player, PlayerConsoleNetwork
from ..utils import create_or_update_player_from_token

from .authentication import ActivePlayerAuthentication
from .authorization import PlayerAuthorization
from .constants import PERSONAL_DETAILS_FIELDS
from .forms import PersonalDetailsForm


# POST parameter used during authentication.
USER_TOKEN_PARAM = 'user_token'


class PlayerTitleResource(GotGameModelResource):
    class Meta:
        queryset = Title.objects.all()
        allowed_methods = []
        # fields = ['id', 'fb_id', 'fb_token']
        authentication = ActivePlayerAuthentication()
        # authorization = PlayerAuthorization(player_rel='player__pk')
        include_resource_uri = False


class PlayerConsoleNetworkResource(GotGameModelResource):
    name = fields.CharField(attribute='network__name')

    class Meta:
        queryset = PlayerConsoleNetwork.objects.all()
        allowed_methods = []
        fields = ['gamer_tag']
        authentication = ActivePlayerAuthentication()
        authorization = PlayerAuthorization(player_rel='player__pk')
        include_resource_uri = False


class PlayerActiveStreakResource(GotGameModelResource):
    class Meta:
        queryset = Streak.objects.filter(active=True)
        allowed_methods = []
        # fields = ['id', 'fb_id', 'fb_token']
        # authentication = ActivePlayerAuthentication()
        # authorization = PlayerAuthorization(player_rel='player__pk')
        include_resource_uri = False


class PlayerInActiveStreakResource(GotGameModelResource):
    class Meta:
        queryset = Streak.objects.filter(active=False)
        allowed_methods = ['get', ]
        # fields = ['id', 'fb_id', 'fb_token']
        # authentication = ActivePlayerAuthentication()
        # authorization = PlayerAuthorization(player_rel='player__pk')
        include_resource_uri = False


class PersonalDetailsResource(GotGameModelResource):
    """
    Personal Details Resource.
    """
    class Meta:
        queryset = Player.objects.all()
        allowed_methods = ['get', 'put']
        fields = PERSONAL_DETAILS_FIELDS
        authentication = ActivePlayerAuthentication()
        authorization = PlayerAuthorization(player_rel='pk')
        validation = CleanedDataFormValidation(form_class=PersonalDetailsForm)
        include_resource_uri = False


class PlayerResource(GotGameModelResource):
    """
    Player Resource.

    It adds a custom authenticate method.
    """

    titles = fields.ToManyField(
        PlayerTitleResource, 'titles', full=True, null=True, blank=True
    )
    networks = fields.ToManyField(
        PlayerConsoleNetworkResource, attribute=lambda bundle: bundle.obj.networks.through.objects.filter(player=bundle.obj) or bundle.obj.networks, full=True, null=True, blank=True
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
        fields = ['id', 'fb_id', 'fb_token', 'credits', 'first_name', 'last_name', 'email']
        authentication = ActivePlayerAuthentication()
        authorization = PlayerAuthorization(player_rel='pk')
        include_resource_uri = False

    def __init__(self, *args, **kwargs):
        super(PlayerResource, self).__init__(*args, **kwargs)

        self.personal_details_resource = PersonalDetailsResource()

    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>%s)%s$" % (self._meta.resource_name, trailing_slash()),
                self.wrap_view('details'), name="details"),

            url(r"^(?P<resource_name>%s)/authenticate%s$" % (self._meta.resource_name, trailing_slash()),
                self.wrap_view('authenticate'), name="authenticate"),

            url(r"^(?P<resource_name>%s)/personaldetails%s$" % (self._meta.resource_name, trailing_slash()),
                self.wrap_view('dispatch_personal_details'), name="personaldetails"),
        ]

    def details(self, request, **kwargs):
        """
            Dispatches the request to detail.
            Here to override the default tastypie implementation so that
            `player/' returns the player detail instead of the list of
            players.

            It's a shortcut to `player/<player-id>/`.
        """
        return self.dispatch_detail(request, **kwargs)

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
        request.META[settings.FACEBOOK_TOKEN_HEADER] = user_token
        self.is_authenticated(request)

        # returning the (new) player
        bundle = self.build_bundle(obj=player, request=request)
        bundle.data['new_player'] = created
        bundle = self.full_dehydrate(bundle)
        bundle = self.alter_detail_data_to_serialize(request, bundle)

        return self.create_response(
            request, bundle,
            response_class=http.HttpCreated if created else HttpResponse
        )

    def dispatch_personal_details(self, request, **kwargs):
        """
        `personaldetails` end point.


        It filters the request by player to be sure that we don't expose anything data
        of other players and dispatches the request to the (:class: PersonalDetailsResource).
        """
        self.is_authenticated(request)
        kwargs['pk'] = request.player.pk
        return self.personal_details_resource.dispatch('detail', request, **kwargs)
