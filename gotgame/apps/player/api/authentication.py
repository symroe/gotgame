from __future__ import absolute_import

from django.conf import settings

from tastypie.authentication import Authentication

from ..models import Player


class ActivePlayerAuthentication(Authentication):
    """
    (:class: `tastypie.authentication.Authentication`) that gets the
    facebook token header and checks that there's a Player associated
    with it.
    """
    def is_authenticated(self, request, **kwargs):
        """
        It returns False if the token is invalid, the Player doesn't exist
        or the Player has been banned (that is the `active` flag
        is set).

        It also set `request.player` so that the API Resources can access to it.
        """

        if settings.DEVELOPMENT:
            # TODO Remove in production
            fb_token = "123"
            try:
                player = Player.objects.get(fb_token=fb_token)
            except Player.DoesNotExist:
                player = Player(fb_token=fb_token)

            player.save()

            request.player = player
            return True

        # getting fb_token, if doesn't exist => return False
        fb_token = request.META.get(settings.FACEBOOK_TOKEN_HEADER)

        if not fb_token:
            return False

        # getting player, if doesn't exist => return False
        try:
            player = Player.objects.get(fb_token=fb_token)
        except Player.DoesNotExist:
            return False

        # checking if player is active, if not => return False
        if not self.check_active(player):
            return False

        request.player = player
        return True

    def get_identifier(self, request):
        """
        Returns the Player id.
        """
        return request.player.id
