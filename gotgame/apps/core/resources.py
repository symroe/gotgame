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
    def is_valid(self, bundle):
        """
            Flatterns the errors so that instead of being returned as:
            {
                <model-name>: {
                    'field1': ['error1'],
                    'field2': ['error2'],
                }
            }
            are returned as:
            {
                'field1': ['error1'],
                'field2': ['error2'],
            }
        """
        errors = self._meta.validation.is_valid(bundle, bundle.request)

        if errors:
            bundle.errors = errors
            return False
        return True

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
