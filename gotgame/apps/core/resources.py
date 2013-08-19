from tastypie.resources import ModelResource


class GotGameModelResource(ModelResource):
    """
       ModelResource which makes sure that the authenticated player
       doesn't have access to others resources.

       The default implementation looks for an authorization object with a
       property `player_rel` which defines the relationship between the
       resource and the Player.

       The authorization object is usually
       (:class: player.api.authorization.PlayerAuthorization).
    """
    def get_object_list(self, request):
        """
            Filters the queryset including only the resources the authenticated
            player has access to.
        """
        object_list = super(GotGameModelResource, self).get_object_list(request)

        if self._meta.authorization and hasattr(self._meta.authorization, 'player_rel'):
            object_list = object_list.filter(**{
                self._meta.authorization.player_rel: request.player.pk
            })

        return object_list
