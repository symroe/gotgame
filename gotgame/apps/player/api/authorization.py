from tastypie.exceptions import Unauthorized
from tastypie.authorization import Authorization


class PlayerAuthorization(Authorization):
    """
       (:class: tastypie.authorization.Authorization) which filters the objects
       by current authenticated player (that is request.player).

       This is to avoid player access to things that they were not supposed to.

       When instantiating, you need to pass the django path to access to the
       player object from the resource you are defining.
       E.g. if MyResource has a ForeignKey to Player, you need to specify:
       `player__pk`.

       NOTE: THIS MUST BE USED BY ALL THE RESOURCES RELATED TO A PLAYER

       Usage::
            class MyResource(NamespacedModelResource):
                ...
                class Meta:
                    ...
                    authorization = PlayerAuthorization(player_rel='player__pk')
    """
    def __init__(self, player_rel):
        self.player_rel = player_rel

    def _filter_list(self, object_list, bundle):
        """
            Generic internal method that filters `object_list` including
            only the objects related to the authenticated player.
        """
        kwargs = {
            self.player_rel: bundle.request.player.pk
        }
        return object_list.filter(**kwargs)

    def read_list(self, object_list, bundle):
        """
            Returns a list of objects the authenticated player has access to.
        """
        return self._filter_list(object_list, bundle)

    def read_detail(self, object_list, bundle):
        """
            Returns the object requested or raises (:class: tastypie.exceptions.Unauthorized)
            if the Player doesn't have access to it.
        """
        if not self._filter_list(object_list, bundle):
            raise Unauthorized("You are not allowed to access that resource.")
        return True

    def create_list(self, object_list, bundle):
        """
            Not supported.
        """
        return []

    def create_detail(self, object_list, bundle):
        """
            Never allowed.
        """
        raise Unauthorized("You are not allowed to create that resource.")

    def update_list(self, object_list, bundle):
        """
            Not supported.
        """
        return []

    def update_detail(self, object_list, bundle):
        """
            Returns the object requested or raises (:class: tastypie.exceptions.Unauthorized)
            if the Player doesn't have access to it.
        """
        if not self._filter_list(object_list, bundle):
            raise Unauthorized("You are not allowed to update that resource.")
        return True

    def delete_list(self, object_list, bundle):
        """
            Not supported.
        """
        return []

    def delete_detail(self, object_list, bundle):
        """
            Returns True if the Player can delete the object or raises
            (:class: tastypie.exceptions.Unauthorized) otherwise.
        """
        if not bundle or not bundle.obj:
            raise Unauthorized("You are not allowed to delete that resource.")

        value = bundle.obj
        for prop in self.player_rel.split('__'):
            value = getattr(value, prop)

        if value != bundle.request.player.pk:
            raise Unauthorized("You are not allowed to delete that resource.")

        return True